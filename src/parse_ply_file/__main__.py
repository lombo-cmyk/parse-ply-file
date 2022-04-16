from argparse import ArgumentParser
from parse_ply_file._ply_reader import PlyReader


def main():
    parser = ArgumentParser()
    parser.add_argument("file", help="path to file to parse",
                        type=str)
    parser.add_argument("--excel", help="use this argument if parsed file is "
                                        "Excel file (.xlsx)",
                        action='store_true')
    args = parser.parse_args()

    reader = PlyReader(args.file, args.excel)
    reader.run()


if __name__ == "__main__":
    main()
