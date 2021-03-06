import pandas as pd
import numpy as np
# deseq = importr('DESeq2', lib_loc='/Users/coltongarelli/anaconda3/envs/GeneAnalysis/lib/R/')

def calculate_FC(differential_data: pd.DataFrame, baseline_data: pd.DataFrame) -> pd.DataFrame:
    """Calculates fold change from expression counts
       Calculates fold change (FC) using control data and experiment data ( (experimental/baseline) - 1 ).

    Args:
        differential_data: Data from some experimental group (disease, treated, time course, etc.)
        baseline_data: Data from a control group (untreated, healthy, time = 0, etc.)

    Returns: pandas df containing Fold Change calculation

    """
#     pseudo-code

    index = differential_data.index
    FC = pd.DataFrame(index=index)
    differential_data
    # if baseline < expression:
    #     expression/baseline = FC
    # elif baseline > expression:
    #     (baseline/expression) * -1 = FC


def log_transform(df: pd.DataFrame, col: str or list, logbase=2) -> tuple:
    """Log transform data by log2 or log10
        Perform a log transformation on FC data to eliminate bias between under and over-expressed genes,
        p-value data for volcano plot, or other log transformations.

    Args:
        df: a DataFrame containing some (but not only) data to log transform
        col: column if str or list of columns of df to perform log transformation on
        logbase: the log base to transform data by (default is log2)

    Returns:

    """

    if logbase == 2:
        if isinstance(col, list):
            log_col = list()
            for i in col:
                df[i] = replace_zeroes(df[i], i)
                log = 'log_{}'.format(i)
                log_col.append(log)
                # if logbase == 2:
                #     df[log] = (df[i].apply(np.log2))
                # else:
                df[log] = (df[i].apply(np.fabs))
            return df.copy(deep=True), log
        else:
            df[col] = replace_zeroes(df[col], col)
            log_col = 'log_{}'.format(col)
            df[log_col] = (np.fabs(np.log2(df[col])))
            return df.copy(deep=True), log_col
    else:
        if isinstance(col, list):
            log_col = list()
            for i in col:
                df[i] = replace_zeroes(df[i], i)
                log = 'log_{}'.format(i)
                log_col.append(log)
                df[log] = (df[i].apply(np.log10))
                df[log] = (df[i].apply(np.fabs))
            return df.copy(deep=True), log
        else:
            df[col] = replace_zeroes(df[col], col)
            log_col = 'log_{}'.format(col)
            df[log_col] = (np.fabs(np.log10(df[col])))
            return df.copy(deep=True), log_col


def replace_zeroes(df: pd.DataFrame or pd.Series, col: str):
    """

    Returns:

    """
    # method for lists...?  lowest = df[df > 0].min(axis=0)
    lowest = df.nsmallest(2, keep='first')
    return df.replace(to_replace=0, value=lowest)
