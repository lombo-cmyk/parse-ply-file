from unittest.mock import MagicMock
import pytest


@pytest.fixture
def mock_dataframe(expected_all_columns: list):
    data = MagicMock()
    data.columns = expected_all_columns.copy()

    def drop(labels: str, axis: int):
        data.columns.remove(labels)
        return data

    data.drop = drop
    return data
