import numpy as np
from src.model.multiply_matrices_interface import MultiplyMatricesInterface
from src.controller.map_reduce import MapReduce
from typing import Type


def multiply_matrices(model: Type[MultiplyMatricesInterface]):
    matrix_a = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    matrix_b = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]

    expected_result = np.matmul(matrix_a, matrix_b)

    map_worker = model.map_worker
    reduce_worker = model.reduce_worker
    mapper = MapReduce(map_worker, reduce_worker)
    input_data = model.pre_processing(matrix_a, matrix_b)

    partitioned_data = mapper.map(input_data, num_workers=4)
    actual_result = mapper.reduce(partitioned_data)
    for elem in actual_result:
        if isinstance(elem, list):
            for value_info in elem:
                pos, value = value_info
                i, j = pos
                assert expected_result[i][j] == value
        else:
            pos, value = elem
            i, j = pos
            assert expected_result[i][j] == value
