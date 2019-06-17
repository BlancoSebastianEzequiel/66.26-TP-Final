from src.model.by_blocks import ByBlocks
from tests.conftest import multiply_matrices
from src.controller.utils import get_random_matrix_of_dim_n


def test_simple_multiplication():
    matrix_a = get_random_matrix_of_dim_n(4)
    matrix_b = get_random_matrix_of_dim_n(4)
    multiply_matrices(ByBlocks, matrix_a, matrix_b, 4)

    matrix_a = get_random_matrix_of_dim_n(4)
    matrix_b = get_random_matrix_of_dim_n(4)
    multiply_matrices(ByBlocks, matrix_a, matrix_b, 3)

    matrix_a = get_random_matrix_of_dim_n(64)
    matrix_b = get_random_matrix_of_dim_n(64)
    multiply_matrices(ByBlocks, matrix_a, matrix_b, 4)
