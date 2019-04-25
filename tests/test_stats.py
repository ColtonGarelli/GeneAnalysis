import pytest

# a list of p_values to adjust
p_values = None


"""
General test methods:
    test on small (10) medium (50-100) and large (>1000) datasets
"""

def setup():
    """
    Create dataframes with data to perform calculations on
    :return:
    """
    pass

def test_adjusting_pvalue():
    pass


def test_value_cutoff():
    """
    test cutoff function.
    FUT should take:
        a dataframe with some kind of identifier ('symbol') and at least one
        other column with float values. The name(s) of the column containing float
        values to be cut off should be passed in as a list
    FUT should return:
        a dataframe containing all values from input df below the input threshold
    """


def test_combine_multiple_dfs_by_gene():
    """
    Test appropriate combination of values by gene name. Ensure only common gene info is taken, and that
    the info is correctly appended
    FUT takes:
        a list of dataframes containing symbol names, logfc data, and adjusted pvalue (adj_pvalue)
    FUT returns:
        a dataframe that contains all data associated with all shared genes (eg only the genes common
        b/t the dataframes
    """


def test_calc_log2fc():
    pass


def test_calc_pvalue():
    pass




#
# def test_counts_normalization():
#     """
#     test removal of low count reads
#     :return:
#     """
#     pass
