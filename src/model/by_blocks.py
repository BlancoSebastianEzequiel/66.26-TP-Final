import numpy as np
from src.model.multiply_matrices_interface import MultiplyMatricesInterface
from src.controller.utils import get_partitions


class ByBlocks(MultiplyMatricesInterface):

    @staticmethod
    def pre_processing(matrix_a, matrix_b):
        output = []
        blocks_a = get_partitions(matrix_a, 2, 2)
        blocks_b = get_partitions(matrix_b, 2, 2)
        for idx, elem_a in enumerate(blocks_a):
            r, c, block = elem_a
            row_blocks = []
            for elem_b in blocks_b:
                r_b, c_b, a_block_b = elem_b
                if c == r_b:
                    row_blocks.append((a_block_b, c_b))
            output.append((r, c, block, row_blocks))
        return output

    @staticmethod
    def map_worker(chunk):
        r, c, block_a, blocks_b = chunk
        output = []
        for elem in blocks_b:
            block, c_b = elem
            result = np.matmul(block_a, block).tolist()
            key = (r, c_b)
            output.append((key, result))
        return output

    @staticmethod
    def reduce_worker(item):
        output_pos, values = item
        result = []
        size = len(values)
        for idx in range(0, size-1):
            partial_add = np.add(values[idx], values[idx+1]).tolist()
            if not result:
                result = partial_add
            else:
                result = np.add(partial_add, result.copy()).tolist()
        output = []
        row_size = len(result)
        block_pos_i, block_pos_j = output_pos
        for i in range(0, row_size):
            col_size = len(result[i])
            for j in range(0, col_size):
                pos = (block_pos_i*row_size+i, block_pos_j*col_size+j)
                output.append((pos, result[i][j]))
        return output
