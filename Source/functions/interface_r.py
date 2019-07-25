"""
A module containing functions to utilize R, mainly the ComBat function in the sva package
"""

import pandas as pd
import rpy2.robjects as robjs
from rpy2.robjects.packages import importr
from rpy2.rinterface import SexpS4
from rpy2.robjects.conversion import Converter
biobase = importr('Biobase')
DFP = importr('DFP')
matrix = robjs.r.matrix


class pyExpressionSet(robjs.methods.RS4):
    """A class explicitly written to

    """
    def __init__(self, files):
        # read data from csv into SexpS4 object and then into an ExpressionSet

        super().__init__()
        pass


def pandas_df_to_exprset(dfs: pd.DataFrame or [pd.DataFrame]) -> pd.DataFrame or list:
    """A function to convert a pandas DataFrame to a Biobase ExpressionSet

    Takes a list of pandas DataFrames or a single pandas DataFrame and converts it to
    (source: https://bioconductor.org/packages/release/bioc/html/Biobase.html)

    References:
        https://rpy2.readthedocs.io/en/version_2.7.x/generated_rst/s4class.html
        https://rpy2.readthedocs.io/en/version_2.7.x/_static/notebooks/s4class.html
        https://rpy2.readthedocs.io/en/version_2.8.x/robjects_oop.html

    Args:
        dfs: pd.DataFrame(s) to convert to Biobase.ExpressionSet (single dataframe or a list)

    Returns:
        a Biobase.ExpressionSet object or a list of Biobase.ExpressionSet objects

    """
    # attributes can be accessed using .slots
    if isinstance(dfs, [pd.DataFrame]):
        exprset = list()
        for i in dfs:
            data = [dfs[col].values.tolist() for col in dfs]
            cols = [col for col in dfs]
            exprset.append(biobase.ExpressionSet(assayData=data, phenoData=cols))
    else:
        data = [dfs[col].values.tolist() for col in dfs]
        exprset = biobase.ExpressionSet(assayData=data, phenoData=[col for col in dfs])

    return exprset