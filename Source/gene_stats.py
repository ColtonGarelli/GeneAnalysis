import pandas as pd
import numpy as np


def calculate_FC(differential_data: pd.DataFrame, baseline_data: pd.DataFrame, logbase=2) -> pd.DataFrame:
    """Calculates fold change from expression counts.

    Calculates fold change (FC) using control data and experiment data ( (differential/baseline) -1 ).
    if baseline < expression:
        expression/baseline = FC
    elif baseline > expression:
        (baseline/expression) * -1 = FC
    log2(FC) = log2FC

    Returns:

    """


def log_transform(df: pd.DataFrame, col, logbase=2) -> tuple:
    """
    Perform a log transformation on FC data to eliminate bias between under and overexpressed genes.

    Args:
        FCdata:

        logbase:

    Returns:

    """
    low_p = df.nsmallest(2, col)
    df[col].replace(to_replace=0, value=low_p)

    if logbase == 2:
        log_col = 'log_{}'.format(col)
        df[log_col] = (np.log2(df[col]))
    elif logbase == 10:
        log_col = 'log_{}'.format(col)
        df[log_col] = (-np.log10(df[col]))

    return df.copy(deep=True), log_col


