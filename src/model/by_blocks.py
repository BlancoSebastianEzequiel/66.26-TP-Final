import numpy as np
from src.model.multiply_matrices_interface import MultiplyMatricesInterface
from src.controller.utils import get_partitions, sum_matrices


class ByBlocks(MultiplyMatricesInterface):

    @staticmethod
    def pre_processing(matrix_a, matrix_b, **kwargs):
        output = []
        row_p = kwargs.get('row_p', 2)
        col_p = kwargs.get('col_p', 2)
        blocks_a = get_partitions(matrix_a, row_p, col_p)
        blocks_b = get_partitions(matrix_b, row_p, col_p)
        for r_a in range(0, row_p):
            for c_a in range(0, col_p):
                a_block = blocks_a[r_a][c_a]
                output.append((r_a, a_block, blocks_b[c_a]))
        return output

    @staticmethod
    def map_worker(chunk):
        r_a, block_a, blocks_b = chunk
        output = []
        col_size = len(blocks_b)
        for c_b in range(0, col_size):
            result = np.matmul(block_a, blocks_b[c_b]).tolist()
            key = (r_a, c_b)
            output.append((key, result))
        return output

    @staticmethod
    def reduce_worker(item):
        output_pos, values = item
        result = sum_matrices(values)
        output = []
        row_size = len(result)
        block_pos_i, block_pos_j = output_pos
        for i in range(0, row_size):
            col_size = len(result[i])
            for j in range(0, col_size):
                pos = (block_pos_i*row_size+i, block_pos_j*col_size+j)
                output.append((pos, result[i][j]))
        return output
