import pandas as pd
import re
import csv
import os
from datetime import date


logfc = 'logfc'
gene_name = 'symbol'
pvalue = 'pval'


def read_csv_data(path: str, col_names: dict=None):
    """Read csv data to pandas DataFrame

    Read csv formatted expression data into a pandas DataFrame for further manipulation.
    The file should be formatted 'symbol,logfc,pvalue' as the first row and corresponding data on following rows

    Args:
        path (str): Full path to the target file
        col_names (dict): Actual names of columns from file
    Returns:
        pandas.DataFrame : A dataframe containing data from the file input as 'path'
    """
    if col_names is None:
        df = pd.read_csv(os.path.join(path))
    else:
        if '/' in path or '\\' in path:
            df = pd.read_csv(os.path.join(path), index_col=col_names.get(gene_name),
                             dtype={col_names.get(gene_name): 'object',
                             col_names.get(logfc): 'float64',
                             pvalue: 'float64'}
                             )
        else:
            df = pd.read_csv(os.path.join(os.path.expanduser('~'), 'Desktop', path), index_col=col_names.get(gene_name),
                             dtype={col_names.get(gene_name): 'object',
                                    col_names.get(logfc): 'float64',
                                    pvalue: 'float64'}
                             )
    return df


def check_col_names(path):
    """Inspect a file for column names
    Attempt to determine columns containing relevant information. In this case, relevant information is some form of
    of a p-value, log transformed fold change data (some form of logfc), and a gene names column to use as an index.

    Args:
        path: path to data file to inspect

    Returns: a dictionary mapping universal string representations for genes, p-values, logfc data to those in the file
    TODO: update this function to accommodate different file formats (e.g. with/without pvalue, to include extra params in the dict returned
    """
    with open(path, 'r+') as file:
        reader = csv.reader(file)
        try:
            cols = next(reader)
        except:
            return None
    pval = re.compile(r'.*adj.*p.*val.*', re.I)
    log = re.compile('.*log.*fc.*', re.I)
    gene = re.compile('symbol.*|gene.*', re.I)
    pval_match = None
    log_match = None
    gene_match = None
    for i in cols:
        if pval.search(i) is not None:
            pval_match = re.search(pval, i).group()
        if re.search(log, i) is not None:
            log_match = re.search(log, i).group()
        if re.search(gene, i) is not None:
            gene_match = re.search(gene, i).group()

    # if None in [pval_match, log_match, gene_match]:
    #     print("Check your column names!!")
    #     return None
    else:
        return {'symbol': gene_match, 'logfc': log_match, 'pval': pval_match}


def make_unique_index(df):
    """Check for duplicate indices (genes) in df and make unique (add _ and a count)

    Args:
        df: DataFrame to check for duplicated indices

    Returns: df with no duplicated indices

    """
    count = dict()
    counter = 1
    indices = df.index.to_list()
    for i in range(len(df.index.duplicated())):
        if i:
            index_to_mod = df.index[i]
            count.update({index_to_mod: str(index_to_mod) + '_' + str(counter)})
            counter += 1
            indices[i] = count.get(index_to_mod)
    df.index = pd.Index(indices, name=gene_name)
    return df


def strip_data(df: pd.DataFrame, data_to_keep: dict):
    """Strip unwanted data from a DataFrame

    TODO: define use cases for this function and update docs. Duplicate of modify_dataframes.drop_cols

    Args:
        df:
        data_to_keep:

    Returns:

    """
    gene_name = 'symbol'
    if df.index.name == data_to_keep.get(gene_name):
        data_to_keep.pop(gene_name)
    new_df = df[data_to_keep.values()]
    return new_df


def infer_file_name(path):
    """
    Dataframes of imported data will be hashed to the name of the file. All of the files should reside
    in the same folder
    :return:
    """
