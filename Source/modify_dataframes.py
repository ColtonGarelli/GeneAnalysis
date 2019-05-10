# pd.concat([df3, df.get('time'), df.get('40')], axis=1) to concat columns
# values = new_df.loc[~new_df['40'].isin(range(-1,1))] to exclude things b/t -1,1
# pvals.append(float(decimal.Decimal(random.randrange(1, 1000))/10000))

import pandas as pd


def value_cutoff(df: pd.DataFrame, col_name, upper, lower=None):
    """Removes rows containing values **WITHIN** the given range (upper, lower) in the specified column in the df passed

    A df containing data is passed in. The function removes the entire row when a value contained in the specified column
    (col_name) falls within the range. For log2FC DEG analysis, upper and lower bounds should be provided. Only a lower
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
    """Takes a list of dataframes and returns a dataframe containing only common genes.

    Filter out uncommon genes from a set of dataframes. Useful for comparing gene targets from different
    tissues/cell types/diseases where constitutive expression may vary.
    Args:
        frames: a list of Pandas DataFrames containing transcription data

    Returns:
        A Pandas DataFrame where

    """
    # Drop values that don't have shared genes (symbol column)
    common = pd.DataFrame()
    for i1 in range(len(frames)-1):
        # frame1_dtype = frames[i1].dtypes.to_dict()
        # frame2_dtype = frames[i1+1].dtypes.to_dict()
        if i1 == 0:
            common = frames[i1].join(frames[i1+1], how='inner')
        else:
            temp = common.copy(deep=True)
            temp = temp.join(frames[i1+1], how='inner')
            if not temp.empty:
                common = temp
            else:
                # If nothing in common between two of the frames
                # Return empty frame
                return pd.DataFrame()
    return common
