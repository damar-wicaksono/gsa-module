# -*- coding: utf-8 -*-
"""
    gsa_module.cmdnln_interface
    ***************************

    Module with collection of driver routines as the command line interface
    to execute functionalities within gsa-module package
"""
import numpy as np


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
