from src.controller.generate_output_data import OutputData

output = OutputData()
output.read_dfs_data_from_json()
output.graph_dfs()

dgemm_output_data = OutputData()
dgemm_df = dgemm_output_data.get_df_from_csv("src/data/dgemm.csv")
dgemm_output_data.save_df_in_image(dgemm_df, "dgemm.png")
