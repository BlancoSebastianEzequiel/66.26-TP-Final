from src.model.multiply_matrices_interface import MultiplyMatricesInterface


class ElementByRowBlock(MultiplyMatricesInterface):

    @staticmethod
    def pre_processing(matrix_a, matrix_b):
        row_size = len(matrix_a)
        col_size = len(matrix_a[0])
        output = []
        for i in range(0, row_size):
            for j in range(0, col_size):
                element_by_row_block = [matrix_a[i][j]] + matrix_b[j]
                output.append((i, element_by_row_block))
        return output

    @staticmethod
    def map_worker(chunk):
        output = []
        i, elements = chunk
        elem_a = elements[0]
        elements.pop(0)
        col_size = len(elements)
        for j in range(0, col_size):
            output.append(((i, j), elem_a * elements[j]))
        return output

    @staticmethod
    def reduce_worker(item):
        output_pos, values = item
        result = 0
        for a_value in values:
            result += a_value
        return output_pos, result
