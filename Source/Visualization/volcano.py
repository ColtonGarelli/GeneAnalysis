import plotly.offline as py
# import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from functions.differential_expression import log_transform
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


def seaborn_volcano_plot(colnames, d=None, title=None):
    """
    From: https://reneshbedre.github.IO/blog/volcano.html
    :param d:
    :return:
    """
    # y-value is -log10 normalized pvalue
    d, log_p = log_transform(d, colnames['pval'], logbase=10)
    d.dropna(inplace=True)
    # for i1 in d.index:
    #     if "CXCL" in str(i1):
    #         print(i1)
    sns.set_style('darkgrid')
    plt.xlim((-6, 6))
    # Create a colorbar for the volcano plot
    norm = plt.Normalize(d[colnames['logfc']].max(), d[colnames['logfc']].min())
    cmap = sns.diverging_palette(h_neg=200, h_pos=0, as_cmap=True)
    mappable = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    mappable.set_array([])
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
                               palette=cmap, legend=False)
    scat.figure.colorbar(mappable)
    # plt.colorbar(scat)
    plt.xlabel('Log$_2$FC')
    plt.ylabel("Log$_{10}$ Adjusted P-Value")
    plt.title("Plot of {}".format(title))
    a = pd.concat({'x': d[colnames['logfc']], 'y': d[log_p], 'val': d.index.to_series()}, axis=1)
    for i, point in a.iterrows():
        if d[log_p].loc[i] > 2 and (d[colnames['logfc']].loc[i] < -3 or d[colnames['logfc']].loc[i] > 3):
            scat.text(point['x'] + .15, point['y'], str(point['val']), size=5)
    return scat


def display_vals(df, genes_to_display):
    return df.join(genes_to_display, how='inner')











    # plt.savefig('testing_volcano.png')
    # Assign colors to up and down regulated genes
    # d.loc[(d[logFC] >= 3) & (d[colnames['pval']] < 0.05), 'color'] = "green"  # upregulated
    # d.loc[(d[logFC] <= -3) & (d[colnames['pval']] < 0.05), 'color'] = "red"  # downregulated
    # d['color'].fillna('grey', inplace=True)

    # plt.scatter(d['log2FC'], d[log_col'], c=d['color'])
    # plt.xlabel('log2 Fold Change', fontsize=15, fontname="sans-serif", fontweight="bold")
    # plt.ylabel('-log10(P-value)', fontsize=15, fontname="sans-serif", fontweight="bold")
    # plt.xticks(fontsize=12, fontname="sans-serif")
    # plt.yticks(fontsize=12, fontname="sans-serif")

    # d = d.loc[(d['value1'] >= 10) & (d['value2'] >= 10)]


