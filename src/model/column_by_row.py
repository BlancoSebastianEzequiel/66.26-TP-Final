from src.model.multiply_matrices_interface import MultiplyMatricesInterface


class ColumnByRow(MultiplyMatricesInterface):

    @staticmethod
    def pre_processing(matrix_a, matrix_b, **kwargs):
        N = len(matrix_a)
        output = []
        for i in range(0, N):
            col_a = [row[i] for row in matrix_a]
            output.append((col_a, matrix_b[i]))
        return output

    @staticmethod
    def map_worker(chunk):
        col_a, row_b = chunk
        output = []
        for row, elem_a in enumerate(col_a):
            for col, elem_b in enumerate(row_b):
                key = (row, col)
                value = elem_a * elem_b
                output.append((key, value))
        return output

    @staticmethod
    def reduce_worker(item):
        output_pos, values = item
        result = 0
        for a_value in values:
            result += a_value
        return output_pos, result
