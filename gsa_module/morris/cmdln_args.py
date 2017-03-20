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
import os
from ..__init__ import __version__


def get_create_sample():
    """Get the command line arguments to generate DOE for Morris screening

    :return:  a dictionary of command line arguments

    +------------------+------------------------------------------------------+
    | Key              | Value                                                |
    +==================+======================================================+
    | num_blocks       | (int, positive) The number of blocks/trajectories    |
    |                  |  replications to compute the statistics of the       |
    |                  |  elementary effects                                  |
    +------------------+------------------------------------------------------+
    | num_dimensions   | (int, positive) The number of dimensions/parameters  |
    +------------------+------------------------------------------------------+
    | sampling_scheme  | ("trajectory", "radial") Sampling scheme to generate |
    |                  | One-at-a-time design. Trajectory is the original     |
    |                  | randomized Morris' formulation, while radial uses    |
    |                  | Saltelli et al. formulation based on Sobol' sequence |
    +------------------+------------------------------------------------------+
    | num_levels       | (None or int, >0) The number of levels, partitioning |
    |                  | the parameter space in the trajectory sampling scheme|
    +------------------+------------------------------------------------------+
    | seed_number      | (None or int, >= 0) Seed number for random number    |
    |                  | generation in the trajectory sampling scheme         |
    +------------------+------------------------------------------------------+
    | direction_numbers| (None or str) the full path to the file containing   |
    |                  | direction number for Sobol' sequence generator       |
    |                  | (default: built-in new-joe-kuo-6.21201)
    +------------------+------------------------------------------------------+
    """
    from ..samples import sobol

    parser = argparse.ArgumentParser(
        description="%(prog)s - gsa-module, Generate DOE for Morris"
    )

    # The number of trajectories
    parser.add_argument(
        "-r", "--num_blocks",
        type=int,
        required=True,
        help="The number of blocks (or replications)"
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
    group_trajectory = parser.add_argument_group("Trajectory Sampling Scheme Only")

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
        "num_blocks": args.num_blocks,
        "num_dimensions": args.num_dimensions,
        "sampling_scheme": args.sampling_scheme,
        "output_file": output_file,
        "delimiter": delimiter,
        "num_levels": num_levels,
        "seed_number": seed_number,
        "direction_numbers": direction_numbers
    }

    return inputs


def get_analyze():
    """Get the command line arguments to create parameter ranking using Morris

    :return:  a dictionary of command line arguments

    +------------------+------------------------------------------------------+
    | Key              | Value                                                |
    +==================+======================================================+
    | normalized_inputs| (str) The fullname (path + filename) of the          |
    |                  | normalized inputs file (i.e., value in [0,1]         |
    |                  | generated using Morris Design of Experiment,         |
    |                  | either radial or trajectory                          |
    +------------------+------------------------------------------------------+
    | rescaled_inputs  | (str) The fullname (path + filename) of the rescaled |
    |                  | inputs file (i.e., according to the actual model     |
    |                  | specification)                                       |
    +------------------+------------------------------------------------------+
    | outputs          | (str) The fullname (path + filename) of the output   |
    |                  | from conducting the experimental runs based on the   |
    |                  | Morris design                                        |
    +------------------+------------------------------------------------------+
    | output_file      | (str) The filename for the output of the analysist   |
    |                  | by default it is "<morris_design_name>-morris.csv"   |
    +------------------+------------------------------------------------------+
    | model_checking   | (bool) Flag to verbosely check the model             |
    +------------------+------------------------------------------------------+
    """
    import os

    parser = argparse.ArgumentParser(
        description="%(prog)s - gsa-module, Analyze Morris Experimental Runs"
    )

    # Normalized inputs file
    parser.add_argument(
        "-in", "--normalized_inputs",
        type=str,
        required=True,
        help="The normalized inputs file"
    )

    # Rescaled inputs file
    parser.add_argument(
        "-ir", "--rescaled_inputs",
        type=str,
        required=False,
        help="The rescaled inputs file"
    )

    # Output file
    parser.add_argument(
        "-o", "--outputs",
        type=str,
        required=True,
        help="The model/function outputs file"
    )

    # Result of the analysis output file
    parser.add_argument(
        "-output", "--output_file",
        type=str,
        required=False,
        help="The results of the analysis output file"
    )

    # Verbose Error Checking flag
    parser.add_argument(
        "-mc", "--model_checking",
        action="store_true",
        required=False,
        help="Verbose model error checking"
    )

    # Print Version
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s (gsa-module version {})" .format(__version__)
    )

    # Get the command line arguments
    args = parser.parse_args()

    # Check the existence of inputs file
    if not os.path.exists(args.normalized_inputs):
        raise ValueError("{} inputs file does not exist!"
                         .format(args.normalized_inputs))

    # Check the existence of rescaled inputs file
    if args.rescaled_inputs is not None:
        if not os.path.exists(args.rescaled_inputs):
            raise ValueError("{} rescaled inputs file does not exist!"
                             .format(args.rescaled_inputs))

    # Check the existence of model outputs file
    if not os.path.exists(args.outputs):
        raise ValueError("{} output file does not exist!"
                         .format(args.outputs))

    # Create filename of analysis output file
    if args.output_file is None:
        output_file = "{}-{}.csv" \
            .format(args.normalized_inputs.split("/")[-1].split(".")[0],
                    args.outputs.split("/")[-1].split(".")[0])
    else:
        output_file = args.output_file

    # Return the parsed command line arguments as a dictionary
    inputs = {"normalized_inputs": args.normalized_inputs,
              "rescaled_inputs": args.rescaled_inputs,
              "outputs": args.outputs,
              "output_file": output_file,
              "model_checking": args.model_checking
              }

    return inputs
