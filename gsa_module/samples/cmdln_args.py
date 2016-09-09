"""Module to parse command line arguments in creating sample or validation data
"""
import argparse

__author__ = "Damar Wicaksono"


def get():
    """Get the passed command line arguments"""

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
        help="The random seed number (irrelevant for Sobol' sequence)"
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
    # The path to sobol generator
    group_sobol.add_argument(
        "-sobol", "--sobol_generator",
        type=str,
        required=False,
        help="The path to Sobol' sequence generator executable"
    )

    # The path to sobol generator
    group_sobol.add_argument(
        "-dirnum", "--direction_numbers",
        type=str,
        required=False,
        help="The path to Sobol' sequence generator direction numbers file"
    )

    # Flag to include the nominal point in the design
    group_sobol.add_argument(
        "-nom", "--include_nominal",
        action="store_true",
        required=False,
        help="Include the nominal point in the design"
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
    )

    # Get the command line arguments
    args = parser.parse_args()

    # Check the validity of number of samples
    if args.num_samples <= 0:
        raise ValueError

    # Check the validity of the number of dimensions
    if args.num_dimensions <= 0:
        raise ValueError

    # Check the validity of inputs if Sobol' sequence is used
    if args.method == "sobol":
        if args.sobol_generator is None:
            raise ValueError("Sobol' method requires generator executable")
        elif args.direction_numbers is None:
            raise ValueError("Sobol' method requires direction numbers file")

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
                                            args.num_dimensions, args.delimiter)
    else:
        output_file = args.output_file

    # Return the parsed command line arguments as a dictionary
    inputs = {"num_samples": args.num_samples,
              "num_dimensions": args.num_dimensions,
              "method": args.method,
              "filename": output_file,
              "delimiter": delimiter,
              "seed_number": seed_number,
              "sobol_generator": args.sobol_generator,
              "direction_numbers": args.direction_numbers,
              "include_nominal": args.include_nominal,
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