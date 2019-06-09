from src.model.by_blocks import ByBlocks
from tests.conftest import multiply_matrices


def test_simple_multiplication():
    multiply_matrices(ByBlocks)
