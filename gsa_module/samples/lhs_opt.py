# -*- coding: utf-8 -*-
"""lhs_opt.py: Module to generate design matrix from an optimized
Latin Hypercube design
"""
import numpy as np
from . import lhs

__author__ = "Damar Wicaksono"


def create_ese(n: int, d: int, seed: int, max_outer: int,
               obj_function: str="w2_discrepancy",
               threshold_init: float=0,
               num_exchanges: int=0,
               max_inner: int = 0,
               improving_params: list = [0.1, 0.8],
               exploring_params: list = [0.1, 0.8, 0.9, 0.7]) -> np.ndarray:
    """Generate an optimized LHS using Enhanced Stochastic Evolutionary Alg.

    The default parameters of the optimization can be overridden, if necessary.

    :param n: the number of samples
    :param d: the number of dimension
    :param seed: the random seed number
    :param max_outer: the maximum number of outer iterations
    :param obj_function: the objective function to optimize
    :param threshold_init: the initial threshold
    :param num_exchanges: the number of candidates in perturbation step
    :param max_inner: the maximum number of inner iterations
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

    # If dimension is less than 2, abort optimization
    if d < 2:
        raise ValueError("Dimension less than 2, optimization irrelevant!")

    if seed is not None:
        np.random.seed(seed)

    # Create initial LHD sample
    dm = lhs.create(n, d, seed=seed)

    # Optimize the LHD sample
    dm_opt = optimize(dm, obj_function, threshold_init, num_exchanges,
                      max_inner, max_outer, improving_params, exploring_params)

    return dm_opt.dm_best
