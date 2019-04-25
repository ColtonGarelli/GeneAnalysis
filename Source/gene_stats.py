import pandas as pd
# pd.concat([df3, df.get('time'), df.get('40')], axis=1) to concat columns
# values = new_df.loc[~new_df['40'].isin(range(-1,1))] to exclude things b/t -1,1
# pvals.append(float(decimal.Decimal(random.randrange(1, 1000))/10000))

def value_cutoff(*upper, lower, df, col_name):
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



