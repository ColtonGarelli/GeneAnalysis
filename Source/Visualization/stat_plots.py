import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster import hierarchy
import numpy as np
import plotly.graph_objects as go




def dendrogram(df: pd.DataFrame, groups: dict):
    """
    References: https://python-graph-gallery.com/401-customised-dendrogram/
    Args:
        df:

    Returns:

    """
    # del df.index.name
    # working = df.copy().to_numpy()
    dflt_col = "#808080"  # Unclustered gray
    D_leaf_colors = {"attr_1": dflt_col,

                     "attr_4": "#B061FF",  # Cluster 1 indigo
                     "attr_5": "#B061FF",
                     "attr_2": "#B061FF",
                     "attr_8": "#B061FF",
                     "attr_6": "#B061FF",
                     "attr_7": "#B061FF",

                     "attr_0": "#61ffff",  # Cluster 2 cyan
                     "attr_3": "#61ffff",
                     "attr_9": "#61ffff",
                     "attr_10": "#61ffff",
                     "attr_11": "#61ffff",
                     "attr_12": "#61ffff"

                     }

    # notes:
    # * rows in Z correspond to "inverted U" links that connect clusters
    # * rows are ordered by increasing distance
    # * if the colors of the connected clusters match, use that color for link

    Z = hierarchy.linkage(df.T, 'ward', metric='euclidean')
    DF_dism = 1 - np.abs(df.corr())
    link_cols = {}
    for i, i12 in enumerate(Z[:, :2].astype(int)):
        c1, c2 = (link_cols[x] if x > len(Z) else D_leaf_colors["attr_%d" % x]
                  for x in i12)
        link_cols[i + 1 + len(Z)] = c1 if c1 == c2 else dflt_col
    plot = hierarchy.dendrogram(Z, labels=DF_dism.index, color_threshold=None,
                                leaf_font_size=12, leaf_rotation=45, link_color_func=lambda x: link_cols[x])

    # plot = hierarchy.dendrogram(Z, leaf_rotation=90, leaf_font_size=8,
    #                             color_threshold=2.5)
    plt.tight_layout()
    return plot


def density_plot(df: pd.DataFrame, batch: dict = None, kind: str = 'density'):
    """Create a density plot from a DataFrame

    Plot density of all samples in df. All columns should be of the same data (e.g. log2fc, read counts, p-values.
    Density plots can be used to determine presence of batch effects

    Args:
        df: a DataFrame containing sample data
        batch: a dictionary mapping each batch to a list of experiments

    Returns:
        A density plot

    """
    plot_types = {'density', 'kde'}
    # fig = plt.figure(figsize=(10,10))

    if kind not in plot_types:
        raise ValueError("this function is only intended for kde and density plots. Please pass 'kde' or 'density' to param 'kind'")
    # fig, ax = plt.subplots(4, 4)
    if batch is None:
        plot = df.plot(kind=kind,legend=True)
    else:
        num_colors = len(batch)
        labels = ['Batch {}'.format(i + 1) for i in range(num_colors)]
        cm = plt.get_cmap('gist_rainbow')
        colors = [cm(1. * i / num_colors) for i in range(num_colors)]
        for k, v in [*batch.items()]:
            count = k
            for i in df[[*v]]:
                plot = sns.distplot(df[i], color=colors[k], kde=True, hist=False, label=(labels[k] if count == k else None))
                count += 1
        # g = sns.FacetGrid(df, col=[*batch.values()], hue=[*batch.keys()], palette="Set1")
        #
        # g = (g.map(sns.distplot, , hist=False, rug=True))
        # plot = df.plot(kind=kind, legend=True, c=colors)
    # plt.xlim(-10000, 10000)
    # plt.xlim(df.values.min(), df.values.max()+1)
    plt.legend().remove()
    plt.tight_layout()
    return plot


def read_count_bar(df: pd.DataFrame, cols: list, gene: str or list):
    """

    Args:
        df: dataframe containing genes, samples, and corresponding counts for each coordinate
            should be formatted with genes as index and samples as columns
        cols: a list of columns to include in the bar graph
        gene: the gene for which counts will be plotted

    Returns:

    """

    bar = sns.barplot(data=df[cols].T[gene].T, ci=None,
                    palette='rainbow')
    bar.set_xticklabels(labels=bar.get_xticklabels(), rotation=40)
    bar.set_title("Read counts {}".format(''.join([str(g) for g in gene])))
    plt.tight_layout()

    return bar

