import numpy as np


def multiply_two_matrices(A, B, N):
    C = [[0]*N]*N
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k]*B[k][j]
    return C


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


def split(matrix_a, matrix_b):
    row_size = len(matrix_a)
    col_size = len(matrix_a[0])
    output = []
    for i in range(0, row_size):
        for j in range(0, col_size):
            element_by_row_block = [matrix_a[i][j]] + matrix_b[j]
            output.append((i, element_by_row_block))
    return output


def map_worker(chunk):
    output = []
    i, elements = chunk
    elem_a = elements[0]
    elements.pop(0)
    col_size = len(elements)
    for j in range(0, col_size):
        output.append(((i, j), elem_a * elements[j]))
    return output


def reduce_worker(item):
    output_pos, values = item
    result = 0
    for a_value in values:
        result += a_value
    return output_pos, result


def pre_processing(matrices):
    A, B = matrices
    row_size_a = len(A)
    row_size_b = len(B)
    col_size_a = len(A[0])
    col_size_b = len(B[0])
    output = []
    for i in range(0, row_size_a):
        for j in range(0, col_size_a):
            for k in range(0, col_size_b):
                key = (i, k)
                value = ('A', j, A[i][j])
                output.append((key, value))

    for i in range(0, row_size_b):
        for j in range(0, col_size_b):
            for k in range(0, row_size_a):
                key = (k, j)
                value = ('B', i, B[i][j])
                output.append((key, value))
    return output


def multiply(item):
    pos, values = item
    hash_a = {}
    hash_b = {}
    for value in values:
        if value[0] == 'A':
            hash_a[value[1]] = value[2]
        else:
            hash_b[value[1]] = value[2]
    result = 0
    for key in hash_a:
        a_ij = hash_a[key]
        b_ij = hash_b[key]
        result += a_ij * b_ij
    return pos, result


"""
def test_multiply():
    matrix_a = [
        [1, 2],
        [3, 4]
    ]
    matrix_b = [
        [5, 6],
        [7, 8]
    ]
    # 0: (1, 5, 6) => ((0, 0), 1*5) , ((0, 1), 1*6)
    # 0: (2, 7, 8) => ((0, 0), 2*7) , ((0, 1), 2*8)
    # 1: (3, 5, 6) => ((1, 0), 3*5) , ((1, 1), 3*6)
    # 1: (4, 7, 8) => ((1, 0), 4*7) , ((1, 1), 4*8)

    # ((0, 0), 1*5 + 2*7) => (0, 0), 19)
    # ((0, 1), 1*6 + 2*8) => (0, 1), )
    # ((1, 0), 3*5 + 4*7) => (1, 0), )
    # ((1, 1), 3*6 + 4*8) => (1, 1), )

    result = multiply_two_matrices(matrix_a, matrix_b, 2)
    mapper = MapReduce(map_worker, reduce_worker)
    input_data = split(matrix_a, matrix_b)
    partitioned_data = mapper.map(input_data, num_workers=4)
    result_2 = mapper.reduce(partitioned_data)
    print(f"A: {matrix_a}")
    print(f"B: {matrix_b}")
    print(f"result: {result}")
    print(f"result_2: {result_2}")
    return None
"""
