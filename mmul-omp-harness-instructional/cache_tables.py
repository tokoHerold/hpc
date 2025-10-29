import pandas as pd


def analyze_cache_data(input_csv, counter_column, output_prefix):
    df = pd.read_csv(input_csv)
    df.columns = df.columns.str.strip()
    serial_df = df[df['Number of threads'] == 1].copy()

    cblas_baseline = serial_df[serial_df['Benchmark'] == 'blas'].set_index('Problem Size')[counter_column]
    result_df = pd.DataFrame(index=cblas_baseline.index)

    basic_data = serial_df[serial_df['Benchmark'] == 'basic-omp'].set_index('Problem Size')[counter_column]
    blocked_df = serial_df[serial_df['Benchmark'] == 'blocked-omp']
    blocked_b4_data = blocked_df[blocked_df['Number of blocks'] == 4.0].set_index('Problem Size')[counter_column]
    blocked_b16_data = blocked_df[blocked_df['Number of blocks'] == 16.0].set_index('Problem Size')[counter_column]
    result_df['CBLAS'] = cblas_baseline / cblas_baseline
    result_df['basic'] = basic_data / cblas_baseline
    result_df['blocked B4'] = blocked_b4_data / cblas_baseline
    result_df['blocked B16'] = blocked_b16_data / cblas_baseline

    csv_output_path = f'{output_prefix}_normalized.csv'
    result_df.to_csv(csv_output_path)

    latex_string = result_df.to_latex(float_format="%.2f")
    print(f"--- {output_prefix.upper()} Access (Normalized by CBLAS) ---")
    print(result_df)
    print(f"--- Latex Output: ---\n{latex_string}")
    print(f"\nCSV table successfully saved to '{csv_output_path}'")


# --- L2 Cache Analysis ---
analyze_cache_data(
    input_csv='data/l2_cache_data.csv',
    counter_column='L2 accesses',
    output_prefix='data/l2_cache'
)

# --- L3 Cache Analysis ---
analyze_cache_data(
    input_csv='data/l3_cache_data.csv',
    counter_column='L3_ACCESS_ALL_TYPES',
    output_prefix='data/l3_cache'
)

# --- Instruction Count Analysis ---
analyze_cache_data(
    input_csv='data/flops_dp_data.csv',
    counter_column='Instruction Count',
    output_prefix='data/instruction_count'
)
