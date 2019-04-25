import pytest
import pandas as pd
import file_in
from Source import custom_errors

# files containing different edge cases



# if df.empty = true




@pytest.fixture()
def setup_good_dfs():
    test_files1 = \
        ['/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/good_small_dataset1.csv',
         '/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/good_med_dataset1.csv',
         '/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/good_large_dataset1.csv']
    dfs = [pd.read_csv(i).set_index('symbol').rename_axis(index='symbol') for i in test_files1]
    # for i in dfs:
    #     i.set_index('symbol')
    #     i.rename_axis(index='symbol')
    return dfs

@pytest.fixture()
def setup_bad_dfs():
    fail_test_files = ['/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/bad_small_dataset1.csv',
                        '/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/bad_med_dataset1.csv',
                        # '/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/bad_large_dataset1.csv'
                       # "/Users/coltongarelli/pyLibraries/GeneAnalysis/tests/testing_files/empty_dataset.csv"
                       ]
    dfs = [pd.read_csv(i).set_index('symbol').rename_axis(index='symbol') for i in fail_test_files]
    # for i in dfs:
    #     i.set_index('symbol')
    return dfs

def test_column_name_norm(setup_good_dfs):
    """
    Test to ensure column names are read correctly. Symbol, log2fc/logfc column
    test lowercase, name equiv
    :return:
    """
    for i in setup_good_dfs:
        assert ['logfc', 'adj-pvalue'] == i.columns.values.tolist()


def test_index_set_to_symbol(setup_good_dfs):
    """
    Indexes should be unique gene identifiers, denoted as 'symbol' in data
    Test index set to symbol
    :param setup_good_dfs:
    :return:
    """
    for i in setup_good_dfs:
        assert i.index.name == 'symbol'


# def test_error_wrong_column_name(setup_bad_dfs):
#     """
#     Test correct error thrown for insufficient column naming/contents
#     :return:
#     """
#
#     with pytest.raises(custom_errors.InvalidColumnsError("error")) as info:
#         for i in setup_bad_dfs:
#             message = file_in.check_col_names(i)


def test_correct_datatype_from_input(setup_good_dfs):
    """
    Set datatypes for columns (eg str for symbol, float for pvalue+logfc)
    :return:
    """
    # for i in setup_good_dfs:
    #     assert


if __name__ == '__main__':
    pytest.main()

