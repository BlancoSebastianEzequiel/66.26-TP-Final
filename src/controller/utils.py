import numpy as np
from math import ceil


def column(matrix, i):
    return [row[i] for row in matrix]


def get_random_matrix_of_dim_n(N):
    random_matrix = np.random.rand(N, N)
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
    blocks = []
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
            blocks.append((r, c, block))
    return blocks
