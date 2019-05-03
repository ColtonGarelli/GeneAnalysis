import pytest
import pandas as pd
from Source import gene_stats

# a list of p_values to adjust
p_values = None


"""
General test methods:
    test on small (10) medium (50-100) and large (>1000) datasets
"""

@pytest.fixture()
def setup_sorting_data():
    """Setup function
    Creates dataframes to be sorted by gene name

    Returns:

    """
    test_files1 = \
        ['/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/Book1.csv',
         '/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/Book2.csv',
         '/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/Book3.csv']
    dfs = list()
    for i in test_files1:
        df = pd.read_csv(i).set_index('symbol')
        df.rename_axis('symbol')
        dfs.append(df)
    # dfs = [pd.read_csv(i).set_index('symbol').rename_axis(index='symbol') for i in test_files1]

    return dfs

@pytest.fixture()
def setup_reference_data():
    return pd.read_csv('/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/GoodBook.csv').set_index('symbol').rename_axis(index='symbol')


def test_adjusting_pvalue():
    pass


def test_good_value_cutoff():
    """
    test cutoff function.
    FUT should take:
        a dataframe with some kind of identifier ('symbol') and at least one
        other column with float values. The name(s) of the column containing float
        values to be cut off should be passed in as a list
    FUT should return:
        a dataframe containing all values from input df below the input threshold
    """


def test_bad_value_cutoff():
    """

    Returns:

    """


def test_gene_sort(setup_sorting_data, setup_reference_data):
    """
    Test proper sorting by gene (i.e multiple RNAseq sets may not have 100% shared read sets, remove unshared reads)


    Returns:
    """
    test_dfs = setup_sorting_data
    # two dfs with common genes, one not common
    actual = gene_stats.find_common_genes(test_dfs)
    assert actual.equals(setup_reference_data)
    no_common = [test_dfs[0], test_dfs[2]]
    # two dfs without common genes. should be empty
    actual = gene_stats.find_common_genes(no_common)
    assert actual.empty



def test_data_merge():
    """
    Test FUT to ensure the correct data is moved with sorted symbols
    Returns:

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
