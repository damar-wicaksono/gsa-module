# -*- coding: utf-8 -*-
"""
    gsa_module.morris.cmdnln_args
    *****************************

    Module with routines to parse different command line operations of carrying
    out Morris screening analysis, namely: generate samples, analyze samples
    (make ranking), and make some plots (exploratory purpose, not for
    publication)
"""
import argparse
from gsa_module import __version__


def get_create_sample():
    """Get the command line arguments to generate DOE for Morris screening

    :return:  a dictionary of command line arguments

    +-----------------+------------------------------------------------------+
    | Key             | Value                                                |
    +=================+======================================================+
    | num_blocks      | (int, positive) The number of blocks/trajectories    |
    |                 |  replications to compute the statistics of the       |
    |                 |  elementary effects                                  |
    +-----------------+------------------------------------------------------+
    | num_dimensions  | (int, positive) The number of dimensions/parameters  |
    +-----------------+------------------------------------------------------+
    | sampling_scheme | ("trajectory", "radial") Sampling scheme to generate |
    |                 | One-at-a-time design. Trajectory is the original     |
    |                 | randomized Morris' formulation, while radial uses    |
    |                 | Saltelli et al. formulation based on Sobol' sequence |
    +-----------------+------------------------------------------------------+
    | num_levels      | (None or int, >0) The number of levels, partitioning |
    |                 | the parameter space in the trajectory sampling scheme|
    +-----------------+------------------------------------------------------+
    | seed_number     | (None or int, >= 0) Seed number for random number    |
    |                 | generation in the trajectory sampling scheme         |
    +-----------------+------------------------------------------------------+
    | sobol_generator | (None or str) The fullpath of executable to external |
    |                 | Sobol' sequence generator                            |
    +-----------------+------------------------------------------------------+
    | direction_number| (None or str) the full path to the file containing   |
    |                 | direction number for Sobol' sequence generator       |
    +-----------------+------------------------------------------------------+
    """

    parser = argparse.ArgumentParser(
        description="%(prog)s - gsa-module, Generate DOE for Morris"
    )

    # The number of trajectories
    parser.add_argument(
        "-r", "--num_blocks",
        type=int,
        required=True,
        help="The number of blocks (or trajectories)"
    )

    # The number of dimensions
    parser.add_argument(
        "-d", "--num_dimensions",
        type=int,
        required=True,
        help="The number of dimensions (or parameters)"
    )

    # the output filename
    parser.add_argument(
        "-o", "--output_file",
        type=str,
        required=False,
        help="The output filename"
    )

    # The delimiter
    parser.add_argument(
        "-sep", "--delimiter",
        type=str,
        choices=["csv", "tsv", "txt"],
        required=False,
        default="csv",
        help="the delimiter for the file (default: %(default)s)"
    )

    # The method of generation
    parser.add_argument(
        "-ss", "--sampling_scheme",
        type=str,
        choices=["trajectory", "radial"],
        required=False,
        default="trajectory",
        help="The sampling scheme (default: %(default)s)"
    )

    # Only for trajectory sampling scheme
    group_trajectory = parser.add_argument_group("Radial Sampling Scheme Only")

    # The number of levels, only for trajectory scheme
    group_trajectory.add_argument(
        "-p", "--num_levels",
        type=int,
        required=False,
        default=4,
        help="The number of levels in the design, must be even number"
             " (default: %(default)s)"
    )

    # The random seed number, only for trajectory scheme
    group_trajectory.add_argument(
        "-s", "--seed_number",
        type=int,
        required=False,
        help="The random seed number"
    )

    # Only for radial sampling scheme
    group_radial = parser.add_argument_group("Radial Sampling Scheme Only")

    # The path to sobol generator executable, only for radial scheme
    group_radial.add_argument(
        "-sobol", "--sobol_generator",
        type=str,
        required=False,
        help="The path to Sobol' sequence generator executable"
    )

    # The path to sobol generator directional number, only for radial scheme
    group_radial.add_argument(
        "-dirnum", "--direction_numbers",
        type=str,
        required=False,
        help="The path to Sobol' sequence generator direction numbers file"
    )

    # Print the version
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s (gsa-module version {})" .format(__version__)
    )

    # Get the command line arguments
    args = parser.parse_args()

    # Check the validity of number of samples
    if args.num_blocks <= 0:
        raise ValueError("Number of blocks must be > 0")

    # Check the validity of the number of dimensions
    if args.num_dimensions <= 0:
        raise ValueError("Number of dimensions must be > 0")

    # Assign the delimiter
    if args.delimiter == "csv":
        delimiter = ","
    elif args.delimiter == "tsv":
        delimiter = "\t"
    else:
        delimiter = " "

    # Create default filename if not passed
    if args.output_file is None and args.sampling_scheme == "trajectory":
        output_file = "trajectory_{}_{}_{}.{}" .format(args.num_blocks,
                                                       args.num_dimensions,
                                                       args.num_levels,
                                                       args.delimiter)
    elif args.output_file is None and args.sampling_scheme == "radial":
        output_file = "radial_{}_{}.{}" .format(args.num_blocks,
                                                args.num_dimensions,
                                                args.delimiter)
    else:
        output_file = args.output_file

    # Check the validity of number of levels
    if args.sampling_scheme == "trajectory":
        if args.num_levels%2 == 1:
            raise ValueError("Number of levels must be even")
        else:
            num_levels = args.num_levels
    else:
        num_levels = None

    # Check the validity of seed number
    if args.seed_number is None:
        seed_number = None
    elif args.seed_number < 0:
        raise ValueError("Random seed number must be >= 0")
    else:
        seed_number = args.seed_number

    # Check the validity of sobol' sequence generator and direction numbers
    if args.sampling_scheme == "radial":
        if args.sobol_generator is None:
            raise ValueError("Radial scheme requires Sobol' requires generator")
        elif args.direction_numbers is None:
            raise ValueError("Radial scheme requires Sobol' direction numbers")

    # Return the parsed command line arguments as a dictionary
    inputs = {
        "num_blocks": args.num_blocks,
        "num_dimensions": args.num_dimensions,
        "sampling_scheme": args.sampling_scheme,
        "output_file": output_file,
        "delimiter": delimiter,
        "num_levels": num_levels,
        "seed_number": seed_number,
        "sobol_generator": args.sobol_generator,
        "direction_numbers": args.direction_numbers
    }

    return inputs
