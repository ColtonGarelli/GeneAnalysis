
from Bio import Geo
import pytest


def test_cutoff_vals():

    records = list()
    with open("../tests/GDS996.soft") as f:
        # Parse geo records to Bio Records
        data = Geo.parse(f)
        for i in data:
            records.append(i)
    # records[5] holds the expression data
    print(records[0].table_rows)


def test_the_test():
    assert 1 == 2, "some stuff to test message"


if __name__ == '__main__':
    pytest.main()
