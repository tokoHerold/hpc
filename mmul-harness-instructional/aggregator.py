import pandas as pd

problems = ["basic", "blocked", "blas"]
input_dfs = [pd.read_csv(f"data/{problem}.csv") for problem in problems]

# Compare basic with blas
basic_blas = pd.DataFrame()
basic_blas["N"] = input_dfs[0]["N"]

basic_blas["basic"] = input_dfs[0]["N"]**3 / input_dfs[0]["runtime"] / 10**6
basic_blas["blas"] = input_dfs[2]["N"]**3 / input_dfs[2]["runtime"] / 10**6

basic_blas.to_csv("data/mflops_basic.csv", index=False)

# Compare blocked with blas
blocked_blas = pd.DataFrame()
blocked_blas["N"] = input_dfs[0]["N"]
vars = input_dfs[1].groupby("block_size")
for key in vars.groups.keys():
    group = vars.get_group(key)
    values = (group["N"]**3 / group["runtime"] / 10**6).reset_index(drop=True)
    blocked_blas[f"b = {key}"] = values

blocked_blas["blas"] = input_dfs[2]["N"]**3 / input_dfs[2]["runtime"] / 10**6
blocked_blas.to_csv("data/mflops_blocked.csv", index=False)
