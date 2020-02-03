import plotly.offline as py
# import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from data_processing.differential_expression import log_transform
import matplotlib as mpl
import matplotlib.colors as colors
mpl.rcParams['figure.dpi'] = 350
# py.tools.set_credentials_file(username='coltongarelli', api_key='xRJ5tPIjCkx8pz17KWzl')


def plotly_volcano(log_col, data=None, pvalue="adj_pvalue"):
    """

    Args:
        log_col:
        data:
        pvalue:

    Returns:

    """
    logFC = "logFC"
    # Only include data with large differential expression and good p values
    data_to_plot = data.loc[(data[pvalue] < 0.01)]
    data_to_plot.append(data.loc[-2 < (data[logFC] < 2)])
    # only take values that had 10 or more expression count...this should be unnecessary bc of adjusted p-value
    # data_to_plot = data_to_plot.loc[(data_to_plot['AveExpr'] >= 10)]
    print(data_to_plot.pvalue.max())
    # you can use d.nsmallest(2, 'p-value') to replace p-values of 0 with smallest pvalue (to avoid artifacts)
    low_p = data_to_plot.nsmallest(2, pvalue)
    data_to_plot[pvalue].replace(to_replace=0, value=low_p)
    # y-value is -log10 normalized pvalue
    data_to_plot[log_col] = -np.log10(data_to_plot[pvalue])
    l = []
    y = []
    # Setting colors for plot.
    N = 53
    c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 360, N)]

    for i in range(int(N)):
        y.append((2000 + i))
        # The hover text goes text=...
        trace0 = go.Scatter(
            x=data_to_plot[logFC],
            y=data_to_plot[log_col],
            mode='markers',
            marker=dict(size=14, line=dict(width=1), color=c[i], opacity=0.3), name=y[i], text=data_to_plot['symbol'])
        l.append(trace0)

    layout = go.Layout(
        title='Differential Expression',
        hovermode='closest',
        xaxis=dict(
            title='Expression change',
            ticklen=2,
            zeroline=True,
            gridwidth=2,
        ),
        yaxis=dict(
            title='-Log P-value',
            ticklen=5,
            gridwidth=2,
        ),
        showlegend=False
    )
    fig = go.Figure(data=l, layout=layout)
    py.plotly.plotly.plot(fig)


def sns_volcano(colnames, d=None, title=None, genes: list=None):
    # TODO: Adapt to OOP. Look up how mpl does oop vs functional.
    # TODO: split into multiple functions that sns_volcano uses
    """
    Adapted from example at: https://reneshbedre.github.IO/blog/volcano.html
    :param d:
    :return:

    # need to make object oriented but maintain axes
    """
    # y-value is -log10 normalized pvalue
    d, log_p = log_transform(d, colnames['pval'], logbase=10)
    d.dropna(inplace=True)
    # for i1 in d.index:
    #     if "CXCL" in str(i1):
    #         print(i1)
    sns.set_style('darkgrid')
    big = d[colnames['logfc']].nlargest(1).to_numpy()
    small = d[colnames['logfc']].nsmallest(1).to_numpy()
    xlim = big[0] if big[0] > np.fabs(small[0]) else np.fabs(small[0])
    plt.xlim = (-xlim, xlim)
    # plt.pcolor(X=d[colnames['logfc']], Y=d[colnames['pval']])
    # Create a colorbar for the volcano plot
    norm = plt.Normalize(d[colnames['logfc']].max(), d[colnames['logfc']].min())
    midnorm = MidpointNormalize(midpoint=0, vmin=small, vmax=big)
    cmap = sns.diverging_palette(h_neg=200, h_pos=0, as_cmap=True)
    mappable = plt.cm.ScalarMappable(cmap=cmap, norm=midnorm)
    # mappable.set_array([])
    # color dots on a green spectrum
    if 'DEG' in d.columns:

        scat = sns.scatterplot(x=colnames['logfc'], y=log_p,
                               data=d, hue=d[colnames['logfc']],
                               palette=cmap, legend=False)
        # non_deg = d[~d.DEG]
        # greys = non_deg.index.values
        # nans = np.argwhere(np.isnan(greys))
        # greys = greys.nan_to_num(range(len(nans)), copy=True)
        # x = d.loc[greys]
        # plt.scatter(d[greys][colnames["logfc"]], y=d[greys][colnames["pvalue"]], color='grey')
    else:


        scat = sns.scatterplot(x=colnames['logfc'], y=log_p,
                               data=d, hue=d[colnames['logfc']],
                               palette=cmap, hue_norm=midnorm, legend=False)
    scat.figure.colorbar(mappable)
    scat.set_xlabel('Log$_2$FC')
    scat.set_ylabel("Log$_{10}$ Adjusted P-Value")
    scat.figure.suptitle("Plot of {}".format(title))
    a = pd.concat({'x': d[colnames['logfc']], 'y': d[log_p], 'val': d.index.to_series()}, axis=1)

    if genes is None:
        for i, point in a.iterrows():
            try:
                if d.loc[i, log_p] > 2.0 and (d.loc[i, colnames['logfc']] < -1 or d.loc[i, colnames['logfc']] > 2):
                    scat.text(point['x'] + .15, point['y'], str(point['val']), size=5)

            # This will turn everything below significance gray
            #     else:
            #         scat.scatter(point['x'], point['y'], color='silver')
            except Exception:
                pass
    elif genes is not None:
        for i, point in a.iterrows():
            try:
                if d.loc[i, log_p] > 2.0 and (d.loc[i, colnames['logfc']] < -1 or d.loc[i, colnames['logfc']] > 1) and i in genes:

                    scat.text(point['x'] + .15, point['y'], str(point['val']), size=5)

                elif i not in genes:
                    pass
            except Exception:
                print(d.loc[i, log_p])
                # This will turn everything below significance gray
                # else:
                #     scat.scatter(point['x'], point['y'], color='silver')
    return scat


def display_vals(df, genes_to_display):
    return df.join(genes_to_display, how='inner')


class MidpointNormalize(colors.Normalize):
    """
    Copied from: http://chris35wills.github.io/matplotlib_diverging_colorbar/
    Normalise the colorbar so that diverging bars work there way either side from a prescribed midpoint value)

    e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

