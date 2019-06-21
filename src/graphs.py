from src.controller.generate_output_data import OutputData
from src.controller.utils import get_version_number

output = OutputData(get_version_number)
output.read_dfs_data_from_json()
output.graph_dfs()
