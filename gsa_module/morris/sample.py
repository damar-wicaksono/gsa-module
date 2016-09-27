# -*- coding: utf-8 -*-
"""
    gsa_module.morris.sample
    ************************

    Module implementing method to generate design of experiments specifically
    for Morris screening method

    Two flavors for generating design of experiment for Morris screening
    analysis are implemented:

    1. The trajectory design: the one proposed originally by Morris, also known
       as the winding stair design proposed by Jansen (although comes in a bit
       modified form)
    2. The radial design: the one proposed by Saltelli et al. that uses Sobol'
       low discrepancy sequence to build an OAT design. It is promoted because
       it remove the number of levels from the specification, thus reducing
       additional user-specified parameter
"""
import numpy as np


def trajectory(r: int, k: int, p: int, seed: int) -> np.ndarray:
    r"""Create Morris One-at-a-time design matrix, or the trajectory design

    :param r: the number of trajectories or replications
    :param k: the number of parameters
    :param p: the number of levels, have to be an even number
    :param seed: the seed number for random number generation
    :return: the trajectory design matrix of dimension r*(k+1)-by-k
    """
    # set the seed number
    if seed is None:
        np.random.seed()
    else:
        np.random.seed(seed)

    # Generate B matrix, a strictly lower triangular matrix of 1
    # See [1] for the properties of B matrix
    b = np.tril(np.ones([k+1, k], dtype=int), -1)

    # delta is restricted by the number of levels as recommended in [2] to
    # ensure equally probable parameter space coverage
    delta = p / 2 / (p - 1)
    # Create a diagonal matrix with delta in the diagonal
    delta_diag = np.diag([delta for _ in range(k+1)])

    # Initialize B_star matrix
    b_star = np.empty([r*(k+1), k])

    # Create J matrix, (k + 1)-by-k matrix of 1
    j_k = np.ones([k+1, k])

    # Generate r number of trajectories, each contains k + 1 evaluation points
    for i in range(r):

        # Generate random starting point, x_star
        # Note that not all levels can be selected according to [1]
        # Only the first half of the parameter space is valid to be selected
        x_star = np.empty([k+1, k])
        # Fill in the starting point dimension-by-dimension
        for j in range(k):
            x_star[:, j] = np.random.choice(np.arange(p / 2) / (p - 1))

        # Generate random permutation matrix, p_star
        # See [1] for the properties of the p_star matrix
        permuted = np.random.permutation(k)
        p_star = np.zeros([k, k])
        for j in range(k):
            p_star[j, permuted[j]] = 1

        # Generate random direction matrix, D_star
        # See [1] for the properties of the D_star matrix
        d_star = np.diag([np.random.choice([-1, 1]) for _ in range(k)])

        # Set indices that signify a trajectory in the matrix
        index_list = np.arange(k+1) + i * (k+1)

        # Compute the b_star for each trajectories
        b_star[index_list, :] = np.dot(x_star + np.dot(delta_diag/2,
                                                (np.dot((2*b - j_k), d_star) +
                                                 j_k)), p_star)

    return b_star
