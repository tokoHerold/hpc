import itertools
import pandas as pd
import matplotlib.pyplot as plt


def plot(
        title: str,
        df: pd.DataFrame, 
        output_name: str,
        xlabel: str,
        ylabel: str,
        legend_prefix="",
        ymodifier=1.0,
        logscale="",
        log_base_x=10.0,
        log_base_y=10.0,
        x_coords=None
        ):
    """
    Generates and saves a plot from a pandas DataFrame.

    This function takes a DataFrame and plots its columns as separate lines.
    It is designed to be flexible for various types of plots, with options for
    logarithmic scaling on either axis.

    Args:
        title (str): The title of the plot.
        df (pd.DataFrame): The DataFrame to plot. The index is used for the x-axis,
                           and each column is plotted as a separate series.
        output_name (str): The filename for the saved plot (e.g., 'my_plot.pdf').
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        ymodifier (float, optional): A factor to multiply the y-values by. Defaults to 1.0.
        logscale (str, optional): A string containing 'x' or 'y' (or both) to
                                  set the corresponding axes to a log scale. Defaults to "".
        log_base_x (int, optional): The base for the logarithmic x-axis. Defaults to 2.
        log_base_y (int, optional): The base for the logarithmic y-axis. Defaults to 10.
        legend_prefix (str, optional): A prefix to add to each legend entry. Defaults to "".
        x_cords (list[int], optional): Spacing for ticks on the x-axis.
    """
    print(f"-= Plotting {title.split("\n")[0]} =-")
    print(df)

    var_names = list(df.columns)
    print("Detected series: ", [f"{legend_prefix}{x}" for x in var_names])

    # Split the df into individual vars
    # problem_sizes = df[var_names[0]].values.tolist()
    x_labels = df.index.tolist()

    # Prepare metrics for all columns except the first one
    metrics = [(df[var_names[i]] * ymodifier).values.tolist() for i in range(len(var_names))]

    plt.figure()
    plt.title(title)

    xlocs = x_coords if x_coords is not None else [i for i in range(len(x_labels))]
    plt.xticks(xlocs, [f"${problem_size}$" for problem_size in x_labels])

    # Define a list of markers to use
    markers = ['o', 'x', '^', 's', 'D', '*', 'P', 'H']
    marker_cycle = itertools.cycle(markers)

    # Plot each metric with a different marker
    for i, metric in enumerate(metrics):
        plt.plot(xlocs, metric, marker=next(marker_cycle), label=f"{legend_prefix}{var_names[i]}")

    if 'y' in logscale:
        plt.yscale("log", base=log_base_y)
        ylabel += " (logarithmic)"

    if 'x' in logscale:
        plt.xscale("log", base=log_base_x)
        # ylabel += " (logarithmic)"

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.legend(loc="best")
    plt.grid(axis='both')

    # Save the figure before trying to show the plot
    plt.savefig(output_name, dpi=300, format='pdf')
    # plt.show()


# plot("FLOP/s of Basic vs. LibSci BLAS DGEMM:\nPerlmutter CPU Node, -O3, 64-bit floats",
#      "data/mflops_basic.csv",
#      "basic.pdf",
#      "Problem Size (n)",
#      "MFLOP/s")

flops_df = pd.read_csv("data/flops_dp_data.csv")

# -= Speedup in basic plot =-
basic_df = flops_df[flops_df['Benchmark'] == 'basic-omp'].copy()
# Sort values to by Problem Size and Number of threads...
basic_df = basic_df.sort_values(by=['Problem Size', 'Number of threads'])
# .. so we can get the baseline runtime (first entry for each problem size)
baseline_runtime = basic_df.groupby('Problem Size')['Runtime (RDTSC)'].transform('first')
basic_df['Speedup'] = baseline_runtime / basic_df['Runtime (RDTSC)']
speedup_df = basic_df.pivot(index='Problem Size', columns='Number of threads', values='Speedup')
speedup_df.drop(columns=1, inplace=True)

plot("Speedup of Basic vs. LibSci BLAS DGEMM:\nPerlmutter CPU Node, -O3, -march=native, 64-bit floats",
     speedup_df,
     "basic_speedup.pdf",
     "Problem Size (n)",
     "Speedup",
     legend_prefix='p=',
     x_coords=[0, 1, 3],
     )
