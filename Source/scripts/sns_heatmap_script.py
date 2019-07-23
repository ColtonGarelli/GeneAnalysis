import Source.file_in as file_in
import Source.modify_dataframes as modify_dataframes
import Source.Visualization.heatmap as heatmap
import os
import ntpath
from rpy2 import robjects
import rpy2

# obj = robjects.DataFrame(rpy2.robjects.)

master_dfs = list()
file_dir = None
# files = os.listdir(file_dir)
# paths = [os.path.join(file_dir, path) for path in files]
paths = ""
# paths = input("input the path of a file containing file names for data to be analyzed, or hit enter: ")
if paths is "":
    paths = [os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/B19-639-A_07-logfc.csv"),
             os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/B19-1182_06-logfc.csv"),
             os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/GSE113113_late_avg.csv"),
             os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/GSE113113_early_avg.csv")]
             # os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/formatted/GSE81071_scle_healthyvscle_formatted.csv"),
             # os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/formatted/GSE81071_cdle_healthyvdle_formatted.csv")

paths = os.path.join('/Users/coltongarelli/Desktop/Geo data for comps/other_disease_ratios.csv')
for i in paths:
    cols = file_in.check_col_names(i)
    df = file_in.read_csv_data(i, cols)
    # df = file_in.make_unique_index(df)
    # drop duplicate values
    df = modify_dataframes.remove_duplicate_indicies(df)
    # remove unneeded data
    to_pop = list()
    # TODO remove requirement for pvalue (or other empty required field)....should probably think of a better soln
    for k, v in cols.items():
        if v is None:
            to_pop.append(k)
    for i in to_pop:
        cols.pop(i)
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
    if 'pval' in cols.keys():
        modify_dataframes.drop_cols(working_dfs[i], cols['pval'])
final_df = modify_dataframes.find_common_genes(working_dfs)
# final_df = modify_dataframes.drop_genes(final_df, ["CXCL11", "CCL2", "CXCL10"])
hm = heatmap.sns_clustermap(df=final_df)
# heatmap.simple_clustermap(final_df)
# hm.fig.show()
