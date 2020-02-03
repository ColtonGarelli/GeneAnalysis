from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go
import chart_studio.tools

# for offline graphs
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


def plotly_3d_scatter(df, batch: bool = False):
    markers, colors = construct_point(df)
    # cdict = dict(zip(rows.keys(), colors))
    # marker = dict(zip(rows.keys(), markers))
    if batch:
        # consider changing batch to 'group' for generic grouping
        labels = ['Batch {}'.format(i+1) for i in range(len(colors))]
    else:
        labels = df.index.to_list()
    x = df.T.loc['Principal Component 1']
    y = df.T.loc['Principal Component 2']
    z = df.T.loc['Principal Component 3']
    fig = go.Figure(go.Scatter3d(x=x, y=y,z=z, mode='markers', text=labels))
    fig.update_traces(textposition='top center')
    fig.update_layout(title_text='3D PCA of LPP Nanostring by groups')
    fig.update_layout(scene=dict(
        xaxis_title='Principal Component 1',
        yaxis_title='Principal Component 2',
        zaxis_title='Principal Component 3'))
    return fig


# TODO: save username and key to file and ignore file for github
def save_online_interactive(fig: go.Figure, name):
    """
    Save an interactive plotly plot on my account
    Args:
        fig: a go.Figure object to save online
        name: a name for the plot

    """
    from chart_studio.plotly import plot
    if chart_studio.tools.get_credentials_file().get('username') != 'coltongarelli':
        chart_studio.tools.set_credentials_file(username='coltongarelli', api_key='JEoo9aVmctpeUlByHPU3')
    plot(fig, filename=name, auto_open=True)


def save_local_interactive(fig: go.Figure, name):
    """
    Save an interactive plotly plot locally
    Args:
        fig: a go.Figure object to save online
        name: a name for the plot

    """
    from plotly.offline import plot
    plot(fig, filename=name)

def construct_point(df):
    markers = ['o', 'v', 's', 'd', 'P', '+', '8', '*', "X", 'x', "D", 'd', 7, 6,
               "$:)$", "$:($", "$=$", "$?$",
               "$!$"]
    if df.shape[0] > len(markers):
        mult = df.shape[0]/len(markers)
        mod = df.shape[0]%len(markers)
        if mod == 0:
            markers = markers*int(mult)
        else:
            markers = markers*int((mult+1))
    num_colors = len(df.index)
    cm = plt.get_cmap('gist_rainbow')
    colors = [cm(1. * i / num_colors) for i in range(num_colors)]
    return markers, colors


def plot_pca(df, rows, batch: bool =False):
    """Plots PCA data on a scatter plot where x = PC1 and y = PC2

    Plot the first two principal components of PC analyzed data on a scattermap. Plotting PCs can be used as a measure
    for batch effect or correction. PCA can also be used to determine correlation of a list of interest genes.

    Notes:
        - Perform PCA on specific genes to utilize PCA for non-batch analysis

    Args:
        df: a DataFrame containing PC analyzed data to plot on a scatter plot (x = PC1, y= PC2)
        rows: A dictionary that maps each sample or batch to each PC data experiment/sample in df.
        batch: consider changing to 'group' for generic grouping
    Returns:
        Figure and Axes objects

    """

    markers, colors = construct_point(df)
    cdict = dict(zip(rows.keys(), colors))
    marker = dict(zip(rows.keys(), markers))
    fig, ax = plt.subplots(figsize=(10, 8))
    if batch:
        # consider changing batch to 'group' for generic grouping
        labels = ['Batch {}'.format(i+1) for i in range(len(colors))]
    else:
        labels = df.index.to_list()
    add_plot(df=df, ax=ax, cdict=cdict, marker=marker, labels=labels, rows=rows)
    plt.xlabel("Principal Component 1", fontsize=15)
    plt.ylabel("Principal Component 2", fontsize=15)

    for i in df.index.to_list():
        ax.annotate(i, (df.loc[i, ['Principal Component 1']]+.05, df.loc[i, ['Principal Component 2']]+.05))
    # ax.legend(loc='upper right', bbox_to_anchor=(1.04, 1))
    plt.tight_layout()
    ax.legend().remove()
    return fig, ax


def pca_3D(df, rows, batch: bool =False):
    """
    3D PCA using https://matplotlib.org/3.1.1/gallery/mplot3d/scatter3d.html
    Plot the first two principal components of PC analyzed data on a scattermap. Plotting PCs can be used as a measure
    for batch effect or correction. PCA can also be used to determine correlation of a list of interest genes.

    Notes:
        - Perform PCA on specific genes to utilize PCA for non-batch analysis

    Args:
        df: a DataFrame containing PC analyzed data to plot on a scatter plot (x = PC1, y= PC2)
        rows: A dictionary that maps each sample or batch to each PC data experiment/sample in df.
        batch: consider changing to 'group' for generic grouping
    Returns:
        Figure and Axes objects

    """
    markers, colors = construct_point(df)
    cdict = dict(zip(rows.keys(), colors))
    marker = dict(zip(rows.keys(), markers))
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    if batch:
        # consider changing batch to 'group' for generic grouping
        labels = ['Batch {}'.format(i+1) for i in range(len(colors))]
    else:
        labels = df.index.to_list()
    add_plot(df=df, ax=ax, cdict=cdict, marker=marker, labels=labels, rows=rows)
    ax.set_xlabel("Principal Component 1", fontsize=15)
    ax.set_ylabel("Principal Component 2", fontsize=15)
    ax.set_zlabel("Principal Component 3", fontsize=15)
    plt.tight_layout()
    ax.legend()
    return fig, ax


def add_plot(df, ax, rows, cdict, labels, marker):
    for k, v in rows.items():
        ax.scatter(xs=df.loc[v]['Principal Component 1'], ys=df.loc[v]['Principal Component 2'], zs=df.loc[v]['Principal Component 3'],
                   c=[cdict.get(k)],
                   marker=marker.get(k), label=labels[k],
                   s=55)