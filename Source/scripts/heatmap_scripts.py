import functions.file_in as file_in
import functions.modify_dataframes as modify_dataframes
import Source.Visualization.heatmap as heatmap
import os
import matplotlib.pyplot as plt

master_dfs = list()
path = '/Users/coltongarelli/Desktop/Geo data for comps/Canine Nanostring data/log2fc_all_diseases'
files = [os.path.join(path, i) for i in os.listdir(path)]
# file = path
for file in files:

    cols = file_in.check_col_names(file)
    df = file_in.read_csv_data(file, cols)
    # df.set_index('symbol', inplace=True)
    if df.empty:
        pass
    else:
        master_dfs.append(df)

working_dfs = list()
final_df = modify_dataframes.find_common_genes(master_dfs)
# Cutting off top and bottom row should be fixed in mpl 3.1.2
hm = heatmap.sns_clustermap(final_df)
hm.savefig("/Users/coltongarelli/Desktop/{}_clustermap.png".format("test"))
