import functions.file_in as file_in
import Source.Visualization.heatmap as heatmap
import os
import matplotlib.pyplot as plt


master_dfs = list()
path = '/Users/coltongarelli/Desktop/Geo data for comps/working files/all_lupus.csv'
# files = [os.path.join(path, i) for i in os.listdir(path)]
file = path
# for i in files:
cols = file_in.check_col_names(file)
df = file_in.read_csv_data(file, cols)
hm = heatmap.sns_clustermap(df)
hm.savefig(os.path.join("/Users/coltongarelli/Desktop/Richmond Lab/Plots/Canine plots/", "{}_clustermap.png".format("Lupus")))


master_dfs.append(df)

# genes_of_interest = ["IL16", "TSLP", "CXCL8", "CXCL10",
#                      "CXCL11", "CXCL12", "CCL20", "CXCL13", "CXCL16",
#                      "CXCL14", "CX3CL1", "CCL1", "CCL2",
#                      "CCL3", "CCL4", "CCL5", "CCL7", "CCL8",
#                      "CCL13", "CCL23", "CCL16", "CCL17", "CCL19",
#                      "CCL20", "CCL21", "CCL22", "CCL24", "CCL25",
#                      "CCL26", "CCL27", "CCL28", "PPBP", "CXCL17"]
# genes_of_interest = pd.read_csv('/Users/coltongarelli/Desktop/Geo data for comps/working files/panels.csv')
# # genes = master_dfs[0].index.to_list()
# # genes_to_keep = [gene for gene in genes if gene in genes_of_interest]



# for genes in genes_of_interest:
#     final_df = pd.DataFrame()
#     print(genes)
#     for i in master_dfs:
#
#         if final_df.empty:
#             final_df = modify_dataframes.drop_genes(i.copy(deep=True), genes_of_interest[genes].dropna().to_list())
#         else:
#             final_df = final_df.join(modify_dataframes.drop_genes(i.copy(deep=True), genes_of_interest[genes].dropna().to_list()))
#     hm = heatmap.sns_clustermap(final_df, genes)
#     hm.savefig(os.path.join("/Users/coltongarelli/Desktop/Richmond Lab/Plots/Canine plots/", "{}_clustermap_all_diseases.png".format(genes)))

# final_df = modify_dataframes.find_common_genes(master_dfs)


plt.show()




