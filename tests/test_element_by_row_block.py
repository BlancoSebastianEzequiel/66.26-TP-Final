from src.model.element_by_row_block import ElementByRowBlock
from tests.conftest import multiply_matrices


def test_simple_multiplication():
    multiply_matrices(ElementByRowBlock)
