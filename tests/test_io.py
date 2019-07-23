import pytest
import pandas as pd
from functions import file_in
import os


# files containing different edge cases
class FileNames:
    fail_test_files = [os.path.join(os.getcwd(), 'testing_files/test_files/fail_data1.csv'),
                               os.path.join(os.getcwd(), 'testing_files/test_files/bad_med_dataset1.csv'),
                               # os.path.join(os.getcwd(), 'testing_files/test_Files/empty_dataset.csv')
                       ]
    empty_file = os.path.join(os.getcwd(), 'testing_files/test_Files/empty_dataset.csv')

    test_files1 = \
                 [os.path.join(os.getcwd(), 'testing_files/test_files/small_dataset1.csv'),
                  os.path.join(os.getcwd(), 'testing_files/test_files/med_dataset1.csv'),
                  os.path.join(os.getcwd(), 'testing_files/test_files/large_dataset1.csv')]

    fail_cols = [os.path.join(os.getcwd(), 'testing_files/test_files/gene_col_fail.csv'),
                 os.path.join(os.getcwd(), 'testing_files/test_files/log_col_fail.csv'),
                 os.path.join(os.getcwd(), 'testing_files/test_files/pval_col_fail.csv'),
                 os.path.join(os.getcwd(), 'testing_files/test_files/pval_col_fail2.csv'),
                 os.path.join(os.getcwd(), 'testing_files/test_files/empty_dataset.csv')]


@pytest.fixture()
def setup_good_dfs():
    dfs = [pd.read_csv(i).set_index('symbol').rename_axis(index='symbol') for i in FileNames.test_files1]
    yield dfs


@pytest.fixture()
def setup_fail_dfs():

    dfs = [pd.read_csv(i).set_index('symbol').rename_axis(index='symbol') for i in FileNames.fail_test_files]
    from itertools import chain
    dfs = chain(dfs, [pd.DataFrame()])
    yield dfs


def test_column_name_norm():
    """
    Test to ensure column names are read correctly. Symbol, log2fc/logfc column
    test lowercase, name equiv
    :return:
    """
    for i in FileNames.test_files1:
        assert file_in.check_col_names(i) is not None
    for i in FileNames.fail_cols:
        assert file_in.check_col_names(i) is None
    # file_in.read_csv_data(os.path.join(os.getcwd(), 'testing_files/small_dataset1.csv'))


def test_index_set_to_symbol(setup_good_dfs, setup_fail_dfs):
    """
    Indexes should be unique gene identifiers, denoted as 'symbol' in data
    Test index set to symbol
    :param setup_good_dfs:
    :return:
    """
    for i in setup_good_dfs:
        assert i.index.name == 'symbol'


if __name__ == '__main__':
    pytest.main()

