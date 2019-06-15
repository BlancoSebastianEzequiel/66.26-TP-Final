from typing import Type
from math import ceil
from src.controller.map_reduce import MapReduce
from src.controller.utils import get_random_matrix_of_dim_n
from src.model.element_by_row_block import ElementByRowBlock
from src.model.column_by_row import ColumnByRow
from src.model.by_blocks import ByBlocks
from src.model.multiply_matrices_interface import MultiplyMatricesInterface
from src.controller.generate_output_data import OutputData


def gustafson(model: Type[MultiplyMatricesInterface], name):
    print(f"------------RUNNING GUSTAFSON------------")
    output_data = OutputData()
    for matrix_dim in [2, 4, 8, 16, 32, 64, 100, 300]:
        print(f"RUNNING WITH MATRIX DIMENSION: {matrix_dim}")
        serial, parallel = run(4, matrix_dim, model)
        output_data.add_data(serial, parallel, 4, matrix_dim)
    output_data.save_data(name + '_gustafson_output.png')
    output_data.graph_gustafson_exec_time(name + '_gustafson_exec_time.png')
    output_data.graph_gustafson_speed_up(name + '_gustafson_speed_up.png')
    output_data.save_df_data_to_json()


def amdahl(model: Type[MultiplyMatricesInterface], name):
    print(f"------------RUNNING AMDAHL------------")
    output_data = OutputData()
    for num_workers in [1, 2, 3, 4, 8, 16, 32]:
        print(f"RUNNING WITH NUM WORKERS: {num_workers}")
        serial, parallel = run(num_workers, 10, model)
        output_data.add_data(serial, parallel, num_workers, 500)
    output_data.save_data(name + '_amdahl_output.png')
    output_data.graph_amdahl_speed_up(name + '_amdahl_speed_up.png')
    output_data.save_df_data_to_json()


def run(num_workers, matrix_dim, model: Type[MultiplyMatricesInterface]):
    map_worker = model.map_worker
    reduce_worker = model.reduce_worker
    mapper = MapReduce(map_worker, reduce_worker)

    matrix_a = get_random_matrix_of_dim_n(matrix_dim)
    matrix_b = get_random_matrix_of_dim_n(matrix_dim)

    div = ceil(matrix_dim/2)

    input_data = model.pre_processing(matrix_a, matrix_b, row_p=div, col_p=div)

    partitioned_data = mapper.map(input_data, num_workers=num_workers)
    mapper.reduce(partitioned_data)

    statistics = mapper.get_statistics()
    parallel_time = statistics.get_time_elapsed('parallel')
    serial_time = statistics.get_time_elapsed('serial')
    return serial_time, parallel_time


# OutputData.delete_all_data()
print(f"**************************************")
print(f"ElementByRowBlock")
print(f"**************************************")
amdahl(ElementByRowBlock, ElementByRowBlock.__name__)

print(f"**************************************")
print(f"ColumnByRow")
print(f"**************************************")
amdahl(ColumnByRow, ColumnByRow.__name__)

print(f"**************************************")
print(f"ByBlocks")
print(f"**************************************")
amdahl(ByBlocks, ByBlocks.__name__)

print(f"**************************************")
print(f"ElementByRowBlock")
print(f"**************************************")
gustafson(ElementByRowBlock, ElementByRowBlock.__name__)

print(f"**************************************")
print(f"ColumnByRow")
print(f"**************************************")
gustafson(ColumnByRow, ColumnByRow.__name__)

print(f"**************************************")
print(f"ByBlocks")
print(f"**************************************")
gustafson(ByBlocks, ByBlocks.__name__)
