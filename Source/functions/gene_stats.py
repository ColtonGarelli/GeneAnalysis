import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, quantile_transform
from itertools import chain
from functools import reduce


def pca_calculation(pca_dfs: [pd.DataFrame] or pd.DataFrame):
    """PCA on a DataFrame or on a list of DataFrames.

    Perform PCA on several datasets to determine extent of batch effects or to compare global differences between
    datasets. A DataFrame containing samples to compare or a list of DataFrames (usually to compare between samples for
    batch effect) is passed. Data is standardized using the sklearn.preprocessing.StandardScaler class. (n/2)-1 components
    are calculated from standardized data. DataFrames passed should be formatted with experiments as columns and genes
    as rows.

    References: https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
                https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html
                http://www.marcottelab.org/users/BCH391L_2015/NBT_primer_PCA.pdf


    Args:
        pca_dfs: A DataFrame, or list of DataFrames containing gene expression data for PCA comparison.

    Returns: A DataFrame containing the first (n/2)-1 components

    """
    PCs = int((len(pca_dfs.columns.to_list()) / 2) - 1)
    if isinstance(pca_dfs, list):
        cols = dict(list(enumerate(chain(*[i.columns.values for i in pca_dfs]))))
        vals = [cols.values()]
        vals = list(chain.from_iterable(vals))
        pooled = [pca_dfs[i].join(pca_dfs[i + 1]) for i in range(len(pca_dfs) - 1)]
        [i.dropna() for i in pooled]
        merged = reduce(lambda left, right: pd.merge(left, right, on='gene'), pca_dfs)
        pca = PCA(n_components=int((len(pca_dfs) / 2) - 1))

    else:
        vals = pca_dfs.columns.to_list()
        i = iter(vals)
        cols = dict(zip(range(len(vals)), i))
        merged = pca_dfs
        merged.dropna()
        pca = PCA(n_components=PCs)
    transposed = merged.transpose()
    # StandardScalar calculates z-score z = (x-mean)/std-dev
    scaled = StandardScaler().fit_transform(transposed)
    pca_transformed = pca.fit_transform(scaled)
    final_df = pd.DataFrame(data=pca_transformed, index=vals, columns=["Principal Component {}".format(i+1) for i in range(PCs)])
    return final_df, cols


def quantile_norm(dfs: [pd.DataFrame] or pd.DataFrame):
    """Perform quantile normalization on expression data.

    Quantile normalize a list of DataFrames using sklearn.Preprocessing.quantile_transform with default n_quantiles=1000.
    The DataFrame(s) passed should contain samples from the same batch. Each DataFrame should be formatted with columns
    as samples and rows as genes.

    TODO: as of now the function assumes the gene order and number are the same across samples. This should change

    Args:
        dfs: a DataFrame or list of DataFrames from the same batch

    Returns: a dataframe containing

    """
    transformed = list()
    vals = [list(i.columns.values) for i in dfs]
    index = dfs[0].index.tolist()
    if isinstance(dfs, list):
        for i in range(len(dfs)):
            transformed.append(pd.DataFrame(quantile_transform(dfs[i], axis=0), columns=vals[i], index=index))
    else:
        transformed = pd.DataFrame(quantile_transform(dfs, axis=0), columns=vals, index=index)
    return transformed


def batch_effect_adjust(df):
    """Adjust for batch effects using R function ComBat from sva package
    Ref: https://www.youtube.com/watch?v=z3vqrkRGSLI

    Args:
        df:

    Returns:

    """


def calc_adj_pvalue(dfs):
    """Calculate adjusted p-value

    Args:
        dfs:

    Returns:

    """
    pass


# def kmeans_cluster(df):
#     """
#     A DataFrame containing several samples
#     Args:
#         df:
#
#     Returns:
#     """
