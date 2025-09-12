import pandas as pd
import matplotlib.pyplot as plt


def plot(title, path, output_name, xlabel, ylabel, ymodifier=1.0):
    df = pd.read_csv(path, comment="#")
    print(df)

    var_names = list(df.columns)

    print("var names =", var_names)

# split the df into individual vars
# assumption: column order - 0=problem size, 1=blas time, 2=basic time

    problem_sizes = df[var_names[0]].values.tolist()
    code1_metric = (df[var_names[1]] * ymodifier).values.tolist()
    code2_metric = (df[var_names[2]] * ymodifier).values.tolist()
    code3_metric = (df[var_names[3]] * ymodifier).values.tolist()

    plt.figure()

    plt.title(title)

    xlocs = [i for i in range(len(problem_sizes))]

    plt.xticks(xlocs, [rf"${problem_size // (1 << 20)} \cdot 2^{{20}}$" for problem_size in problem_sizes])

    plt.plot(code1_metric, "r-o")
    plt.plot(code2_metric, "b-x")
    plt.plot(code3_metric, "g-^")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    varNames = [var_names[1], var_names[2], var_names[3]]
    plt.legend(varNames, loc="best")

    plt.grid(axis='both')

    # save the figure before trying to show the plot
    plt.savefig(output_name, dpi=300, format='pdf')
    # plt.show()


plot("Performance Measure: FLOP/s", "data/mflops.csv", "flops.pdf", "Problem Size", "MFLOP/s")
plot("Performance Measure: Memory Bandwidth", "data/bandwidth.csv", "bandwidth.pdf", "Problem Size", "Utilized Bandwidth [%]", 100)
plot("Performance Measure: Memory Latency", "data/latency.csv", "latency.pdf", "Problem Size", "Average Acceess Latency [ms]", 100)
# plot("MyTitle", "sample_data_3vars.csv", "Problem Sizes", "runtime")
