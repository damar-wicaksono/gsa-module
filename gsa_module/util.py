# -*- coding: utf-8 -*-
"""
    gsa_module.util
    ***************************

    Module with collection of utilities
"""
import numpy as np


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


