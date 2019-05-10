import pandas as pd
import custom_errors
import re
import csv


logfc = 'logfc'
gene_name = 'symbol'
pvalue = 'pval'


def read_csv_data(path=str, col_names=dict):
    """Read in csv formatted DEGs

    Read csv formatted expression data into a pandas DataFrame for further manipulation.
    The file should be formatted 'symbol,logfc,pvalue' as the first row and corresponding data on following rows

    Args:
        path (str): Full path to the target file
        col_names (dict): Actual names of columns from file
    Returns:
        pandas.DataFrame : A dataframe containing data from the file input as 'path'
    """
    df = pd.read_csv(path, index_col=col_names.get(gene_name),
                     dtype={col_names.get(gene_name): 'object',
                     col_names.get(logfc): 'float64',
                     pvalue: 'float64'}
                     )

    # df = df.set_index(col_names.get(gene_name))
    return df


def check_col_names(path):
    with open(path, 'r+') as file:
        reader = csv.reader(file)
        try:
            cols = next(reader)
        except:
            return None
    pval = re.compile('.*adj.*p.*value.*')
    log = re.compile('.*log.*')
    gene = re.compile('symbol|gene')
    pval_match = None
    log_match = None
    gene_match = None
    for i in cols:
        if re.search(pval, i) is not None:
            pval_match = re.search(pval, i).group()
        if re.search(log, i) is not None:
            log_match = re.search(log, i).group()
        if re.search(gene, i) is not None:
            gene_match = re.search(gene, i).group()

    if None in [pval_match, log_match, gene_match]:
        print("Check your column names!!")
        return None
    else:
        return {'symbol': gene_match, 'logfc': log_match, 'pval': pval_match}


def infer_file_name(path):
    """
    Dataframes of imported data will be hashed to the name of the file. All of the files should reside
    in the same folder
    :return:
    """
