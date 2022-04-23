import sys
from enum import Enum
from typing import Optional, List, Tuple
from pandas import DataFrame, Index


class Colnames(Enum):
    X = "x"
    Y = "y"
    Z = "z"
    LABEL = "label"
    SIGNAL = "signal"
    TMP = "tmp_"


class ColumnSanitizer:

    def __init__(self, filename: str, columns: list):
        self._filename = filename
        self._columns = columns.copy()
        self._max_col_count: Optional[int] = None

    def determine_column_count(self):
        try:
            with open(self._filename) as f:
                possible_col_sizes = [f.readline().count(" ") + 1 for _ in
                                      range(100)]
        except FileNotFoundError:
            sys.exit(f"Provided file: >> {self._filename} << does not exist! "
                     f"Closing...")
        self._max_col_count = max(possible_col_sizes)

    def extend_columns(self) -> List[str]:
        if self._max_col_count > (tmp := len(self._columns)):
            for i in range(self._max_col_count - tmp):
                self._columns.append(f"{Colnames.TMP.value}{i}")
        return self._columns

    @staticmethod
    def drop_extra_columns(data: DataFrame) -> Tuple[DataFrame, Index]:
        columns = data.columns.copy()
        for col in columns:
            if Colnames.TMP.value in col:
                data: DataFrame = data.drop(labels=col, axis=1)
        return data, data.columns
