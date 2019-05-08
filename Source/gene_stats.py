import pandas as pd


def calculate_FC(differential_data: pd.DataFrame, baseline_data: pd.DataFrame, logbase=2) -> pd.DataFrame:
    """Calculates fold change from expression counts.

    Calculates fold change (FC) using control data and experiment data ( (differential/baseline) -1 ).



    Returns:

    """


def log_transform(FCdata: pd.DataFrame, logbase=2) -> pd.DataFrame:
    """
    Perform a log transformation on FC data to eliminate bias between under and overexpressed genes.

    Args:
        FCdata:

        logbase:

    Returns:

    """


