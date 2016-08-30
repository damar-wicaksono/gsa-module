"""Module to parse command line arguments in creating sample
"""

__author__ = "Damar Wicaksono"


def get():
    """Get the passed command line arguments"""
    import argparse

    parser = argparse.ArgumentParser(
        description="gsa-module create_sample - Generate Design Matrix File"
    )

    # the number of samples
    parser.add_argument(
        "-n", "--num_samples",
        type=int,
        help="The number of samples",
        required=True
    )

    # the number of dimension
    parser.add_argument(
        "-d", "--num_dimensions",
        type=int,
        help="The number of dimensions",
        required=True
    )

    # the method to generate sample
    parser.add_argument(
        "-m", "--method",
        type=str,
        choices=["srs", "lhs"],
        required=False,
        default="srs",
        help="The statistical method to generate sample (default: %(default)s)"
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
        choices=["csv", "tsv", "ssv"],
        required=False,
        default="csv",
        help="the delimiter for the file (default: %(default)s)"
    )

    # The random seed number
    parser.add_argument(
        "-s", "--seed_number",
        type=int,
        required=False,
        help="The random seed number"
    )

    # Get the command line arguments
    args = parser.parse_args()

    # Check the validity of number of samples
    if args.num_samples <= 0:
        raise ValueError

    # Check the validity of the number of dimensions
    if args.num_dimensions <= 0:
        raise ValueError

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
              "seed_number": seed_number
              }

    return inputs