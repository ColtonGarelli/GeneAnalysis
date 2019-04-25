"""
Functions to be used by MVC to create heatmaps of data
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial import distance
import plotly.graph_objs as go
import plotly as py
import plotly.offline as offline
from scipy.cluster.hierarchy import linkage



def sns_heatmap(df: pd.DataFrame):
    df.set_index('symbol')
    sns.clustermap(df)
    plt.show()


def plotly_heatmap(df: pd.DataFrame):

    cols = [col for col in df if col not in ['symbol', 'uniprot_id', 'avg']]
    short_cols = [col[0:20] for col in cols]
    print(short_cols)
    short_cols = [short_cols[i] + str(i) for i in range(1, len(short_cols), 1)]
    print(short_cols)
    data_dist = distance.pdist(df[cols].values.transpose())

    data = py.graph_objs.Heatmap(z=distance.squareform(data_dist), colorscale='YlGnBu', x=short_cols, y=short_cols)
    layout = go.Layout(title='Transcription profiling of human brain samples', autosize=False,
                       margin=go.layout.Margin(l=200, b=200, pad=4), xaxis=go.layout.XAxis(showgrid=False, dtick=1),
                       yaxis=go.layout.YAxis(showgrid=False, dtick=1))
    fig = go.Figure(data=data, layout=layout)
    py.plotly.plot(fig, width=900, height=900)

