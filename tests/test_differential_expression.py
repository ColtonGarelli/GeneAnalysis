import pytest
import pandas as pd
import differential_expression


def test_logbase_choice():
    """
    test log transformation base decision
    Returns:

    """
#     2.3219280949 log2 of 5
#     0.69897000434 log10 of 5
    df = pd.DataFrame(data={"A": [5], "B": [0], "C": [2]})
    log2, log2col = differential_expression.log_transform(df, col="A", logbase=2)
    log10, log10col = differential_expression.log_transform(df, col="A", logbase=10)
    assert pytest.approx(log2[log2col], 2.3219280949)
    assert pytest.approx(log10[log10col], 0.69897000434)



def test_replace_zeroes():
    """
    test
    Returns:

    """


def test_list_choice():
    """
    test both list decisions (logbase 2 and 10)
    Returns:

    """


def test_calc_FC():
    """
    test fold change calculation
    Returns:

    """
