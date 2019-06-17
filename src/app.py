import time
from typing import Type
from math import ceil
# from src.controller.threaded import Threaded as MapReduce
from src.controller.pool import Pool as MapReduce
from src.controller.utils import get_random_matrix_of_dim_n
from src.model.element_by_row_block import ElementByRowBlock
from src.model.column_by_row import ColumnByRow
from src.model.by_blocks import ByBlocks
from src.model.multiply_matrices_interface import MultiplyMatricesInterface
from src.controller.generate_output_data import OutputData


SAVE = True


def gustafson(model: Type[MultiplyMatricesInterface]):
    name = model.__name__
    print(f"------------RUNNING GUSTAFSON------------")
    output_data = OutputData()
    num_workers = 4
    for matrix_dim in [2, 4, 16, 64, 100, 200, 300]:
        print(f"RUNNING WITH MATRIX DIMENSION: {matrix_dim}")
        serial, parallel = run(num_workers, matrix_dim, model)
        output_data.add_data(serial, parallel, num_workers, matrix_dim)
    if SAVE:
        output_data.save_data(name + '_gustafson_output.png')
        output_data.graph_gustafson_exec_time(name + '_gustafson_exec_time.png')
        output_data.graph_gustafson_speed_up(name + '_gustafson_speed_up.png')
        output_data.save_df_data_to_json()


def amdahl(model: Type[MultiplyMatricesInterface]):
    name = model.__name__
    print(f"------------RUNNING AMDAHL------------")
    output_data = OutputData()
    matrix_dim = 100
    for num_workers in [1, 2, 3, 4, 8, 16, 32, 64, 128]:
        print(f"RUNNING WITH NUM WORKERS: {num_workers}")
        serial, parallel = run(num_workers, matrix_dim, model)
        output_data.add_data(serial, parallel, num_workers, matrix_dim)
    if SAVE:
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


def run_model(model: Type[MultiplyMatricesInterface]):
    print(f"**************************************")
    print(f"{model.__name__}")
    print(f"**************************************")
    amdahl(model)
    gustafson(model)


start = time.time()
if SAVE:
    OutputData.delete_all_data()
run_model(ElementByRowBlock)
run_model(ColumnByRow)
run_model(ByBlocks)
end = time.time()
print(f"**************************************")
print(f"The process lasted {end-start} seconds")
print(f"**************************************")
