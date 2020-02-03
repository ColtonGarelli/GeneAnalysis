from data_processing import file_in as file_in, modify_dataframes
import Visualization.volcano
import os
import pandas as pd
import ntpath
import matplotlib.pyplot as plt

master_dfs = list()
paths = "/Users/coltongarelli/Desktop/GEO data for comps/Canine Nanostring data/dle vs ref with pvalue.csv"
# paths = input("input the path of a file containing file names for data to be analyzed, or hit enter: ")
if paths is "":
    paths = [os.path.join("/Users/coltongarelli/Dropbox/toptables/scle_toptable_abs-logfc-1.csv"),
             os.path.join("/Users/coltongarelli/Dropbox/toptables/acle_toptable_abs-logfc-1.csv"),
             os.path.join("/Users/coltongarelli/Dropbox/toptables/dle_toptable_abs-logfc-1.csv")]

if isinstance(paths, list):
    for i in paths:
        cols = file_in.check_col_names(i, pvalue=True)
        df = file_in.read_csv_data(i, cols)
        # drop duplicate values
        df = modify_dataframes.remove_duplicate_indicies(df)
        # remove unneeded data
        df = file_in.strip_data(df, cols.copy())
        # add to the master list of dfs
        master_dfs.append(df)
else:
    cols = file_in.check_col_names(paths, pvalue=True)
    df = file_in.read_csv_data(paths, cols)
    df = modify_dataframes.remove_duplicate_indicies(df)
    # df = file_in.strip_data(df, cols.copy())
    master_dfs = df.copy(deep=True)

counter = 0
working_dfs = list()
if isinstance(master_dfs, list):
    for i in master_dfs:
        working_dfs.append(i.copy(deep=True))
else:
    working_dfs = [master_dfs.copy()]

# for i in range(len(working_dfs)):
#     new_log = 'logfc_' + str(counter)
#     new_p = 'adjpval_' + str(counter)
#     working_dfs[i].rename(columns={cols['logfc']: new_log, cols['pval']: new_p})
#     title = ntpath.basename(paths[i]).split('.')[0]
#     deg_df = modify_dataframes.value_cutoff(working_dfs[i], cols['logfc'], 1, -1)
#     for deg in deg_df:
#         deg_df["DEG"] = True
#
#     temp = pd.merge(working_dfs[i], deg_df["DEG"], left_index=True, right_index=True, how='left')
#     temp = temp.fillna(False)
#     plot = Visualization.volcano.seaborn_volcano_plot(d=temp, colnames=cols, title=title)
#     plt.show()
new_log = 'logfc' + str(counter)
new_p = 'adjpval' + str(counter)
title = ntpath.basename(paths[2]).split('.')[0]

working_dfs[0].rename(columns={cols['logfc']: new_log, cols['pval']: new_p})
plot = Visualization.volcano.sns_volcano(d=working_dfs[0], colnames=cols, title=title)
plot.get_figure().savefig('testing_volcano.png', format='png', dpi=400)
