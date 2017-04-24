# -*- coding: utf-8 -*-
"""
    gsa_module.morris.misc
    **********************

    Module with collection of utilities related to Morris screening method
    implementation
"""
import numpy as np


def sniff_morris(dm: np.ndarray):
    """Detect the type of Morris design

    It is assumed that if the number of unique absolute grid jump is greater
    than 2 (i.e, 0 and delta) then the design is considered "radial".
    """
    num_dim = dm.shape[1]   # Number of dimensions

    delta = np.array([])
    for i in range(num_dim):
        delta = np.append(delta, np.unique(np.abs(dm[:num_dim,i] - dm[1:(num_dim+1),i])))

    delta = np.unique(delta.round(decimals=4))

    if len(delta) > 2:
        return "radial", None, None
    else:
        num_lev = int(round(2 * delta[1] / (2 * delta[1] - 1)))
        return "trajectory", num_lev, delta[1]


def calc_pf(mu_star_1: np.ndarray, mu_star_2: np.ndarray) -> float:
    """Compute the position factor for 2 mu* calc. with different block size
    
    *Reference*:
    (1) M. V. Ruano, et al., "An improved sampling strategy based on trajectory
        design for application of the Morris method to systems with many input
        factors," Journal of Environmental Modelling & Software, vol. 37,
        pp. 103-109, 2012.
 
    :param mu_star_1: array of mu_star obtained with a block size
    :param mu_star_2: array of mu_star obtained with another block size
    :return: the position factor
    """
    if mu_star_1.shape[0] != mu_star_2.shape[0]:
        raise ValueError("The two arrays are not the same length!")

    array_length = mu_star_1.shape[0]

    # Create two empty array
    rank_array_1 = np.empty(array_length, dtype=int)
    rank_array_2 = np.empty(array_length, dtype=int)

    # Fill the arrays with the rank of mu_star arrays
    # sorted in descending order of the value in mu_star, such that
    # array[i] = j => ith element of the array has a rank j
    rank_array_1[np.argsort(mu_star_1)[::-1]] = np.arange(1, array_length + 1)
    rank_array_2[np.argsort(mu_star_2)[::-1]] = np.arange(1, array_length + 1)

    pf = np.sum(np.abs(rank_array_1 - rank_array_2) /
                (rank_array_1 + rank_array_2) / 2)

    return pf
