import pandas as pd
import matplotlib.pyplot as plt


def density_plot(df: pd.DataFrame, batch: dict = None):
    """Create a density plot from a DataFrame

    Plot density of all samples in df. All columns should be of the same data (e.g. log2fc, read counts, p-values.
    Density plots can be used to determine presence of batch effects

    Args:
        df: a DataFrame containing sample data
        batch: a dictionary mapping each batch to a list of experiments

    Returns:
        A density plot

    """
    fig, ax = plt.subplots(4, 4)
    if batch is None:
        df.plot(kind='density', legend=True)
    else:
        num_colors = len(batch)
        cm = plt.get_cmap('gist_rainbow')
        colors = [cm(1. * i / num_colors) for i in range(num_colors)]
        for k in batch.keys():
            df[batch[k]].plot(kind='density', legend=True, c=colors[k])
    return fig, ax


def plot_pca(df, rows):
    """Plots PCA data on a scatter plot where x = PC1 and y = PC2

    Plot the first two principal components of PC analyzed data on a scattermap. Plotting PCs can be used as a measure
    for batch effect or correction. PCA can also be used to determine correlation of a list of interest genes.

    Notes:
        - Perform PCA on specific genes to utilize PCA for non-batch analysis

    Args:
        df: a DataFrame containing PC analyzed data to plot on a scatter plot (x = PC1, y= PC2)
        rows: A dictionary that maps each sample or batch to each PC data experiment/sample in df.

    Returns:
        Figure and Axes objects

    """
    cdict = dict()
    marker = dict()
    markers = ['o', 'v', 's', 'd', 'P', '+', '8', '*', "X", 'x', "D", 'd', 7, 6, "$:-)$", "$:-($", "$=$", "$$$"]
    num_colors = len(rows)
    cm = plt.get_cmap('gist_rainbow')
    colors = [cm(1. * i / num_colors) for i in range(num_colors)]

    fig, ax = plt.subplots(figsize=(10, 8))
    labels = df.index.to_list()
    for i in [*rows.keys()]:
        cdict.update({i: colors[i]})
        marker.update({i: markers[i]})
    for k, v in rows.items():
        ax.scatter(x=df.loc[v][0], y=df.loc[v][1], c=[cdict.get(k)], marker=marker.get(k), label=labels[k-1],
                   s=55)
        plt.xlabel("Principal Component 1", fontsize=15)
        plt.ylabel("Principal Component 2", fontsize=15)

    return fig, ax
