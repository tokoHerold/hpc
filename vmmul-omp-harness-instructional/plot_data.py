import itertools
import pandas as pd
import matplotlib.pyplot as plt


def plot(
        title: str,  # Title of the plot
        path: str,  # Path to the data file
        output_name: str,  # Name under which the plot shall be saved
        xlabel: str,  # Label for the horizontal axis
        ylabel: str,  # Label for the vertical axis
        ymodifier=1.0,  # Multiplicator for values on the y-axis
        logscale=False,  # If the y-axis should be in logscale
        ylims: tuple[int] = None  # A list containing the lower and upper limits for y axis
):
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

    if ylims is not None:
        assert len(ylims) == 2, "ylims must be a tuple with 2 elements"
        plt.ylim(ylims)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.legend(loc="best")
    plt.grid(axis='both')

    # Save the figure before trying to show the plot
    plt.savefig(output_name, dpi=300, format='pdf')
    # plt.show()


plot("FLOP/s of Basic vs. Vectorized vs. LibSci BLAS VMMUL:\nPerlmutter CPU Node, 64-bit floats",
     "data/mflops_serial.csv",
     "serial.pdf",
     "Problem Size (n)",
     "MFLOP/s")

plot("Speedup of Parallel relativ to Basic VMMUL:\nPerlmutter CPU Node, -O1, -march=native, 64-bit floats",
     "data/speedup.csv",
     "parallel.pdf",
     "Problem Size (n)",
     "Speedup",
     )

plot("FLOP/s of serial BLAS vs. Best Parallel OMP VMMUL:\nPerlmutter CPU Node, 64-bit floats",
     "data/mflops_parallel.csv",
     "best.pdf",
     "Problem Size (n)",
     "MFLOP/s",
     )
