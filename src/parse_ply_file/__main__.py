import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from parse_ply_file._ply_reader import PlyReader


def main():
    dsc = f"Executable python module created to parse cell ASCII .ply " \
          f"files. {os.linesep}Takes file as an argument and saved th" \
          f"e output to execution location." \
          f"{os.linesep}Example call:" \
          f"{os.linesep} \t python -m parse_ply_file my_file.ply"

    parser = ArgumentParser(
        prog='python -m parse_ply_file',
        description=dsc,
        formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("file", help="path to file to parse",
                        type=str)
    args = parser.parse_args()

    reader = PlyReader(args.file)
    reader.run()


if __name__ == "__main__":
    main()
