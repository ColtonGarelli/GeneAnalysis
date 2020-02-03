"""
Functions to create heatmaps of gene expression data
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as colors
import numpy as np
# from scipy.spatial import distance
# import plotly.graph_objs as go
# import plotly as py
# import plotly.offline as offline
# from scipy.cluster.hierarchy import linkage


def sns_clustermap(df: pd.DataFrame, title=None, z=False, genes_of_interest: list = None, show_all=True, labels=True) \
        -> sns.matrix.ClusterGrid:
    """Create a clustered heatmap of gene expression data.

    Creates a clustered heatmap from a DataFrame of expression data using the seaborn.clustermap function. There is an
    option to insert a title, use z-scored values, only show certain genes, and to show gene labels. If show all and
    labels are true and genes_of_interest != None, a map will be generated only showing labels for genes of interest.
    If show_all is False, a map of only genes_of_interest will be generated.

    Notes:
        - **Important**: A dataframe passed in MUST contain at least two columns and two rows.
        - probably something i'll think of later
        - Seaborn is a thin wrapper around matplotlib.

    Args:
        df: a DataFrame containing only gene expression data from multiple samples to compare.
        title: A title for the clustermap
        z: calculate z-score across genes for all samples in df. Default is False (don't use z-score).
            if z=True then z_score = 0
        genes_of_interest: If show_all=True, only labels for genes in genes_of_interest are displayed. If show_all=False
            a map is generated only using genes in genes_of_interest
        labels: Show labels (True) or hide (False). Default is True
        show_all: Generate map of all genes, or only genes in genes_of_interest iff (if and only if)
        genes_of_interest != None. Otherwise has no effect

    Returns:
        A clustered heatmap (ClusterGrid object)

    """
    if df.isnull().values.any().any():
        df.dropna(axis=0, inplace=True)
    matplotlib.use('TkAgg')
    if title is None:
        title = "Clustermap"
    # genes_of_interest = ['CXCL9', 'CXCL10', 'CXCL11']
    # new_df = pd.DataFrame(index=genes_of_interest)
    # for i in df.columns.to_list():
    #     new_df.merge(df[df[i].isin(genes_of_interest)])
    # TODO: Zscore over rows or cols (probably rows...plot represents # of deviations
    if genes_of_interest is None:
        heatmap = sns.clustermap(df, row_cluster=True, col_cluster=True, yticklabels=1, cbar_kws={'label': "log$_2$FC"},
                                  cmap='viridis', center=0, z_score=0)
    else:
        heatmap = sns.clustermap(df.loc[genes_of_interest,:], row_cluster=True, col_cluster=True, yticklabels=1, cbar_kws={'label': "log$_2$FC"},
                                 cmap='viridis', center=0, z_score=0)

    newyticklabels = [l if not i % 2 else ('----------------' + l) for i, l in enumerate([label.get_text() for label in heatmap.ax_heatmap.yaxis.get_ticklabels()])]
    heatmap.ax_heatmap.yaxis.set_ticklabels(newyticklabels)
    plt.setp(heatmap.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, wrap=True)
    heatmap.ax_heatmap.yaxis.label.set_size(10)
    heatmap.fig.suptitle(title).set_size(20)

    if df.shape[0] > 50:
        heatmap.fig.set_size_inches(20, 20)
    return heatmap


def simple_clustermap(df, gene_clust: bool = False, sample_clust: bool = False) -> sns.matrix.ClusterGrid:
    """Create a heatmap with no labels.

    Generate a 'naked' heatmap with no labels and options for no clustering. Main utility is for modifying in Adobe
    Illustrator or LibreOffice Draw.

    Args:
        df: a DataFrame containing gene expression data to plot
        gene_clust: Boolean whether to perform hierarchical clustering on genes. Default is False (no clustering)
        sample_clust: Boolean whether to perform hierarchical clustering on samples. Default is False

    Returns:
        A ClusterGrid object which can be displayed (maplotlib.pyplot.show()) or saved (ClusterGrid.savefig(path))

    """
    hm = sns.clustermap(df, row_cluster=gene_clust, col_cluster=sample_clust, z_score=0, cmap='viridis')
    hm.ax_heatmap.yaxis.set_visible(False)
    hm.ax_heatmap.xaxis.set_visible(False)
    # newyticklabels = [l if not i % 2 else ('----------------' + l) for i, l in enumerate([label.get_text() for label in heatmap.ax_heatmap.yaxis.get_ticklabels()])]
    # heatmap.ax_heatmap.yaxis.set_ticklabels(newyticklabels)
    # plt.setp(heatmap.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, wrap=True)
    return hm


def sns_heatmap(df:pd.DataFrame, colormap=None, title="Title"):
    """Creates a regular old boring heatmap. This is basically the same as the simple_clustermap function

    TODO: determine whether this function is worth updating (i.e. labels, title, etc.) or whether it should be archived.
    Args:
        df:

    Returns:

    """
    if colormap is None:
        colormap=plt.cm.get_cmap('viridis')
    plt.figure(figsize=(20,20))
    ax = plt.axes()
    heatmap = sns.heatmap(df, robust=True, cmap=colormap, annot=True, square=True, ax=ax)
    ax.set_title(label=title)
    return heatmap


class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))


