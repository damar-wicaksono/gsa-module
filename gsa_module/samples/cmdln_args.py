"""Module to parse command line arguments in creating sample or validation data
"""
import argparse
import os

__author__ = "Damar Wicaksono"


def get_create_sample():
    """Get the passed command line arguments

    :return:  a dictionary of command line arguments

    +------------------+------------------------------------------------------+
    | Key              | Value                                                |
    +==================+======================================================+
    | num_samples      | (int, positive) The number of blocks/trajectories    |
    |                  |  replications to compute the statistics of the       |
    |                  |  elementary effects                                  |
    +------------------+------------------------------------------------------+
    | num_dimensions   | (int, positive) The number of dimensions/parameters  |
    +------------------+------------------------------------------------------+
    | method           | ("srs", "lhs", "sobol", "lhs-opt") Sampling scheme to|
    |                  | the design of experiments. By default "srs" is chosen|
    +------------------+------------------------------------------------------+
    | filename         | (None or str) The output filename.                   |
    |                  | By default: "{}_{}_{}.{}" .format(method,            |
    |                  |                                   num_samples,       |
    |                  |                                   num_dimensions,    |
    |                  |                                   delimiter)         |
    +------------------+------------------------------------------------------+
    | delimiter        | ("csv", "tsv", "txt") the delimiter of the design    |
    |                  | matrix file. By default: "csv"                       |
    +------------------+------------------------------------------------------+
    | seed_number      | (None or int, >0) The random seed number (irrelevant |
    |                  | for non-randomized Sobol' sequence)                  |
    +------------------+------------------------------------------------------+
    | direction_numbers| (str) the fullname (file+path) to the directions     |
    |                  | numbers file for Joe & Kuo Sobol' generator algorithm|
    |                  | By default: "./dirnumfiles/new-joe-kuo-6.21201"      |
    +------------------+------------------------------------------------------+
    | exclude_nominal  | (bool) Flag whether to include or exclude the {0.5}  |
    |                  | parameter values from the design. By default: False  |
    +------------------+------------------------------------------------------+
    | randomize_sobol  | (bool) Flag whether to random shift the Sobol'       |
    |                  | sequence. By default: False                          |
    +------------------+------------------------------------------------------+
    | num_iterations   | (100 or int, >0) the maximum number of outer         |
    |                  | iterations for optimizing the latin hypercube design |
    +------------------+------------------------------------------------------+
    """
    from .sobol import read_dirnumfile

    parser = argparse.ArgumentParser(
        description="gsa-module create_sample - Generate Design Matrix File"
    )

    # The number of samples
    parser.add_argument(
        "-n", "--num_samples",
        type=int,
        help="The number of samples",
        required=True
    )

    # The number of dimension
    parser.add_argument(
        "-d", "--num_dimensions",
        type=int,
        help="The number of dimensions",
        required=True
    )

    # The method to generate sample
    parser.add_argument(
        "-m", "--method",
        type=str,
        choices=["srs", "lhs", "sobol", "lhs-opt"],
        required=False,
        default="srs",
        help="The statistical method to generate sample (default: %(default)s)"
    )

    # The random seed number
    parser.add_argument(
        "-s", "--seed_number",
        type=int,
        required=False,
        help="The random seed number (irrelevant for non-randomized Sobol'"
             " sequence)"
    )

    # the design matrix filename
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

    # Only for Sobol'
    group_sobol = parser.add_argument_group("Sobol'", 
                                            "Options for Sobol' quasi-random")

    # The path to Sobol' direction number file
    group_sobol.add_argument(
        "-dirnumfile", "--direction_numbers",
        type=str,
        required=False,
        help="The path to Sobol' sequence generator direction numbers file"
             " (default: built-in new-joe-kuo-6.21201)"
    )

    # Flag to include the nominal point in the design
    group_sobol.add_argument(
        "-excl_nom", "--exclude_nominal",
        action="store_true",
        required=False,
        help="Exclude the nominal point in the design"
    )

    # Flag to randomize the sequence by random-shifting
    group_sobol.add_argument(
        "-rand", "--randomize_sobol",
        action="store_true",
        required=False,
        help="Random shift the Sobol' sequence"
    )

    # Only for optimized lhs
    group_lhs_opt = parser.add_argument_group("Optimized LHS",
                                              "Options for optimized lhs")

    # The number of iteration for optimization algorithm
    group_lhs_opt.add_argument(
        "-nopt", "--num_iterations",
        type=int,
        required=False,
        default=100,
        help="The maximum number of iterations for optimization of LHS"
             " (default: 100 iterations)"
    )

    # Get the command line arguments
    args = parser.parse_args()

    # Check the validity of number of samples
    if args.num_samples <= 0:
        raise ValueError("Zero or negative number of samples")

    # Check the validity of the number of dimensions
    if args.num_dimensions <= 0:
        raise ValueError("Zero or negative number of dimensions")

    # Check the validity of inputs if Sobol' sequence is used
    if args.method == "sobol":
        if args.direction_numbers is not None:
            if os.path.exists(args.direction_numbers):
                direction_numbers = read_dirnumfile(args.direction_numbers,
                                                    args.num_dimensions)
            else:
                raise ValueError(
                    "Sobol' generator direction number file does not exist!")
        else:
            direction_numbers = None
    else:
        direction_numbers = None

    # Check the delimiter
    if args.delimiter == "csv":
        delimiter = ","
    elif args.delimiter == "tsv":
        delimiter = "\t"
    else:
        delimiter = " "

    # Check the random seed number
    if args.seed_number is None:
        seed_number = None
    elif args.seed_number < 0:
        raise ValueError
    else:
        seed_number = args.seed_number

    # Create default filename if not passed
    if args.output_file is None:
        output_file = "{}_{}_{}.{}" .format(args.method, args.num_samples,
                                            args.num_dimensions,
                                            args.delimiter)
    else:
        output_file = args.output_file

    # Set default value for the number of iterations if opt-lhs is selected
    if args.num_iterations is not None:
        if args.num_iterations < 0:
            raise ValueError("Number of iterations must be greater than zero!")

    # Return the parsed command line arguments as a dictionary
    inputs = {"num_samples": args.num_samples,
              "num_dimensions": args.num_dimensions,
              "method": args.method,
              "filename": output_file,
              "delimiter": delimiter,
              "seed_number": seed_number,
              "direction_numbers": direction_numbers,
              "exclude_nominal": args.exclude_nominal,
              "randomize_sobol": args.randomize_sobol,
              "num_iterations": args.num_iterations
              }

    return inputs


def get_create_validset():
    """Get the passed command line arguments for creating sample"""
    import argparse

    parser = argparse.ArgumentParser(
        description="gsa-module create_validset - Generate Validation Data Set"
    )

    # The design matrix fullname
    parser.add_argument(
        "-dm", "--dm_fullname",
        type=str,
        required=True,
        help="The design matrix fullname (file + path)",
    )

    # The number of test points
    parser.add_argument(
        "-n", "--num_tests",
        type=int,
        required=True,
        help="The number of test points to be generated"
    )

    # The validation data set filename
    parser.add_argument(
        "-o", "--output_file",
        type=str,
        required=False,
        help="The output filename"
    )

    # The number of candidates
    parser.add_argument(
        "-nc", "--num_candidates",
        type=int,
        required=False,
        default=10000,
        help="The number of candidates from the Hammersley sequence"
    )

    # Get the command line arguments
    args = parser.parse_args()

    # Check the existence of the design matrix file

    # Check the validity of number of test points
    if args.num_tests <= 0:
        raise ValueError

    # Check the validity of number of candidates
    if args.num_candidates <= 0:
        raise ValueError

    # Determine the delimiter inside the file
    delimiter = args.dm_fullname.split("/")[-1].split(".")[-1]
    if delimiter == "csv":
        str_delimiter = ","
    elif delimiter == "tsv":
        str_delimiter = "\t"
    else:
        str_delimiter = " "

    # Create default filename if not passed
    if args.output_file is None:
        dm_name = args.dm_fullname.split("/")[-1]
        output_file = "{}_test_{}.{}" .format(dm_name.split(".")[0],
                                              args.num_tests, delimiter)
    else:
        output_file = args.output_file

    # Return the parsed command line arguments as a dictionary
    inputs = {"dm_fullname": args.dm_fullname,
              "num_tests": args.num_tests,
              "num_candidates": args.num_candidates,
              "filename": output_file,
              "str_delimiter": str_delimiter
              }

    return inputs
