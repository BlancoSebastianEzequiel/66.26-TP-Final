from src.controller.generate_output_data import OutputData
from src.controller.utils import get_version_number

output = OutputData(get_version_number)
output.read_dfs_data_from_json()
output.graph_dfs()

dgemm_output_data = OutputData(get_version_number, avoid=True)
dgemm_df = dgemm_output_data.get_df_from_csv("src/data/dgemm.csv")
dgemm_output_data.save_df_in_image(dgemm_df, "dgemm.png")
