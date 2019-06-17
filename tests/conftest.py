import numpy as np
from math import ceil
from src.model.multiply_matrices_interface import MultiplyMatricesInterface
# from src.controller.threaded import Threaded as MapReduce
from src.controller.pool import Pool as MapReduce
from typing import Type


def multiply_matrices(
        model: Type[MultiplyMatricesInterface],
        matrix_a,
        matrix_b,
        num_workers
):

    expected_result = np.matmul(matrix_a, matrix_b)

    map_worker = model.map_worker
    reduce_worker = model.reduce_worker
    mapper = MapReduce(map_worker, reduce_worker)

    div = ceil(len(matrix_a) / 2)
    input_data = model.pre_processing(matrix_a, matrix_b, row_p=div, col_p=div)

    mapped_data = mapper.map(input_data, num_workers=num_workers)
    actual_result = mapper.reduce(mapped_data)
    assert actual_result

    for elem in actual_result:
        if isinstance(elem, list):
            for value_info in elem:
                pos, value = value_info
                i, j = pos
                assert np.isclose(expected_result[i][j], value)
        else:
            pos, value = elem
            i, j = pos
            assert np.isclose(expected_result[i][j], value)
