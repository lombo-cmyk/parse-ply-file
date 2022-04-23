import pytest
from unittest.mock import MagicMock

from parse_ply_file._columns import ColumnSanitizer


@pytest.mark.parametrize("expected_all_columns", [["1", "2", "3", "tmp_0",
                                                   "tmp_1", "tmp_2"]])
def test_happy_path(mock_dataframe: MagicMock, expected_all_columns):
    sanitizer = ColumnSanitizer("test_data/common/test_happy_path.ply",
                                ["1", "2", "3"])
    sanitizer.determine_column_count()
    all_columns = sanitizer.extend_columns()
    data, columns = ColumnSanitizer.drop_extra_columns(mock_dataframe)

    assert all_columns == expected_all_columns
    assert columns == ["1", "2", "3"]
    assert data


@pytest.mark.parametrize("expected_all_columns", [["1", "2", "3", "4", "5",
                                                   "6"]])
def test_dont_extend_columns(mock_dataframe, expected_all_columns):
    sanitizer = ColumnSanitizer("test_data/common/test_happy_path.ply",
                                expected_all_columns)
    sanitizer.determine_column_count()
    all_columns = sanitizer.extend_columns()
    data, columns = ColumnSanitizer.drop_extra_columns(mock_dataframe)

    assert all_columns == expected_all_columns
    assert columns == expected_all_columns
    assert data


def test_unexisting_file():
    filename = "test_data/non_existing_file.ply"
    sanitizer = ColumnSanitizer(filename, MagicMock())
    with pytest.raises(SystemExit) as e:
        sanitizer.determine_column_count()
    assert e.value.args[0] == f"Provided file: >> {filename} << " \
                              f"does not exist! Closing..."




