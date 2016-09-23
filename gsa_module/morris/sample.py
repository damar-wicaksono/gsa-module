# -*- coding: utf-8 -*-
"""Module implementing generation methods of DOE for Morris screening

Two flavors for generating design of experiment for Morris screening
analysis are implemented:

 1. The trajectory design: the one proposed originally by Morris, also known
    as the winding stair design proposed by Jansen (although comes in a bit
    modified form)
 2. The radial design: the one proposed by Saltelli et al. that uses Sobol' low
    discrepancy sequence to build an OAT design. It is promoted because removing
    the number of levels from the specification, thus reducing additional
    user-specified parameter

"""
import numpy as np


def trajectory(r: int, k: int, p: int, numseed: int) -> np.ndarray:
    r"""Create Morris One-at-a-time design matrix, or the trajectory design

    :param r: the number of trajectories or replications
    :param k: the number of parameters
    :param p: the number of levels, have to be an even number
    :param numseed: the seed number for random number generation
    :return: the trajectory design matrix
    """
    pass
