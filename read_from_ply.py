import pandas as pd
from argparse import ArgumentParser
import sys

parser = ArgumentParser()
parser.add_argument("file", help="path to file to parse",
                    type=str)
parser.add_argument("--excel", help="use this argument if parsed file is "
                                    "Excel file (.xlsx)", action='store_true')
args = parser.parse_args()


def read_file() -> pd.DataFrame:
    try:
        if args.excel:
            file = pd.read_excel(io=args.file,
                                 sheet_name="cell1",
                                 names=["x", "y", "z", "label", "signal", "tmp"])
        else:
            file = pd.read_csv(args.file,
                               sep=" ",
                               names=["x", "y", "z", "label", "signal", "tmp"])
    except FileNotFoundError:
        print(f"Provided file: >> {args.file} << does not exist! Closing...")
        sys.exit()
    file = file.drop(labels="tmp", axis=1)
    return file


def cut_entries(header_size: int,
                number_of_entries: int,
                exc_file: pd.DataFrame) -> pd.DataFrame:
    file = exc_file[header_size:(header_size+number_of_entries)]
    return file


def find_header_size(file: pd.DataFrame) -> int:
    column = file["x"]
    header_size = None

    for i, el in enumerate(column):
        if el == "end_header":
            header_size = i + 1
            break

    if header_size is None:
        raise Exception

    return header_size


def get_number_of_entries(header: pd.DataFrame) -> int:
    lines_count_index = None
    for row, el in enumerate(header["y"]):
        if el == "vertex":
            lines_count_index = row
            break
    if lines_count_index is None:
        raise Exception("Number of lines not found in file! (Is it defined "
                        "next to vertex cell?)")
    return int(header["z"].loc[lines_count_index])


def main():
    entries = read_file()
    header_size = find_header_size(entries)
    number_of_lines = get_number_of_entries(entries)
    entries = cut_entries(header_size, number_of_lines, entries)

    entries = entries.astype({"label": int}, errors='raise')

    entries = entries[entries["label"] == 0]
    entries = entries.reset_index(drop=True)

    is_excel = "_from_excel" if args.excel else ""
    new_file = f"output{is_excel}.csv"
    print(f"Saving to: {new_file} ...")
    entries.to_csv(new_file, index=False)


if __name__ == "__main__":
    main()
