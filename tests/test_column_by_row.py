from src.model.column_by_row import ColumnByRow
from tests.conftest import multiply_matrices
from src.controller.utils import get_random_matrix_of_dim_n


def test_simple_multiplication():
    matrix_a = get_random_matrix_of_dim_n(64)
    matrix_b = get_random_matrix_of_dim_n(64)
    multiply_matrices(ColumnByRow, matrix_a, matrix_b, 1)

    matrix_a = get_random_matrix_of_dim_n(64)
    matrix_b = get_random_matrix_of_dim_n(64)
    multiply_matrices(ColumnByRow, matrix_a, matrix_b, 3)

    matrix_a = get_random_matrix_of_dim_n(64)
    matrix_b = get_random_matrix_of_dim_n(64)
    multiply_matrices(ColumnByRow, matrix_a, matrix_b, 4)
