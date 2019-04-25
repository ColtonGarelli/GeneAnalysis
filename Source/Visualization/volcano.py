import plotly as py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
py.tools.set_credentials_file(username='coltongarelli', api_key='OeZDThyslDgaGROfcb2m')



def plotly_volcano(data=None, pvalue="adj_pvalue"):
    logFC = "logFC"
    if data is None:
        data = pd.read_csv("https://reneshbedre.github.IO/myfiles/volcano/SaLR_DEGseq.txt", sep="\t")
        logFC = "log2FC"

    print(data.head())  # first five lines
    print(data.info())  # table information including dimensions

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
    data_to_plot['logpv'] = -np.log10(data_to_plot[pvalue])
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
            y=data_to_plot['logpv'],
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



def seaborn_volcano_plot(d=None):
    """
    From: https://reneshbedre.github.IO/blog/volcano.html
    :param d:
    :return:
    """
    logFC = "logFC"
    # for reference dataset
    if d is None:
        # load data file
        d = pd.read_csv("https://reneshbedre.github.IO/myfiles/volcano/SaLR_DEGseq.txt", sep="\t")
        logFC = "log2FC"

    # to see first few lines of table and get table dimensions
    print(d.head())  # first five lines
    print(d.info())  # table information including dimensions

    # Only include data with large differential expression and good p values
    # Assign colors to up and down regulated genes
    d.loc[(d[logFC] >= 1) & (d['p-value'] < 0.05), 'color'] = "green"  # upregulated
    d.loc[(d[logFC] <= - 1) & (d['p-value'] < 0.05), 'color'] = "red"  # downregulated
    d['color'].fillna('grey', inplace=True)

    # only take values that had 10 or more expression count
    d = d.loc[(d['value1'] >= 10) & (d['value2'] >= 10)]

    # y-value is -log10 normalized pvalue
    # you can use d.nsmallest(2, 'p-value')
    low_p = d.nsmallest(2, 'p-value')
    for i in d['p-value']:
        if i == 0:
            i = low_p
    d['logpv'] = (-np.log10(d['p-value']))
    # change d['logpv'] to d['p-value']
    sns.scatterplot("log2FC", "logpv", data=d, hue='log2FC')
    # plt.scatter(d['log2FC'], d['logpv'], c=d['color'])
    # plt.xlabel('log2 Fold Change', fontsize=15, fontname="sans-serif", fontweight="bold")
    # plt.ylabel('-log10(P-value)', fontsize=15, fontname="sans-serif", fontweight="bold")
    # plt.xticks(fontsize=12, fontname="sans-serif")
    # plt.yticks(fontsize=12, fontname="sans-serif")
    plt.show()


