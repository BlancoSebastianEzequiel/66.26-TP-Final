from src.model.column_by_row import ColumnByRow
from tests.conftest import multiply_matrices


def test_simple_multiplication():
    multiply_matrices(ColumnByRow)
