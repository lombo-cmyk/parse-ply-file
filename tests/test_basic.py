import pytest
from parse_ply_file import PlyReader


def test_happy_path():
    reader = PlyReader("test_data/test_happy_path.ply", False)
    reader.run()

    assert reader.filename == "test_data/test_happy_path.ply"
    assert reader.entries_count == 7
    assert reader.header_size == 14
    assert reader.file.shape[0] == 3


def test_zero_at_end():
    reader = PlyReader("test_data/test_zero_at_end.ply", False)
    reader.run()

    assert reader.file.shape[0] == 1


def test_zero_at_start():
    reader = PlyReader("test_data/test_zero_at_start.ply", False)
    reader.run()

    assert reader.file.shape[0] == 1


def test_no_extra_lines_at_end():
    reader = PlyReader("test_data/test_no_extra_lines.ply", False)
    reader.run()

    assert reader.file.shape[0] == 1


def test_empty_output():
    reader = PlyReader("test_data/test_empty_output.ply", False)
    reader.run()

    assert reader.file.shape[0] == 0


def test_file_missing():
    filename = "test_data/non_existing_file.ply"
    reader = PlyReader(filename, False)
    with pytest.raises(SystemExit) as e:
        reader.run()
    assert e.value.args[0] == f"Provided file: >> {filename} << " \
                              f"does not exist! Closing..."


def test_no_header_size():
    filename = "test_data/test_no_end_header.ply"
    reader = PlyReader(filename, False)
    with pytest.raises(Exception) as e:
        reader.run()
    assert e.value.args[0] == "Header size not found! Does it finish with "\
                              "\"end_header\"? "


def test_no_entries_count():
    filename = "test_data/test_no_size.ply"
    reader = PlyReader(filename, False)
    with pytest.raises(Exception) as e:
        reader.run()
    assert e.value.args[0] == "Number of lines not found in file! " \
                              "(Is it defined next to vertex cell?)"
