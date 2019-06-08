from src.controller.generate_output_data import OutputData

output = OutputData()
output.read_dfs_data_from_json()
output.graph_dfs()
