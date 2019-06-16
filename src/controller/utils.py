import numpy as np
from math import ceil


def column(matrix, i):
    return [row[i] for row in matrix]


def get_random_matrix_of_dim_n(N):
    random_matrix = np.random.randint(low=1, high=255, size=(N, N))
    for i in range(0, N):
        random_matrix[i] = random_matrix[i].tolist()
    return random_matrix.tolist()


def get_null_matrix_of_dim_n(N):
    random_matrix = np.zeros((N, N))
    for i in range(0, N):
        random_matrix[i] = random_matrix[i].tolist()
    return random_matrix.tolist()


def get_partitions(matrix, row_p, col_p):
    N = len(matrix)
    col_size_p = ceil(N/col_p)
    row_size_p = ceil(N/row_p)
    blocks = array_to_list(np.zeros((row_p, col_p)))
    for r in range(0, row_p):
        for c in range(0, col_p):
            left_side = c * col_size_p
            right_side = left_side + col_size_p
            up_side = r * row_size_p
            down_side = up_side + row_size_p
            rows = matrix[up_side:down_side]
            block = []
            for row in rows:
                block.append(row[left_side:right_side])
            blocks[r][c] = block.copy()
    return blocks


def multiply_two_matrices(matrix_a, matrix_b):
    rows_a = len(matrix_a)
    cols_b = len(matrix_b[0])
    cols_a = len(matrix_a[0])
    multiplication = array_to_list(np.zeros((rows_a, cols_b)))
    for i in range(0, rows_a):
        for j in range(0, cols_b):
            partial_sum = 0
            for k in range(0, cols_a):
                partial_sum += matrix_a[i][k] * matrix_b[k][j]
            multiplication[i][j] = partial_sum
    return multiplication


def sum_matrices(matrices):
    rows = len(matrices[0])
    cols = len(matrices[0][0])
    result = array_to_list(np.zeros((rows, cols)))
    for i in range(0, rows):
        for j in range(0, cols):
            for matrix in matrices:
                result[i][j] += matrix[i][j]
    return result


def array_to_list(array):
    rows = len(array)
    for i in range(0, rows):
        array[i] = array[i].tolist()
    return array.tolist()


def print_matrix(matrix):
    rows = len(matrix)
    for i in range(0, rows):
        print(f"{matrix[i]}\n")


def chunks(a_list, num):
    """
    :param a_list: a list to split in n chunks
    :param num: number of chunks
    :return: list splitted
    """
    avg = len(a_list) / float(num)
    out = []
    last = 0.0
    while last < len(a_list):
        out.append(a_list[int(last):int(last + avg)])
        last += avg
    return out
