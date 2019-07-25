# pd.concat([df3, df.get('time'), df.get('40')], axis=1) to concat columns
# values = new_df.loc[~new_df['40'].isin(range(-1,1))] to exclude things b/t -1,1
# pvals.append(float(decimal.Decimal(random.randrange(1, 1000))/10000))
import pandas as pd


def value_cutoff(df: pd.DataFrame, col_name, upper, lower=None):
    """Removes rows containing values above an upper bound or **within** a range (upper, lower)...(NON-INCLUSIVE)

    A df containing data is passed in. The function removes the entire row when a value contained in the specified column
    (col_name) falls within the range. For logFC DEG analysis, upper and lower bounds should be provided. Only a lower
    bound is required for p-values (will remove everything >lower bound).


    This function is intended to reduce memory load, specifically for efficient, non-laggy Plotly plots.

    Args:
        upper: An upper bound to eliminate genes from the passed df
        lower: A lower bound to eliminate genes from the passed df
        df: A df containing desired data to modify
        col_name: The column containing the data the function will

    Returns: A Dataframe containing only the filtered data

    """
    if lower is None:
        # everything less than the upperbound
        new_df = df[df[col_name] < upper]
        return new_df
    else:
        new_df = pd.DataFrame(df[df[col_name] < lower])
        new_df = pd.concat([new_df, df[df[col_name] > upper]])
        return new_df


def find_common_genes(frames: [pd.DataFrame]):
    """Takes a list of DataFrames and returns a DataFrame containing genes common between all DataFrames in the list.

    Filter out uncommon genes from a set of DataFrame. Useful for comparing gene targets from different
    tissues/cell types/diseases where constitutive expression may vary.
    Args:
        frames: a list of Pandas DataFrames containing transcription data

    Returns:
        A Pandas DataFrame only with genes that overlap between all DataFrames in frames

    """
    # Drop values that don't have shared genes (symbol column)
    common = pd.DataFrame()
    for i1 in range(len(frames)-1):
        counter1 = 0
        counter2 = 1
        if i1 == 0:
            common = frames[i1].join(frames[i1+1], lsuffix=str("_" + (str(counter1))),
                                     rsuffix=str("_" + (str(counter2))), how='inner')
            counter1 += 2
            counter2 += 2
        else:
            temp = common.copy(deep=True)
            temp = temp.join(frames[i1+1], how='inner', lsuffix=str("_" + (str(counter1))),
                             rsuffix=str("_" + (str(counter2))))
            counter1 += 2
            counter2 += 2
            if not temp.empty:
                common = temp.copy(deep=True)
            else:
                # If nothing in common between two of the frames
                # Return empty frame
                return pd.DataFrame()
    return common


def drop_cols(df: pd.DataFrame, cols_to_drop):
    """Drop columns from a list of column names.


    TODO: Duplicate of file_in.strip_data
    Args:
        df:
        cols_to_drop:

    Returns:

    """
    return df.drop(columns=cols_to_drop, inplace=True)


def drop_genes(df: pd.DataFrame, genes: list):
    """
    Drops undesired genes from a DataFrame

    Args:
        df:
        genes:

    Returns:

    """
    return_df = pd.DataFrame(columns=df.columns)
    count = 00
    for i in df.index.tolist():
        if i in genes:
            if count == 0:
                temp = df.loc[[i]]
                return_df = temp
            else:
                temp = df.loc[[i]]
                return_df = return_df.append(temp)
            count += 1
    return return_df


def remove_duplicate_indicies(df: pd.DataFrame):
    """
    Keeps first instance of a gene/index and removes the others

    Args:
        df:

    Returns:

    """
    return df.loc[~df.index.duplicated(keep='first')]

