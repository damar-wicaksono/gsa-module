# -*- coding: utf-8 -*-
"""lhs.py: Module to generate design matrix from Latin Hypercube Sampling (LHS)
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


def ese_optimized(n: int, d: int, num_candidates: int = 100, seed: int = -1,
                  obj_function: str = "w2_discrepancy",
                  threshold_init: float = -1.0,
                  j: int = 0,
                  m: int = 0,
                  max_outer: int = 20,
                  reward: bool = True,
                  improving_params: list = [0.1, 0.8],
                  exploring_params: list = [0.1, 0.8, 0.9, 0.7]):
    """Generate an optimized LHS using Enhanced Stochastic Evolutionary Alg.

    Generate `num_candidates` number of initial LHS design, optimize each using
    the enhanced stochastic evolutionary algorithm and return the best design
    with respect to the objective function

    The default parameters of the optimization can be overridden, if necessary.

    :param n: the number of samples
    :param d: the number of dimension
    :param num_candidates: the number of initial LHS generated
    :param seed: the random seed number
    :param obj_function: the objective function to optimize
    :param threshold_init: the initial threshold
    :param j: the number of candidates in perturbation step
    :param m: the maximum number of inner iterations
    :param max_outer: the maximum number of outer iterations
    :param reward: flag to do reward iteration, reduce the current outer loop
        counter by one if a new best solution is found
    :param improving_params: the 2 parameters used in improve process
        (a) the cut-off value to decrease the threshold
        (b) the multiplier to decrease or increase the threshold
    :param exploring_params: the 4 parameters used in explore process
        (a) the cut-off value of acceptance, start increasing the threshold
        (b) the cut-off value of acceptance, start decreasing the threshold
        (c) the cooling multiplier for the threshold
        (d) the warming multiplier for the threshold
    """
    from .opt_alg.stochastic_evolutionary import optimize

    if seed < 0:
        np.random.seed()
    else:
        np.random.seed(seed)

    # Generate num_candidates seed number of reproducibility
    seeds = np.random.uniform(11491, 823525, num_candidates).astype(int)

    obj_func_vals = []      # the best objective function of each candidate
    candidates = []         # the optimization result of a candidate

    for i in range(num_candidates):
        dm = create(n, d, seed=seeds[i])
        candidate = optimize(dm, obj_function, threshold_init, j, m,
                             max_outer, reward, improving_params,
                             exploring_params)

        obj_func_vals.append(candidate.best_evol[-1])
        candidates.append(candidate)

    return candidates[np.argsort(obj_func_vals)[-1]]