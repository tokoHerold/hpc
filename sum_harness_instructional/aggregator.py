import pandas as pd

problems = ["direct", "vector", "indirect"]
input_dfs = [pd.read_csv(f"data/{problem}.csv") for problem in problems]

# FLOPS/s
flops_df = pd.DataFrame()
flops_df["N"] = input_dfs[0]["N"]

for problem, df in zip(problems, input_dfs):
    # FLOPS / time
    flops_df[problem] = df["N"] / df["runtime"] / 10**9

flops_df.to_csv("data/gflops.csv")


# Memory Bandwidth
bandwidth_df = pd.DataFrame()
bandwidth_df["N"] = input_dfs[0]["N"]
THEORETICAL_BANDWIDTH = 204.8e9  # 204.8 GB/s

for problem, df in zip(problems, input_dfs):
    # Bytes moved / time / theo. max. bandwidth
    bandwidth_df[problem] = df["N"] * 4 / df["runtime"] / THEORETICAL_BANDWIDTH

bandwidth_df.to_csv("data/bandwidth.csv")


# Average Memory Latencay in nanoseconds
latency_df = pd.DataFrame()
latency_df["N"] = input_dfs[0]["N"]

# latency_df["direct"] = [0.0] * len(input_dfs[0]["N"])
latency_df["vector"] = (input_dfs[1]["runtime"] - input_dfs[0]["runtime"]).clip(lower=0) / latency_df["N"] * 10e9
latency_df["indirect"] = (input_dfs[2]["runtime"] - input_dfs[0]["runtime"]).clip(lower=0) / latency_df["N"] * 10e9
latency_df.to_csv("data/latency.csv")
