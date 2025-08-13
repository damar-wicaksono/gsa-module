# -*- coding: utf-8 -*-
"""
    gsa_module.sobol.cmdln_args
    ***************************
    
    Module with routines to parse different command line operations of carrying
    out Sobol' (variance decomposition) global sensitivity analysis.
    It includes: generate samples and analyze samples
"""
import argparse
import os
from ..util import ext_to_delimiter
from .._version import __version__


def get_create_sample():
    """Get the command line arguments to generate DOE for Sobol' var. decomp.

    :return: a dictionary of parsed command line arguments

    +------------------+------------------------------------------------------+
    | Key              | Value                                                |
    +==================+======================================================+
    | num_samples      | (int, positive) The number of Monte Carlo samples    |
    |                  |  to estimate the sensitivity indices                 |
    +------------------+------------------------------------------------------+
    | num_dimensions   | (int, positive) The number of dimensions/parameters  |
    +------------------+------------------------------------------------------+
    | sampling_scheme  | ("srs", "lhs", "sobol") Sampling scheme to generate  |
    |                  | the design matrices                                  |
    +------------------+------------------------------------------------------+
    | interaction      | (bool) Flag to include sampling matrices to estimate |
    |                  | second order interaction                             |
    +------------------+------------------------------------------------------+
    | output_header    | (None or str) The output filename header. This header|
    |                  | will be appended by the id of the sampling matrices  |
    |                  | By default: "{}_{}_{}_{}_{}.{}" .format(method,      |
    |                  | num_blocks, num_dimensions, num_levels               |
    |                  | (if trajectory), sampling matrices, delimiter)       |
    |                  | the first four are the header                        |
    +------------------+------------------------------------------------------+
    | delimiter        | ("csv", "tsv", "txt") the delimiter of the design    |
    |                  | matrix file. By default: "csv" or parse directly if  |
    |                  | filename with extension is specified.                |
    +------------------+------------------------------------------------------+
    | seed_number      | (None or int, >= 0) Seed number for random number    |
    |                  | generation if using srs or lhs for the design matrix |
    +------------------+------------------------------------------------------+
    | direction_numbers| (None or np.ndarray) the contents of a direction     |
    |                  | number file for Sobol' sequence generator            |
    |                  | (default: built-in new-joe-kuo-6.21201)              |
    +------------------+------------------------------------------------------+
    """
    from ..samples import sobol

    parser = argparse.ArgumentParser(
        description="%(prog)s - gsa-module, Generate DOE for Sobol' "
                    " Variance Decomposition"
    )
    # The number of samples
    parser.add_argument(
        "-n", "--num_samples",
        type=int,
        required=True,
        help="The number of Monte Carlo samples"
    )
    # The number of dimensions
    parser.add_argument(
        "-d", "--num_dimensions",
        type=int,
        required=True,
        help="The number of dimensions (or parameters)"
    )
    # The method of generation
    parser.add_argument(
        "-ss", "--sampling_scheme",
        type=str,
        choices=["srs", "lhs", "sobol"],
        required=False,
        default="srs",
        help="The sampling scheme (default: %(default)s)"
    )
    # The output filename header
    parser.add_argument(
        "-o", "--output_header",
        type=str,
        required=False,
        help="The output filename header (created by default)"
    )
    # The delimiter
    parser.add_argument(
        "-sep", "--delimiter",
        type=str,
        choices=["csv", "tsv", "txt"],
        required=False,
        default="csv",
        help="The delimiter for the output files (default: %(default)s)"
    )
    # Flag to include matrices to estimate second-order interaction
    parser.add_argument(
        "-int", "--interaction",
        required=False,
        action="store_true",
        default=False,
        help="Include matrices to estimate 2nd-order interaction "
             "(default: %(default)s)"
    )
    # Only for SRS- and LHS- based design
    group_pseudorandom = parser.add_argument_group(
        "SRS and LHS Sampling Scheme Only (Pseudo-random sequence)"
    )
    # The random seed number
    group_pseudorandom.add_argument(
        "-s", "--seed_number",
        type=int,
        required=False,
        help="The random seed number"
    )
    # Only for Sobol'-based design
    group_quasirandom = parser.add_argument_group(
        "Sobol' Sampling Scheme Only (Quasi-random sequence)"
    )
    # The path to Sobol' generator direction numbers
    group_quasirandom.add_argument(
        "-dirnum", "--direction_numbers",
        type=str,
        required=False,
        help="The path to Sobol' sequence generator direction numbers file "
             "(default: built-in new-joe-kuo-6.21201)"
    )
    # Print the version
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s (gsa-module version {})" .format(__version__)
    )

    # Get the command line arguments
    args = parser.parse_args()

    # Check the validity of the number of samples
    if args.num_samples <= 0:
        raise ValueError("Number of samples must be > 0!")

    # Check the validity of the number of dimensions
    if args.num_dimensions <=0:
        raise ValueError("Number of dimensions must be > 0")

    # Assign the delimiter
    delimiter = ext_to_delimiter(args.delimiter)

    # Create a default filename header if not passed
    if args.output_header is None:
        output_header = "{}_{}_{}" .format(args.sampling_scheme,
                                           args.num_samples,
                                           args.num_dimensions)
    else:
        output_header = args.output_header

    # Check the validity of the seed number
    if args.seed_number is None:
        seed_number = None
    elif args.seed_number < 0:
        raise ValueError("Random seed number must be >= 0")
    else:
        seed_number = args.seed_number

    # Check the validity of the Sobol' sequence direction numbers
    if args.sampling_scheme == "sobol":
        if args.direction_numbers is not None:
            if os.path.exists(args.direction_numbers):
                direction_numbers = sobol.read_dirnumfile(
                    args.direction_numbers, args.num_dimensions)
            else:
                raise ValueError(
                    "Specified direction numbers file does not exist!")
        else:
            direction_numbers = None
    else:
        direction_numbers = None

    # Return the parsed command line arguments as a dictionary
    inputs = {
        "num_samples": args.num_samples,
        "num_dimensions": args.num_dimensions,
        "sampling_scheme": args.sampling_scheme,
        "interaction": args.interaction,
        "output_header": output_header,
        "delimiter": delimiter,
        "seed_number": seed_number,
        "direction_numbers": direction_numbers
    }

    return inputs
