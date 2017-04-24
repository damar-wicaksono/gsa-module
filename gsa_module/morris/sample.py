# -*- coding: utf-8 -*-
"""
    gsa_module.morris.sample
    ************************

    Module implementing method to generate design of experiments specifically
    for Morris screening method

    Two flavors for generating design of experiment for Morris screening
    analysis are implemented:

    1. The trajectory design: the one proposed originally by Morris [1], also
       known as the winding stair design proposed by Jansen [2] (although
       this one comes in a bit modified form)
    2. The radial design: the one proposed by Saltelli et al. [3] that uses
       Sobol' low discrepancy sequence to build an OAT design. It is promoted
       because it remove the number of levels from the specification,
       thus reducing additional user-specified parameter. Additionally, the
       size of grid jump will also vary from one nominal point to another

    **References**

    (1) Max D. Morris, "Factorial Sampling Plans for Preliminary Computational
        Experiments", Technometrics, Vol. 33, No. 2, pp. 161-174, 1991.
    (2) Michiel J.W. Jansen, Walter A.H. Rossing, and Richard A. Daamen, "Monte
        Carlo Estimation of Uncertainty Contributions from Several Independent
        Multivariate Sources," in Predictability and Nonlinear Modelling in
        Natural Sciences and Economics, Dordrecht, Germany, Kluwer Publishing,
        1994, pp. 334 - 343.
    (3) F. Campolongo, A. Saltelli, and J. Cariboni, "From Screening to
        Quantitative Sensitivity Analysis. A Unified Approach,"
        Computer Physics Communications, Vol. 192, pp. 978 - 988, 2011.
"""
import numpy as np


def trajectory(r: int, k: int, p: int, seed: int) -> np.ndarray:
    r"""Create Morris One-at-a-time design matrix, or the trajectory design

    See theory section in the documentation for the references

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


def radial(r: int, k: int, dirnum: np.ndarray = None,
           shift_exclude: int = 4) -> np.ndarray:
    """Generate DOE for Morris using radial sampling scheme

    :param r: the number of blocks/replications/trajectories
    :param k: the number of dimensions/parameters
    :param dirnum: the numpy array with direction number parameters
    :param shift_exclude: the lower shift for the half of the design with which
        the first half is subtracted
    :return: the radial design matrix of dimension r*(k+1)-by-k
    """
    import math
    from .. import samples

    # Generate Sobol quasi-random sequence, twice the size of dimensions
    sobol_seq = samples.sobol.create(r+shift_exclude, 2*k, dirnum)

    # Generate the radial design
    dm = np.zeros((r*(k+1), k))
    for i in range(r):
        # Set indices that signify a given block in the matrix
        index_list = np.arange(k+1) + i * (k+1)
        dm[index_list[0], :] = sobol_seq[i, :k]  # Base points
        j = 0
        while j < k:
            dm[index_list[j]+1, :] = sobol_seq[i, :k]   # The base point
            # Change the k-th dimension from the auxiliary point
            dm[index_list[j]+1, j] = sobol_seq[i+shift_exclude, k+j]
            if math.isclose(dm[index_list[0], j], dm[index_list[j] + 1, j]):
                # Perturbation zero, shift downward the auxiliary points, use
                # that point, and add additional point to the auxiliary points
                j = 0
                shift_exclude += 1
                sobol_seq = samples.sobol.create(r + shift_exclude, 2 * k,
                                                 dirnum=dirnum,
                                                 excl_nom=False,
                                                 randomize=False,
                                                 seed=None)
            else:
                j += 1

    return dm
