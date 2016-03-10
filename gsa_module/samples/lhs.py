# -*- coding: utf-8 -*-
"""lhs1.py: Module to generate design matrix from Latin Hypercube Sampling (LHS)
"""
import numpy as np

__author__ = "Damar Wicaksono"


def create(n: int, d: int, seed: int = -1) -> np.ndarray:
    """Generate `n` samples of `d` dimension design matrix

    The function returns a numpy array of n-row and d-dimension filled with
    randomly generated number from uniform variate of [0, 1].
    The sampling is done in stratified manner to ensure that each 1/n interval
    is represented by the samples, see [1] for additional detail.

    **Reference**:

    (1) Michael D. McKay, R. J. Beckman, and W. J. Conover, "A Comparison of
        Three Methods for Selecting Values of Input Variables in the Analysis
        of Output from a Computer Code," Technometrics, vol. 42(1), pp. 55-61,
        2000.

    :param n: (int) the number of samples
    :param d: (int) the number of dimension
    :param seed: (int) the random seed number
    :returns: (ndarray) a numpy array of `n`-by-`d` filled with randomly
        generated random numbers of uniform variate in LHS class
    """
    if (not isinstance(n, int)) or n <= 0:
        raise TypeError
    elif (not isinstance(d, int)) or d <= 0:
        raise TypeError
    elif (not isinstance(seed, int)) or seed <= 0:
        np.random.seed()
    else:
        np.random.seed(seed)

    dm = np.empty([n, d])

    for j in range(d):
        for i in range(n):
            dm[i, j] = np.random.uniform(low=i/n, high=(i+1)/n)

        if j > 0:
            # Shuffle only the d-1 dimension
            np.random.shuffle(dm[:, j])

    return dm


def ese_optimized(n: int, d: int, num_candidates: int = 100, params: list = []):
    """Generate an optimized LHS using Enhanced Stochastic Evolutionary Alg.

    Generate `num_candidates` number of initial LHS design, optimize each using
    the enhanced stochastic evolutionary algorithm and return the best design
    with respect to the objective function

    :param n: the number of samples
    :param d: the number of dimension
    :param num_candidates: the number of initial LHS generated
    :param params: list of parameters of the optimization algorithm
    """
    from .opt_alg.stochastic_evolutionary import optimize

    obj_func_vals = []      # the best objective function of each candidate
    candidates = []         # the optimization result of a candidate

    if params:
        obj_function = params[0]        # the objective function
        threshold_init = params[1]      # initial threshold
        j = params[2]                   # candidates in perturbation
        m = params[3]                   # maximum number of inner iterations
        max_outer = params[4]           # maximum number of outer iterations
        reward = params[5]              # reward calculation flag
        improving_params = params[6]    # improving phase parameters
        exploring_params = params[7]    # exploring phase parameters

    for i in range(num_candidates):
        dm = create(n, d)
        if params:
            candidate = optimize(dm, obj_function, threshold_init, j, m,
                                 max_outer, reward, improving_params,
                                 exploring_params)
        else:
            candidate = optimize(dm)

        obj_func_vals.append(candidate.best_evol[-1])
        candidates.append(candidate)

    return candidates[np.argsort(obj_func_vals)[-1]]