import pytest
import pandas as pd
import modify_dataframes
import os
import file_in


class TestingFiles:
    test_files1 = \
        [os.path.join(os.getcwd(), 'testing_files/test_files/test_data1.csv'),
         os.path.join(os.getcwd(), 'testing_files/test_files/test_data2.csv'),
         os.path.join(os.getcwd(), 'testing_files/test_files/test_data3.csv')]


@pytest.fixture()
def setup_simple_sorting_data():
    """Setup function
    Creates dataframes to be sorted by gene name

    Returns:

    """
    dfs = list()
    for i in TestingFiles.test_files1:
        cols = file_in.check_col_names(i)
        dfs.append(file_in.read_csv_data(i, cols))
    return dfs

@pytest.fixture()
def setup_reference_data():
    overlap_10 = pd.read_csv(os.path.join(os.getcwd(), 'testing_files/reference_files/test_data_reference.csv')).set_index('symbol').rename_axis(
        index='symbol')
    overlap_1 = pd.read_csv(os.path.join(os.getcwd(), 'testing_files/reference_files/single_overlap_ref.csv')).set_index('symbol').rename_axis(
        index='symbol')
    return [overlap_10, overlap_1]


def make_test_df(path):
    cols = file_in.check_col_names(path)
    df = file_in.read_csv_data(path, cols)
    return df


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
    test_df = file_in.read_csv_data(path=(os.path.join(os.getcwd(), 'testing_files/test_files/cutoff_test_data.csv')),
                                    col_names={'logfc': 'logfc-1', 'pval': 'adj-pvalue-1', 'symbol': 'symbol'})
    actual = modify_dataframes.value_cutoff(upper=0.05, df=test_df, col_name='adj-pvalue-1')
    ref_df = file_in.read_csv_data(path=(os.path.join(os.getcwd(), 'testing_files/reference_files/05_pvalue_ref.csv')),
                                   col_names={'logfc': 'logfc-1', 'pval': 'adj-pvalue-1', 'symbol': 'symbol'})
    pd.testing.assert_frame_equal(actual, ref_df,
                                  # index dtype
                                  check_index_type=True,
                                  # col names shouldn't be identical
                                  check_names=False,
                                  # exact numerical values
                                  check_exact=True,
                                  # ignore order
                                  check_like=True)
    ref_df = file_in.read_csv_data(path=(os.path.join(os.getcwd(), 'testing_files/reference_files/low_pval_cutoff_ref.csv')),
                                   col_names={'logfc': 'logfc-1', 'pval': 'adj-pvalue-1', 'symbol': 'symbol'})
    actual = modify_dataframes.value_cutoff(upper=0.001, df=test_df, col_name='adj-pvalue-1')

    pd.testing.assert_frame_equal(actual, ref_df,
                                  # index dtype
                                  check_index_type=True,
                                  # col names shouldn't be identical
                                  check_names=False,
                                  # exact numerical values
                                  check_exact=True,
                                  # ignore order
                                  check_like=True)
    ref_df = file_in.read_csv_data(
        path=(os.path.join(os.getcwd(), 'testing_files/reference_files/logfc2_cutoff_ref.csv')),
        col_names={'logfc': 'logfc-1', 'pval': 'adj-pvalue-1', 'symbol': 'symbol'})
    actual = modify_dataframes.value_cutoff(upper=2, lower=-2, df=test_df, col_name='logfc-1')
    pd.testing.assert_frame_equal(actual, ref_df,
                                  # index dtype
                                  check_index_type=True,
                                  # col names shouldn't be identical
                                  check_names=False,
                                  # exact numerical values
                                  check_exact=True,
                                  # ignore order
                                  check_like=True)

    ref_df = file_in.read_csv_data(
        path=(os.path.join(os.getcwd(), 'testing_files/reference_files/logfc4_cutoff_ref.csv')),
        col_names={'logfc': 'logfc-1', 'pval': 'adj-pvalue-1', 'symbol': 'symbol'})
    actual = modify_dataframes.value_cutoff(upper=4, lower=-4, df=test_df, col_name='logfc-1')
    pd.testing.assert_frame_equal(actual, ref_df,
                                  # index dtype
                                  check_index_type=True,
                                  # col names shouldn't be identical
                                  check_names=False,
                                  # exact numerical values
                                  check_exact=True,
                                  # ignore order
                                  check_like=True)



def test_gene_sort(setup_simple_sorting_data, setup_reference_data):
    """
    Test proper sorting by gene (i.e multiple RNAseq sets may not have 100% shared read sets, remove unshared reads)


    Returns:
    """
    # two dfs with common genes all in common

    actual = modify_dataframes.find_common_genes(setup_simple_sorting_data[:2])
    test_ds_one_two = os.path.join(os.getcwd(), "testing_files/reference_files/all_overlap.csv")
    all_overlapdf = make_test_df(test_ds_one_two)
    pd.testing.assert_frame_equal(actual, all_overlapdf,
                                  # index dtype
                                  check_index_type=True,
                                  # col names shouldn't be identical
                                  check_names=False,
                                  # exact numerical values
                                  check_exact=True,
                                  # ignore order
                                  check_like=True)
    # three dfs, two completely overlap, 1 overlaps by 10
    actual = modify_dataframes.find_common_genes(setup_simple_sorting_data[:3])
    pd.testing.assert_frame_equal(actual, setup_reference_data[0],
                                  # index dtype
                                  check_index_type=True,
                                  # col names shouldn't be identical
                                  check_names=False,
                                  # exact numerical values
                                  check_exact=True,
                                  # ignore order
                                  check_like=True)
    single = os.path.join(os.getcwd(), "testing_files/test_files/single_overlap.csv")
    single_df = make_test_df(single)
    sets = setup_simple_sorting_data[:2]
    new_set = list()
    for i in sets:
        new_set.append(i.copy(deep=True))
    new_set.append(single_df)
    actual = modify_dataframes.find_common_genes(new_set)
    pd.testing.assert_frame_equal(actual, setup_reference_data[1],
                                  # index dtype
                                  check_index_type=True,
                                  # col names shouldn't be identical
                                  check_names=False,
                                  # exact numerical values
                                  check_exact=True,
                                  # ignore order
                                  check_like=True)
    no_overlap = os.path.join(os.getcwd(), 'testing_files/test_files/test_data4.csv')
    no_overlapdf = pd.read_csv(no_overlap).set_index('symbol').rename_axis(index='symbol')
    full_set = list()
    for i in sets:
        full_set.append(i.copy(deep=True))
    full_set.append(no_overlapdf)
    actual = modify_dataframes.find_common_genes(full_set)
    # one of the dfs (no_overlapdf) does not have common genes. should be empty
    assert actual.empty


# check_less_precise : bool or int, default False
# Specify comparison precision.
# Only used when check_exact is False.
# 5 digits (False) or 3 digits (True) after decimal points are compared. If int, then specify the digits to compare.




