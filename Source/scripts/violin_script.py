from Visualization.violin import violin_plot
from data_processing import file_in, modify_dataframes
import matplotlib.pyplot as plt
import gene_stats

path = '/Users/coltongarelli/Desktop/Geo data for comps/working files/all_lupus.csv'
# files = [os.path.join(path, i) for i in os.listdir(path)]
file = path
# for i in files:
cols = file_in.check_col_names(file)
df = file_in.read_csv_data(file, cols)
# df = df.set_index('genes')
df = modify_dataframes.remove_duplicate_indicies(df)
df = gene_stats.quantile_norm(df)
violin_plot(df, genes=['IL-16'], cols=cols)
plt.show()


