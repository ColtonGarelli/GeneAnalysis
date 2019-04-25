import pandas as pd
import custom_errors


def read_csv_data(path):
    """Read in csv formatted DEGs

    Read csv formatted expression data into a pandas DataFrame for further manipulation.
    The file should be formatted 'symbol,logfc,pvalue' as the first row and corresponding data on following rows

    Args:
        path (str): Full path to the target file

    Returns:
        pandas.DataFrame : A dataframe containing data from the file input as 'path'
    """

    df = pd.read_csv(path, dtype={'symbol': 'object', 'logfc': 'float64', 'adj-pvalue': 'float64'}, index_col='symbol')
    if df.index.size > 3:
        # return/throw something to indicate to user incorrect file format
        # print file name along with it
        raise custom_errors.InvalidColumnsError("Please make sure column names in data files include:\n\n"
                                                "'symbol' for gene names, 'logfc' for DEGs,"
                                                " and 'adj-pvalue' from logfc calculation")
    try:
        check_col_names(df)
    except custom_errors.InvalidColumnsError as e:
        print("*****ERROR*****\n\nPlease make sure %s is formatted correctly.".format(infer_file_name(path)))
    df = df.set_index('symbol')
    df = df.astype({'logfc': 'float64', "adj-pvalue": 'float64'})
    return df


def check_col_names(df: pd.DataFrame):
    cols = df.columns.values.tolist()
    cols.append(df.index.name)
    required_cols = ['symbol', 'logfc', 'adj-pvalue']
    for col in required_cols:
        if col not in cols:
            # throw error for missing/incorrect col names
            raise custom_errors.InvalidColumnsError

    return df


def infer_file_name(path):
    """
    Dataframes of imported data will be hashed to the name of the file. All of the files should reside
    in the same folder
    :return:
    """
