import pandas as pd
import re
import csv
import os
from datetime import date


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
    with open(path, 'r+') as file:
        reader = csv.reader(file)
        try:
            cols = next(reader)
        except:
            return None
    pval = re.compile(r'.*adj.*p.*val.*', re.I)
    log = re.compile('.*fc.*', re.I)
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

    if None in [pval_match, log_match, gene_match]:
        print("Check your column names!!")
        return None
    else:
        return {'symbol': gene_match, 'logfc': log_match, 'pval': pval_match}


def make_unique_index(df):
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
    if df.index.name == gene_name:
        data_to_keep.pop(gene_name)
    new_df = df[data_to_keep.values()]
    return new_df


def create_new_file_dir(desktop_dir, dirname=None):
    if dirname is None:
        new_dir_name = os.path.join(desktop_dir, "Transcript_analysis_{}".format(date.today()))
    else:
        new_dir_name = os.path.join(desktop_dir, dirname)
    counter = 0
    if os.path.isdir(new_dir_name):
        new_dir_name = new_dir_name + "_{}".format(counter)
        while os.path.isdir(new_dir_name):
            counter += 1
            if counter < 11:
                new_dir_name = new_dir_name[:-1]
            elif counter > 10:
                new_dir_name = new_dir_name[:-2]
            elif counter > 100:
                new_dir_name = new_dir_name[:-3]

            new_dir_name = new_dir_name + str(counter)
            os.path.join(new_dir_name)
        os.mkdir(new_dir_name)
    else:
        os.mkdir(new_dir_name)
    return new_dir_name


def infer_file_name(path):
    """
    Dataframes of imported data will be hashed to the name of the file. All of the files should reside
    in the same folder
    :return:
    """
