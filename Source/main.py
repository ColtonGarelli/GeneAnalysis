"""
Gene Analysis project

"""
# import file_in
# import modify_dataframes
# import Visualization.heatmap as heatmap
# import Visualization.volcano as volcano
# import matplotlib.pyplot as plt
# import os
# import ntpath


# def make_a_heatmap():
#     dfs = list()
#     paths = [os.path.join("/Users/coltongarelli/Dropbox/toptables/scle_toptable_abs-logfc-1.csv"),
#              os.path.join("/Users/coltongarelli/Dropbox/toptables/acle_toptable_abs-logfc-1.csv"),
#              os.path.join("/Users/coltongarelli/Dropbox/toptables/dle_toptable_abs-logfc-1.csv")]
#
#     for i in paths:
#         cols = file_in.check_col_names(i)
#         df = file_in.read_csv_data(i, cols)
#         # df = file_in.make_unique_index(df)
#         # drop duplicate values
#         df = modify_dataframes.remove_duplicate_indicies(df)
#         # remove unneeded data
#         df = file_in.strip_data(df, cols.copy())
#         dfs.append(df)
#     counter = 0
#
#     for i in dfs:
#         new_name = 'logfc_' + str(counter)
#         # give columns a unique name
#         i.rename(columns={cols['logfc']: new_name}, inplace=True)
#         counter += 1
#         # pop pvalue
#         modify_dataframes.drop_cols(i, cols['pval'])
#     final_df = modify_dataframes.find_common_genes(dfs)
#     hm = heatmap.sns_clustermap(df=final_df)
#     # heatmap.sns_heatmap(final_df)
#     hm.fig.show()
#
# def volcano_plotly():
#     paths = [os.path.join("/Users/coltongarelli/Dropbox/toptables/scle_toptable_abs-logfc-1.csv")]
#     for i in paths:
#         cols = file_in.check_col_names(i)
#         df = file_in.read_csv_data(i, cols)
#         # df = file_in.make_unique_index(df)
#         # drop duplicate values
#         df = modify_dataframes.remove_duplicate_indicies(df)
#         # remove unneeded data
#         df = file_in.strip_data(df, cols.copy())
#
#     volcano.plotly_volcano(df, cols['pval'])

if __name__ == '__main__':
    import os
    import pprint
    pprint.pprint(os.getenv('PATH'))

    pprint.pprint(os.environ.values())
# '/Library/Frameworks/Python.framework/Versions/3.7/bin:/Users/coltongarelli/anaconda3/envs/GeneAnalysis/bin:/Users/coltongarelli/anaconda3/condabin:/Library/Frameworks/Python.framework/Versions/3.6/bin:/Library/Frameworks/Python.framework/Versions/3.6/bin:/Library/Frameworks/Python.framework/Versions/3.6/bin:/Users/coltongarelli/anaconda3/bin:/Library/Frameworks/Python.framework/Versions/3.5/bin:/Library/Frameworks/Python.framework/Versions/3.5/bin:/Library/Frameworks/Python.framework/Versions/3.5/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin'
