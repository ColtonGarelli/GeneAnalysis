import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def violin_plot(df, cols: dict, genes: [] = None):
    """Make a violin plot

    Makes a violin plot of all genes in df or genes defined by the parameter 'genes'.

    Args:
        df: DataFrame containing logFC and p-value. **Must** contain logfc and p-value data from one experiment
        genes: a list of genes
        cols:

    Returns:
        an instance of a violin plot
    """
    if genes is None:
        return sns.violinplot(y=cols.get('logfc'), data=df, orient='v')

    else:
        to_plot = df.loc[genes]
        return sns.violinplot(y=to_plot, orient='v')



