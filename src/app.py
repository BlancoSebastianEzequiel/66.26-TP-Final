import sys
from src.controller.measurer import Measurer
from src.controller.map_reduce import MapReduce
from src.controller.utils import get_random_matrix_of_dim_n
from src.model.element_by_row_block import ElementByRowBlock
from src.controller.generate_output_data import OutputData


def gustafson():
    print(f"------------RUNNING GUSTAFSON------------")
    output_data = OutputData()
    for matrix_dim in [2, 4, 8, 16, 32, 64]:
        print(f"RUNNING WITH MATRIX DIMENSION: {matrix_dim}")
        serial, parallel = run(4, matrix_dim, 0.5, 0.5)
        output_data.add_data(serial, parallel, 4, matrix_dim)
    output_data.save_data('gustafson_output.png')
    output_data.graph_gustafson_exec_time('gustafson_exec_time.png')
    output_data.graph_gustafson_speed_up('gustafson_speed_up.png')
    output_data.save_df_data_to_json()


def amdahl():
    print(f"------------RUNNING AMDAHL------------")
    output_data = OutputData()
    for num_workers in [1, 2, 4, 8, 16, 32]:
        print(f"RUNNING WITH NUM WORKERS: {num_workers}")
        serial, parallel = run(num_workers, 10, 0.5, 0.5)
        output_data.add_data(serial, parallel, num_workers, 10)
    output_data.save_data('amdahl_output.png')
    output_data.graph_amdahl_speed_up('amdahl_speed_up.png')
    output_data.save_df_data_to_json()


def run(num_workers, matrix_dim, serial_min_error, parallel_min_error):

    parallel = Measurer()
    serial = Measurer()
    map_worker = ElementByRowBlock.map_worker
    reduce_worker = ElementByRowBlock.reduce_worker
    mapper = MapReduce(map_worker, reduce_worker)

    matrix_a = get_random_matrix_of_dim_n(matrix_dim)
    matrix_b = get_random_matrix_of_dim_n(matrix_dim)

    input_data = ElementByRowBlock.pre_processing(matrix_a, matrix_b)

    for i in range(500):
        partitioned_data = mapper.map(input_data, num_workers=num_workers)
        mapper.reduce(partitioned_data)

        statistics = mapper.get_statistics()
        parallel_time = statistics.get_time_elapsed('parallel')
        serial_time = statistics.get_time_elapsed('serial')

        parallel.add_value(parallel_time)
        serial.add_value(serial_time)
        sys.stdout.flush()
        if i <= 10:
            continue
        is_serial_error_lower = serial.get_error() < serial_min_error
        is_parallel_error_lower = parallel.get_error() < parallel_min_error
        if is_serial_error_lower and is_parallel_error_lower:
            print(f"i: {i}")
            return serial, parallel
    print(f"i: {i}")
    return serial, parallel


# OutputData.delete_all_data()
amdahl()
gustafson()
