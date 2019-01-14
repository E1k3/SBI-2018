#! /usr/bin/env python3

from argparse import ArgumentParser
from typing import List


def create_offsets(sequence: str) -> List[str]:
    offsets: List[str] = []
    for i in range(len(sequence)):
        offsets.append(sequence[i:] + sequence[:i])
    return offsets


def create_bw_transform(sequence: str) -> List[str]:
    bw_transform: List[str] = create_offsets(sequence)
    bw_transform.sort()
    return bw_transform


def create_suffixes(sequence: str) -> List[str]:
    suffixes: List[str] = []
    for i in range(len(sequence)):
        suffixes.append(sequence[i:])
    return suffixes


def create_suffix_array(sequence: str) -> List[str]:
    suffix_array: List[str] = create_suffixes(sequence)
    suffix_array.sort()
    return suffix_array


def create_latex_table(strings: List[str],
                      column_seperator: bool = True,
                      row_seperator: bool = True) -> str:
    """Creates a latex table string

    Displays all characters of each string in its own cell
    """
    column_count: int = len(max(strings, key=lambda s: len(s)))
    table_spec_seperator = " | " if column_seperator else ' '
    table_spec = (table_spec_seperator
                  + table_spec_seperator.join('c' for i in range(column_count))
                  + table_spec_seperator)

    latex_table: str = "\\begin{tabular}{" + table_spec + "}\n"
    for string in strings:
        if row_seperator:
            latex_table += "    \\hline\n"
        string += ''.join(' ' for i in range(column_count - len(string)))
        latex_table += "    " + " & ".join(string) + " \\\\\n"

    if row_seperator:
        latex_table += "    \\hline\n"
    latex_table += "\\end{tabular}"

    return latex_table


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("sequence")
    parser.add_argument("-o", "--offsets", action="store_true")
    parser.add_argument("-b", "--bw_transform", action="store_true")
    parser.add_argument("-s", "--suffixes", action="store_true")
    parser.add_argument("-a", "--suffix_array", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("-l", "--latex_table", action="store_true")
    parser.add_argument("-c", "--column_seperator", action="store_true")
    parser.add_argument("-r", "--row_seperator", action="store_true")
    args = parser.parse_args()

    functions = [(args.offsets or args.all,      create_offsets,      "Offsets"),
                 (args.bw_transform or args.all, create_bw_transform, "BWT"),
                 (args.suffixes or args.all,     create_suffixes,     "Suffixes"),
                 (args.suffix_array or args.all, create_suffix_array, "Suffix-Array")]

    for key, func, label in functions:
        if key:
            data: str = func(args.sequence)
            print(f"--- {label} ---")
            if args.latex_table:
                print(create_latex_table(data, args.column_seperator, args.row_seperator))
            else:
                for row in data:
                    print(row)
            print()
