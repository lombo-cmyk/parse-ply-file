import sys
import pandas as pd
from datetime import datetime
from typing import Optional

from ._columns import Colnames, ColumnSanitizer


class PlyReader:

    def __init__(self, filename: str):
        self.filename = filename
        self.colnames = [el.value for el in Colnames]

        self.file: Optional[pd.DataFrame] = None
        self.header_size: Optional[int] = None
        self.entries_count: Optional[int] = None

    def run(self):
        self._read_file_content()
        self._find_header_size()
        self._get_number_of_entries()
        self._cut_entries()
        self._filter_non_zero_entries()
        self._save_output()

    def _read_file_content(self):
        column_sanitizer = ColumnSanitizer(self.filename, self.colnames)
        column_sanitizer.determine_column_count()
        self.colnames = column_sanitizer.extend_columns()
        try:
            self.file = pd.read_csv(self.filename,
                                    sep=" ",
                                    names=self.colnames,
                                    dtype=str)
        except FileNotFoundError:
            sys.exit(f"Provided file: >> {self.filename} << does not exist! "
                     f"Closing...")

        self.file, self.colnames = ColumnSanitizer.drop_extra_columns(
            self.file)

    def _find_header_size(self):
        column = self.file[Colnames.X.value]

        for i, el in enumerate(column):
            if el == "end_header":
                self.header_size = i + 1
                break

        if self.header_size is None:
            raise Exception("Header size not found! Does it finish with "
                            "\"end_header\"? ")

    def _get_number_of_entries(self):
        lines_count_index = None
        for row, el in enumerate(self.file[Colnames.Y.value]):
            if el == "vertex":
                lines_count_index = row
                break

        if lines_count_index is None:
            raise Exception(
                "Number of lines not found in file! (Is it defined "
                "next to vertex cell?)")

        self.entries_count = int(self.file[Colnames.Z.value].loc[
                                     lines_count_index])

    def _cut_entries(self):
        self.file = self.file[self.header_size:(
                self.header_size+self.entries_count)]

    def _filter_non_zero_entries(self):
        self.file = self.file.astype({Colnames.LABEL.value: int},
                                     errors='raise')
        self.file = self.file[self.file[Colnames.LABEL.value] == 0]
        self.file = self.file.reset_index(drop=True)

    def _save_output(self):
        exec_time = datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
        new_file = f"{exec_time}_output.csv"
        print(f"Saving to: {new_file} ...")
        self.file.to_csv(new_file, index=False)
