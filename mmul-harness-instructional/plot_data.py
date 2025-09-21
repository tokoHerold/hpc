import itertools
import pandas as pd
import matplotlib.pyplot as plt


def plot(title, path, output_name, xlabel, ylabel, ymodifier=1.0, logscale=False):
    df = pd.read_csv(path, comment="#")
    print(df)

    var_names = list(df.columns)
    print("var names =", var_names)

    # Split the df into individual vars
    problem_sizes = df[var_names[0]].values.tolist()

    # Prepare metrics for all columns except the first one
    metrics = [(df[var_names[i]] * ymodifier).values.tolist() for i in range(1, len(var_names))]

    plt.figure()
    plt.title(title)

    xlocs = [i for i in range(len(problem_sizes))]
    plt.xticks(xlocs, [f"${problem_size}$" for problem_size in problem_sizes])

    # Define a list of markers to use
    markers = ['o', 'x', '^', 's', 'D', '*', 'P', 'H']
    marker_cycle = itertools.cycle(markers)

    # Plot each metric with a different marker
    for i, metric in enumerate(metrics):
        plt.plot(metric, marker=next(marker_cycle), label=var_names[i + 1])

    if logscale:
        plt.yscale("log")
        ylabel += " (logarithmic)"

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.legend(loc="best")
    plt.grid(axis='both')

    # Save the figure before trying to show the plot
    plt.savefig(output_name, dpi=300, format='pdf')
    # plt.show()


plot("FLOP/s of Basic vs. LibSci BLAS DGEMM:\nPerlmutter CPU Node, -O3, 64-bit floats",
     "data/mflops_basic.csv",
     "basic.pdf",
     "Problem Size (n)",
     "MFLOP/s")

plot("FLOP/s of BMMCO vs. LibSci BLAS DGEMM:\nPerlmutter CPU Node, -O3, 64-bit floats",
     "data/mflops_blocked.csv",
     "blocked.pdf",
     "Problem Size (n)",
     "MFLOP/s")
