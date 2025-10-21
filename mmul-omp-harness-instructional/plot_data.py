import itertools
import pandas as pd
import matplotlib.pyplot as plt


def plot(
        title: str,
        dfs: list[pd.DataFrame] | pd.DataFrame,
        output_name: str,
        xlabel: str,
        ylabel: str,
        legend_prefix: str | list[str] = "",
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
        dfs (pd.DataFrame | list[pd.DataFrame]): The DataFrame(s) to plot. The index is used for the x-axis,
                           and each column is plotted as a separate series. If a list is passed, different
                           DataFrames will use different line styles.
        output_name (str): The filename for the saved plot (e.g., 'my_plot.pdf').
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        ymodifier (float, optional): A factor to multiply the y-values by. Defaults to 1.0.
        logscale (str, optional): A string containing 'x' or 'y' (or both) to
                                  set the corresponding axes to a log scale. Defaults to "".
        log_base_x (int, optional): The base for the logarithmic x-axis. Defaults to 2.
        log_base_y (int, optional): The base for the logarithmic y-axis. Defaults to 10.
        legend_prefix (str | list[str], optional): A prefix to add to each legend entry of each series.
                                                    Defaults to "".
        x_cords (list[int], optional): Spacing for ticks on the x-axis.
    """
    if type(dfs) is not list:
        if type(dfs) is not pd.DataFrame:
            print(f"Error: Expected dataframe but got {type()}")
        dfs = [dfs]

    if type(legend_prefix) is not list:
        legend_prefix = [legend_prefix] * len(dfs)
    assert len(dfs) == len(legend_prefix), "Length of data frames must be equal to legend prefixes!"

    # Define cycles for visual properties
    linestyles = ['-', '--', ':', '-.']
    markers = ['o', 'x', '^', 's', 'D', '*', 'P', 'H']
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    base_df = dfs[0]
    print(f"-= Plotting {title.split("\n")[0]} =-")
    x_labels = base_df.index.tolist()

    # Prepare metrics for all columns except the first one
    # metrics = [(base_df[var_names[i]] * ymodifier).values.tolist() for i in range(len(var_names))]

    plt.figure()
    plt.title(title)

    xlocs = x_coords if x_coords is not None else [i for i in range(len(x_labels))]
    plt.xticks(xlocs, [f"${problem_size}$" for problem_size in x_labels])

    # Define a list of markers to use
    # marker_cycle = itertools.cycle(markers)
    for df_idx, df in enumerate(dfs):
        print(df)
        linestyle = linestyles[df_idx % len(linestyles)]
        var_names = list(df.columns)
        print("Detected series: ", [f"{legend_prefix[df_idx]}{x}" for x in var_names])
        print("------==========================================------")

        for metric_idx, var_name in enumerate(var_names):
            metric = (df[var_name] * ymodifier).values.tolist()
            color = colors[metric_idx % len(colors)]
            marker = markers[metric_idx % len(markers)]

            label = f"{legend_prefix[df_idx]}{var_name}"
            plt.plot(xlocs, metric, marker=marker, color=color, linestyle=linestyle, label=label)

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
    print(f"Saved plot to {output_name}.pdf")
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

plot("Speedup of Basic OMP vs Sequential DGEMM:\nPerlmutter CPU Node, -O3, -march=native, 64-bit floats",
     speedup_df,
     "basic_speedup.pdf",
     "Problem Size (n)",
     "Speedup",
     legend_prefix='p=',
     x_coords=[0, 1, 3],
     )


blocked_df = flops_df[flops_df['Benchmark'] == 'blocked-omp'].copy()
blocked_df = blocked_df.sort_values(by=['Problem Size', 'Number of threads'])
blocked_groups = blocked_df.groupby('Number of blocks')
df_bf4 = blocked_groups.get_group(4.0).copy()
df_bf16 = blocked_groups.get_group(16.0).copy()
baseline_bf4 = df_bf4[df_bf4['Number of threads'] == 1].set_index('Problem Size')['Runtime (RDTSC)']
df_bf4['Speedup'] = df_bf4['Problem Size'].map(baseline_bf4) / df_bf4['Runtime (RDTSC)']
speedup_bf4 = df_bf4.pivot(index='Problem Size', columns='Number of threads', values='Speedup')
baseline_bf16 = df_bf16[df_bf16['Number of threads'] == 1].set_index('Problem Size')['Runtime (RDTSC)']
df_bf16['Speedup'] = df_bf16['Problem Size'].map(baseline_bf16) / df_bf16['Runtime (RDTSC)']
speedup_bf16 = df_bf16.pivot(index='Problem Size', columns='Number of threads', values='Speedup')
# blocked_df['Speedup'] = baseline_runtime / blocked_df['Runtime (RDTSC)']
# speedup_df = blocked_df.pivot(index='Problem Size', columns='Number of threads', values='Speedup')
speedup_bf4.drop(columns=1, inplace=True)
speedup_bf16.drop(columns=1, inplace=True)
plot("Speedup of Blocked OMP vs Sequential DGEMM:\nPerlmutter CPU Node, -O3, -march=native, 64-bit floats",
     [speedup_bf4, speedup_bf16],
     "blocked_speedup.pdf",
     "Problem Size (n)",
     "Speedup",
     legend_prefix=['b=4, p=', 'b=16, p='],
     x_coords=[0, 1, 3],
     )
