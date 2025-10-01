import pandas as pd

problems = ["basic", "vector", "blas"] + [f"openmp-{n}" for n in (1, 4, 16, 64)]
input_dfs = [pd.read_csv(f"data/{problem}.csv") for problem in problems]

n_to_flops = lambda n: 2*n**2

# Compare basic with vecotrized and blas
serial = pd.DataFrame()
serial["N"] = input_dfs[0]["N"]

serial["basic"] = n_to_flops(input_dfs[0]["N"]) / input_dfs[0]["t"] / 10**6
serial["vectorized"] = n_to_flops(input_dfs[1]["N"]) / input_dfs[1]["t"] / 10**6
serial["blas"] = n_to_flops(input_dfs[2]["N"]) / input_dfs[2]["t"] / 10**6

serial.to_csv("data/mflops_serial.csv", index=False)


# Compare parallel to blas
parallel = pd.DataFrame()
parallel["N"] = input_dfs[0]["N"]
parallel["blas"] = n_to_flops(input_dfs[2]["N"]) / input_dfs[2]["t"] / 10**6
for i in range(3, 7):
    parallel[problems[i]] = n_to_flops(input_dfs[i]["N"]) / input_dfs[i]["t"] / 10**6
parallel.to_csv("data/mflops_parallel.csv", index=False)

# Calculate speedup
speedup = pd.DataFrame()
speedup["N"] = input_dfs[0]["N"]
for i in range(3, 7):
    speedup[problems[i]] = input_dfs[2]["t"] / input_dfs[i]["t"] 

speedup.to_csv("data/speedup.csv", index=False)
