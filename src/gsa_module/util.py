# -*- coding: utf-8 -*-
"""
    gsa_module.util
    ***************************

    Module with collection of utilities
"""

def sniff_delimiter(input_file: str):
    """Detect the delimiter in a file"""
    import csv

    sniffer = csv.Sniffer()
    with open(input_file, "rt") as f:
        first_line = f.readline().strip()
    dialect = sniffer.sniff(first_line)

    if dialect.delimiter not in [",", " ", "\t"]:
        raise ValueError("Delimiter not supported/detected")
    else:
        return dialect.delimiter


def ext_to_delimiter(extension: str) -> str:
    """Convert file extension to delimiter

    :param extension: file extension ("txt", "csv", "tsv")
    :return: the delimiter (",", " ", "\t")
    """
    if extension == "csv":
        delimiter = ","
    elif extension == "tsv":
        delimiter = "\t"
    elif extension == "txt":
        delimiter = " "
    else:
        raise ValueError("File extension not recognized!"
                         " (Use txt, tsv, or csv)")

    return delimiter
