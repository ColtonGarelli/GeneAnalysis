import os
from functions import file_in, gene_stats
import Visualization.stat_plots as stat_plots

master_dfs = list()
# paths = [os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/B19-639-A_07-logfc.csv"),
#              os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/B19-1182_06-logfc.csv"),
#              os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/GSE113113_late_avg.csv"),
#              os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/GSE113113_early_avg.csv")]
# exp1 = [os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/B19-639-A_07-logfc.csv"),
#         os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/B19-1182_06-logfc.csv")]
#
#
#
# expr1_df = pd.DataFrame()
# for i in exp1:
#     cols = file_in.check_col_names(i)
#     df = file_in.read_csv_data(i, cols)
#     df = modify_dataframes.remove_duplicate_indicies(df)
#     to_pop = list()
#     # TODO remove requirement for pvalue (or other empty required field)....should probably think of a better soln
#     for k, v in cols.items():
#         if v is None:
#             to_pop.append(k)
#     for i in to_pop:
#         cols.pop(i)
#     df = file_in.strip_data(df, cols.copy())
#     expr1_df = pd.concat([expr1_df, df], axis=1)
# exp2 = [os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/GSE113113_late_avg.csv"),
#         os.path.join("/Users/coltongarelli/Desktop/GEO data for comps/GSE113113_early_avg.csv")]
# expr2_df = pd.DataFrame()
# for i in exp2:
#     cols = file_in.check_col_names(i)
#     df = file_in.read_csv_data(i, cols)
#     df = modify_dataframes.remove_duplicate_indicies(df)
#     to_pop = list()
#     # TODO remove requirement for pvalue (or other empty required field)....should probably think of a better soln
#     for k, v in cols.items():
#         if v is None:
#             to_pop.append(k)
#     for i in to_pop:
#         cols.pop(i)
#     df = file_in.strip_data(df, cols.copy())
#     expr2_df = pd.concat([expr2_df, df], axis=1)

path = '/Users/coltongarelli/Desktop/Geo data for comps/working files/all_disease_ratios.csv'
if path[-1] == "v":
    paths = os.path.join(path)
else:
    paths = [os.path.join(path, i) for i in os.listdir(path)]
if isinstance(paths, list):
    for i in paths:
        cols = file_in.check_col_names(i)
        df = file_in.read_csv_data(i, cols)
        if df.empty:
            pass
        elif df.shape[1] == 1:
            master_dfs.append(df)
        else:
            master_dfs = df
else:
    cols = file_in.check_col_names(paths)
    master_dfs = file_in.read_csv_data(paths, cols)

# transformed = gene_stats.quantile_norm([expr1_df, expr2_df])

post_pca, rows = gene_stats.pca_calculation(master_dfs)
# cols1 =
plot, ax = stat_plots.plot_pca(post_pca, rows)
# plt.xlabel("Principal Component 1")
# plt.ylabel("Principal Component 2")
plot.savefig('full_profile_nanostring_2.png', bbox_inches='tight')


