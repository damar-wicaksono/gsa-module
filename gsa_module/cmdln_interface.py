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
