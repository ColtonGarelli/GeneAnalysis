"""
Functions to be used by MVC to create heatmaps of data
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# from scipy.spatial import distance
# import plotly.graph_objs as go
# import plotly as py
# import plotly.offline as offline
# from scipy.cluster.hierarchy import linkage


def sns_clustermap(df: pd.DataFrame, title=None):
    if title is None:
        title = "Clustermap"
    # cmap = sns.diverging_palette(as_cmap=True, h_pos=10, h_neg=240, n=10, center="light", sep=2)
    cmap = sns.light_palette(color="r", input="rgb", as_cmap=True)
    genes_of_interest = ['CXCL9', 'CXCL10', 'CXCL11']
    new_df = pd.DataFrame(index=genes_of_interest)
    # for i in df.columns.to_list():
    #     new_df.merge(df[df[i].isin(genes_of_interest)])
    # TODO: Zscore over rows or cols (probably rows...plot represents # of deviations
    heatmap = sns.clustermap(df, row_cluster=True, col_cluster=True, yticklabels=1, cbar_kws={'label': "log$_2$FC"},
                             z_score=0, cmap='viridis')
    # y_labels = heatmap.ax_heatmap.yaxis.get_majorticklabels()
    newyticklabels = [l if not i % 2 else ('----------------' + l) for i, l in enumerate([label.get_text() for label in heatmap.ax_heatmap.yaxis.get_ticklabels()])]
    heatmap.ax_heatmap.yaxis.set_ticklabels(newyticklabels)
    plt.setp(heatmap.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, wrap=True)
    heatmap.ax_heatmap.yaxis.label.set_size(10)
    heatmap.fig.suptitle(title).set_size(20)

    if df.shape[0] > 50:
        heatmap.fig.set_size_inches(20, 20)
    return heatmap


def simple_clustermap(df):
    heatmap = sns.clustermap(df, row_cluster=False, col_cluster=False   )
    heatmap.ax_heatmap.yaxis.set_visible(False)
    heatmap.ax_heatmap.xaxis.set_visible(False)
    # newyticklabels = [l if not i % 2 else ('----------------' + l) for i, l in enumerate([label.get_text() for label in heatmap.ax_heatmap.yaxis.get_ticklabels()])]
    # heatmap.ax_heatmap.yaxis.set_ticklabels(newyticklabels)
    # plt.setp(heatmap.ax_heatmap.yaxis.get_majorticklabels(), rotation=0, wrap=True)
    heatmap.savefig('simple_testing.png')


def sns_heatmap(df:pd.DataFrame):
    """

    Args:
        df:

    Returns:

    """
    plt.figure(figsize=(20,20))
    heatmap = sns.heatmap(df, robust=True)
    plt.show()
    return heatmap
    # heatmap.savefig('testingheatmap.png')


# def plotly_heatmap(df: pd.DataFrame):
#
#     cols = [col for col in df if col not in ['symbol', 'uniprot_id', 'avg']]
#     short_cols = [col[0:20] for col in cols]
#     print(short_cols)
#     short_cols = [short_cols[i] + str(i) for i in range(1, len(short_cols), 1)]
#     print(short_cols)
#     data_dist = distance.pdist(df[cols].values.transpose())
#
#     data = py.graph_objs.Heatmap(z=distance.squareform(data_dist), colorscale='YlGnBu', x=short_cols, y=short_cols)
#     layout = go.Layout(title='Transcription profiling of human brain samples', autosize=False,
#                        margin=go.layout.Margin(l=200, b=200, pad=4), xaxis=go.layout.XAxis(showgrid=False, dtick=1),
#                        yaxis=go.layout.YAxis(showgrid=False, dtick=1))
#     fig = go.Figure(data=data, layout=layout)
#     py.plotly.plot(fig, width=900, height=900)

