# -*- coding: utf-8 -*-
"""
    gsa_module.cmdnln_interface
    ***************************

    Module with collection of driver routines as the command line interface
    to execute functionalities within gsa-module package
"""
import numpy as np


def create_sample():
    """gsa-module, create a design of experiment command line interface"""
    from gsa_module import samples

    # Get the command line arguments
    inputs = samples.cmdln_args.get_create_sample()

    # Generate the design matrix file
    if inputs["method"] == "srs":
        # Create simple random sampling design
        dm = samples.srs.create(inputs["num_samples"], inputs["num_dimensions"],
                                seed=inputs["seed_number"])
    elif inputs["method"] == "lhs":
        # Create Latin Hypercube Sampling design
        dm = samples.lhs.create(inputs["num_samples"], inputs["num_dimensions"],
                                seed=inputs["seed_number"])
    elif inputs["method"] == "sobol":
        # Create Sobol' quasirandom sequence design
        dm = samples.sobol.create(inputs["num_samples"],
                                  inputs["num_dimensions"],
                                  generator=inputs["sobol_generator"],
                                  dirnumfile=inputs["direction_numbers"],
                                  incl_nom=inputs["include_nominal"],
                                  randomize=inputs["randomize_sobol"],
                                  seed=inputs["seed_number"])
    elif inputs["method"] == "lhs-opt":
        # Create an optimized latin hypercube design
        dm = samples.lhs_opt.create_ese(inputs["num_samples"],
                                        inputs["num_dimensions"],
                                        seed=inputs["seed_number"],
                                        max_outer=inputs["num_iterations"])

    # Save the design into file
    np.savetxt(inputs["filename"], dm,
               fmt="%1.6e", delimiter=inputs["delimiter"])


def morris_generate():
    """gsa-module, create Morris experimental design command line interface"""
    from gsa_module import morris

    # Read command line arguments
    inputs = morris.cmdln_args.get_create_sample()

    # Generate DOE
    if inputs["sampling_scheme"] == "trajectory":
        # Create trajectory scheme for DOE
        dm = morris.sample.trajectory(inputs["num_blocks"],
                                      inputs["num_dimensions"],
                                      inputs["num_levels"],
                                      seed=inputs["seed_number"])
    elif inputs["sampling_scheme"] == "radial":
        # Create radial sampling scheme for the DOE
        dm = morris.sample.radial(inputs["num_blocks"],
                                  inputs["num_dimensions"],
                                  inputs["sobol_generator"],
                                  inputs["direction_numbers"])

    # Save the sample
    np.savetxt(inputs["output_file"], dm,
               fmt="%1.6e", delimiter=inputs["delimiter"])


def morris_analyze():
    """gsa-module, analyze Morris experimental runs command line interface"""
    from gsa_module import morris
    from .util import sniff_delimiter

    # Read command line arguments
    inputs = morris.cmdln_args.get_analyze()

    # Read the inputs/outputs file
    dm_norm = np.loadtxt(inputs["normalized_inputs"],
                         delimiter=sniff_delimiter(inputs["normalized_inputs"]))

    if inputs["rescaled_inputs"] is not None:
        dm_resc = np.loadtxt(
            inputs["rescaled_inputs"],
            delimiter=sniff_delimiter(inputs["rescaled_inputs"]))
        if dm_norm.shape[0] != dm_resc.shape[0]:
            raise ValueError(
                "Lengths of normalized input ({}) and normalized ({}) are not the same!" .format(
                    dm_norm.shape[0], dm_resc.shape[0]))
    else:
        dm_resc = None

    outp = np.loadtxt(inputs["outputs"])

    # Check the length of inputs and outputs
    if dm_norm.shape[0] != outp.shape[0]:
        raise ValueError(
            "Lengths of input ({}) and output ({}) are not the same!" .format(
                dm_norm.shape[0], outp.shape[0]))

    # Check the model specifications
    if inputs["model_checking"]:
        num_runs = dm_norm.shape[0]
        num_dims = dm_norm.shape[1]
        num_reps = int(num_runs / (num_dims + 1))
        morris_type, num_lev, delta = morris.misc.sniff_morris(dm_norm)

        print("Number of Input Dimensions    = {}" .format(num_dims))
        print("Number of Blocks/Replications = {}" .format(num_reps))
        print("Total Number of Runs          = {}" .format(num_runs))
        print("Type of Design                = {}" .format(morris_type))
        print("Number of levels (trajectory) = {} (Delta = {})"
              .format(num_lev, delta))
        print("Rescaled Inputs               = {}"
              .format(inputs["rescaled_inputs"]))

    # Analyze the input/output
    if morris_type == "trajectory":
        param_rank = morris.analyze.trajectory(dm_norm, dm_resc, outp)
    elif morris_type == "radial":
        param_rank = morris.analyze.radial(dm_norm, dm_resc, outp)

    # Save the result of the analysis
    np.savetxt(inputs["output_file"], param_rank,
               fmt="%1.6e", delimiter=",",
               header="mu, mu_star, std_dev, std_mu, std_mu_star, std_std_dev")
