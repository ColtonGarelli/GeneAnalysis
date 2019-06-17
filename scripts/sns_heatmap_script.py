import Source.file_in as file_in
import Source.modify_dataframes as modify_dataframes
import Source.Visualization.heatmap as heatmap
import os
import ntpath

master_dfs = list()
file_dir = None
# files = os.listdir(file_dir)
# paths = [os.path.join(file_dir, path) for path in files]
paths = ""
# paths = input("input the path of a file containing file names for data to be analyzed, or hit enter: ")
if paths is "":
    paths = [os.path.join("/Users/coltongarelli/Dropbox/toptables/scle_toptable_abs-logfc-3.csv"),
             os.path.join("/Users/coltongarelli/Dropbox/toptables/acle_toptable_abs-logfc-3.csv"),
             # os.path.join("/Users/coltongarelli/Dropbox/toptables/kidney_toptable_abs-logfc-3.csv"),
             os.path.join("/Users/coltongarelli/Dropbox/toptables/dle_toptable_abs-logfc-3.csv")]

for i in paths:
    cols = file_in.check_col_names(i)
    df = file_in.read_csv_data(i, cols)
    # df = file_in.make_unique_index(df)
    # drop duplicate values
    df = modify_dataframes.remove_duplicate_indicies(df)
    # remove unneeded data
    df = file_in.strip_data(df, cols.copy())
    master_dfs.append(df)

working_dfs = [i.copy(deep=True) for i in master_dfs]
counter = 0
for i in range(len(working_dfs)):
    new_name = 'logfc_' + str(counter)
    # give columns a unique name
    temp = working_dfs[i].copy(deep=True)
    temp.rename(columns={cols['logfc']: 'log$_2$FC of {}'.format(ntpath.basename(paths[i]).split('.')[0])}, inplace=True)
    working_dfs[i] = temp
    counter += 1
    # pop pvalue
    modify_dataframes.drop_cols(working_dfs[i], cols['pval'])
final_df = modify_dataframes.find_common_genes(working_dfs)
hm = heatmap.sns_clustermap(df=final_df, title="Clustermap")
# heatmap.sns_heatmap(final_df)
hm.fig.show()
