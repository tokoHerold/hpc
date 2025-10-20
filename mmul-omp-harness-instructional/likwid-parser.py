import re
import pandas as pd
import os

# --- Constants for DataFrame column names ---
BENCHMARK = 'Benchmark'
PROBLEM_SIZE = 'Problem Size'
NUM_THREADS = 'Number of threads'
NUM_BLOCKS = 'Number of blocks'
RUNTIME_CHRONO = 'Runtime (chrono)'
RUNTIME_RDTSC = 'Runtime (RDTSC)'
INSTRUCTION_COUNT = 'Instruction Count'
CPI = 'CPI'
MAX_CLOCK = 'Max Clock'
MIN_CLOCK = 'Min Clock'
CPU_CLOCKS_UNHALTED = 'CPU_CLOCKS_UNHALTED'
L3_ACCESS_ALL = 'L3_ACCESS_ALL_TYPES'
L3_MISSES = 'L3 Misses'
L2_ACCESSES = 'L2 accesses'
L2_MISSES = 'L2 misses'
RUN_COMMAND = 'Run Command'

# --- Input File paths ---
files_to_parse = [
    "data/raw/basic-flops_dp.out",
    "data/raw/basic-l2cache.out",
    "data/raw/basic-l3cache.out",
    "data/raw/blas-flops_dp.out",
    "data/raw/blas-l2cache.out",
    "data/raw/blas-l3cache.out",
    "data/raw/blocked-flops_dp.out",
    "data/raw/blocked-l2cache.out",
    "data/raw/blocked-l3cache.out"
]


class MetricGroup:
    """
    A class to hold the configuration for a group of metrics.

    Args:
        name (str): The name of the metric group (e.g., 'FLOPS_DP').
        files_keyword (str): A unique string to identify files belonging to this group.
        output_file (str): The filename for the output CSV.
        columns (dict): A mapping of desired DataFrame column names to the metric names in the LIKWID output.
        stat_types (dict, optional): Specifies which statistic (Sum, Min, Max, Avg) to use for multi-threaded runs. Defaults to {}.
        value_types (dict, optional): Specifies the desired data type (e.g., int, float) for each column. Defaults to {}.
        """
    def __init__(self, name, files_keyword, output_file, columns, stat_types={}, value_types={}):
        self.name = name
        self.files_keyword = files_keyword
        self.output_file = output_file
        self.columns = columns
        self.stat_types = stat_types
        self.value_types = value_types


# -- Desired Ouput Metrics --
output_files = [
    MetricGroup(
        name='FLOPS_DP',
        files_keyword='flops_dp',
        output_file='data/flops_dp_data.csv',
        columns={
            RUNTIME_RDTSC: 'Runtime (RDTSC) [s]',
            INSTRUCTION_COUNT: 'RETIRED_INSTRUCTIONS',
            CPI: 'CPI'
        },
        stat_types={RUNTIME_RDTSC: 'Max', CPI: 'Avg'},
        value_types={INSTRUCTION_COUNT: int}
    ),
    MetricGroup(
        name='L2CACHE',
        files_keyword='l2cache',
        output_file='data/l2_cache_data.csv',
        columns={
            L2_ACCESSES: 'L2 accesses',
            L2_MISSES: 'L2 misses'
        },
        value_types={L2_ACCESSES: int, L2_MISSES: int}
    ),
    MetricGroup(
        name='L3CACHE',
        files_keyword='l3cache',
        output_file='data/l3_cache_data.csv',
        columns={
            L3_ACCESS_ALL: 'L3_ACCESS_ALL_TYPES'
        },
        value_types={L3_ACCESS_ALL: int}
    )
]


def parse_likwid_output(file_path, group_config):
    """
    Parses a LIKWID output file to extract a specified set of performance metrics.

    Args:
        file_path (str): The path to the .out file.
        group_config (MetricGroup): A MetricGroup object specifying which metrics to extract.

    Returns:
        list: A list of dictionaries, each representing a test run.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    runs = re.split(r'likwid-perfctr', content)
    runs = [run for run in runs if run.strip()]
    extracted_data = []

    metrics_to_extract = group_config.columns
    stat_types = group_config.stat_types
    value_types = group_config.value_types

    for run in runs:
        data = {}
        # Regex to capture command line arguments
        # Group 1 (\d+): Core range (e.g., '0' from 'N:0-0').
        # Group 2 ([\w-]+): Benchmark name (e.g., 'basic-omp').
        # Group 3 (\d+): Problem size '-N'.
        # Group 4 (\d+): Optional block size '-B'.
        cmd_line_match = re.search(r'^\s*-m -g \w+ -C N:0-(\d+)\s+\./benchmark-([\w-]+)\s+-N\s+(\d+)(?:\s+-B\s+(\d+))?', run)

        if not cmd_line_match:
            print(f"Warning: Could not parse command line in {file_path}. Skipping.")
            continue

        command_line = f"likwid-perfctr {run.splitlines()[0].strip()}"
        print(f"Processing data from run: {command_line}")
        data[RUN_COMMAND] = command_line
        data[NUM_THREADS] = int(cmd_line_match.group(1)) + 1
        data[BENCHMARK] = cmd_line_match.group(2)
        data[PROBLEM_SIZE] = int(cmd_line_match.group(3))
        data[NUM_BLOCKS] = int(cmd_line_match.group(4)) if cmd_line_match.group(4) else None
        # Group 1 (\d+\.\d+): The floating-point value for the elapsed time.
        chrono_match = re.search(r'Elapsed time is : (\d+\.\d+)', run)
        data[RUNTIME_CHRONO] = float(chrono_match.group(1)) if chrono_match else None

        def get_metric(metric_name, run_text, stat_type, value_type):
            """
            Extracts a single metric from a LIKWID text block.
            It handles both multi-threaded (STAT) and single-threaded tables.
            """
            # This regex is for multi-threaded runs and finds the summary 'STAT' table.
            # - `\|\s*{re.escape(metric_name)}\s*STAT\s*\|`: Matches the metric name followed by "STAT" in a table row.
            # - `[^|]*\|`: Skips the 'Counter' column, which may or may not be present.
            # - `\s*([\d.e+-]+)\s*\|`: Group 1: Captures the 'Sum' value.
            # - `\s*([\d.e+-]+)\s*\|`: Group 2: Captures the 'Min' value.
            # - `\s*([\d.e+-]+)\s*\|`: Group 3: Captures the 'Max' value.
            # - `\s*([\d.e+-]+)\s*\|`: Group 4: Captures the 'Avg' value.
            stat_match = re.search(
                rf'\|\s*{re.escape(metric_name)}\s*STAT\s*\|[^|]*\|\s*([\d.e+-]+)\s*\|\s*([\d.e+-]+)\s*\|\s*([\d.e+-]+)\s*\|\s*([\d.e+-]+)\s*\|',
                run_text
            )
            if stat_match:
                stats = {'Sum': 1, 'Min': 2, 'Max': 3, 'Avg': 4}
                if stat_type in stats:
                    try:
                        return value_type(float(stat_match.group(stats[stat_type])))
                    except (ValueError, IndexError):
                        return None

            # This regex handles single-threaded runs for 'Event' tables that include a 'Counter' column.
            # - `\|\s*{re.escape(metric_name)}\s*\|`: Matches the metric name in a table row.
            # - `[^|]+\|`: Skips over the 'Counter' column.
            # - `\s*([\d.e+-]+)\s*\|`: Group 1: Captures the metric's value from the final column.
            event_match = re.search(rf'\|\s*{re.escape(metric_name)}\s*\|[^|]+\|\s*([\d.e+-]+)\s*\|', run_text)
            if event_match:
                try:
                    return value_type(float(event_match.group(1)))
                except (ValueError, IndexError):
                    pass  # Fall through to the next regex if this fails

            # This regex handles single-threaded runs for 'Metric' tables (no 'Counter' column).
            # - `\|\s*{re.escape(metric_name)}\s*\|`: Matches the metric name in a table row.
            # - `\s*([\d.e+-]+)\s*\|`: Group 1: Captures the metric's value directly.
            metric_match = re.search(rf'\|\s*{re.escape(metric_name)}\s*\|\s*([\d.e+-]+)\s*\|', run_text)
            if metric_match:
                try:
                    return value_type(float(metric_match.group(1)))
                except ValueError:
                    return None
            return None

        for col_name, metric_in_file in metrics_to_extract.items():
            stat = stat_types.get(col_name, 'Sum')
            v_type = value_types.get(col_name, float)
            data[col_name] = get_metric(metric_in_file, run, stat, v_type)

        extracted_data.append(data)
    return extracted_data


# --- Main script execution ---
if __name__ == "__main__":

    for group_config in output_files:
        print(f"--- Processing group: {group_config.name} ---")
        
        group_files = [f for f in files_to_parse if group_config.files_keyword in f]
        
        all_group_data = []
        for filename in group_files:
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                print(f"Created dummy directory structure: {os.path.dirname(filename)}")
                continue

            if os.path.exists(filename):
                all_group_data.extend(parse_likwid_output(filename, group_config))
            else:
                print(f"Warning: File '{filename}' not found and will be skipped.")

        if not all_group_data:
            print(f"No data extracted for group {group_config.name}.")
            continue

        df = pd.DataFrame(all_group_data)

        base_cols = [BENCHMARK, PROBLEM_SIZE, NUM_THREADS, NUM_BLOCKS, RUNTIME_CHRONO]
        metric_cols = list(group_config.columns.keys())
        output_cols = base_cols + metric_cols

        df = df[output_cols]

        int_cols = [k for k, v in group_config.value_types.items() if v == int]
        for col in int_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

        output_path = group_config.output_file
        df.to_csv(output_path, index=False)
        print(f"Successfully created '{output_path}'\n")
