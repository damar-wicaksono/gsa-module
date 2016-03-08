# -*- coding: utf-8 -*-
"""stochastic_evolutionary.py: Module containing functionalities to optimize
a given Latin Hypercube Design using an implementation of Enhanced Stochastic
Evolutionary Algorithm proposed by Jin, Chen, and Sudjianton (2003)
"""
import numpy as np
from . import objective_functions


__author__ = "Damar Wicaksono"


def init_threshold(dm: np.ndarray):
    """

    :param dm:
    :return:
    """
    pass


def num_candidate(dm):
    """

    :param dm:
    :return:
    """
    pass


def max_inner(dm):
    """

    :param dm:
    :return:
    """
    pass


def optimize(dm: np.ndarray,
             obj_functions: str = "w2_discrepancy",
             threshold_init: float = -1.0,
             j: int = 0,
             m: int = 0,
             max_outer: int = 100,
             improving_params: list = [0.1, 0.8],
             exploring_params: list = [0.1, 0.8, 0.9, 0.7]):
    """

    :param dm: the initial design matrix
    :param obj_functions: the objective function used in the optimization
    :param threshold_init: the initial threshold, if negative calculate from
        the recommended value
    :param j: the number of candidates obtained by perturbing current design,
        if 0 calculate from the recommended value
    :param m: the maximum number of inner iterations, if 0 calculate from the
        recommended value
    :param max_outer: the maximum number of outer iterations, served as the
        stopping criterion for the optimization algorithm
    :param improving_params: The 2 parameters used in improving process phase
        (1) the cut-off value to decrease the threshold
        (2) the multiplier to decrease or increase the threshold
    :param exploring_params: The 4 parameters used in exploring process phase
        (1) the cut-off value of acceptance to start increasing the threshold
        (2) the cut-off value of acceptance to start decreasing the threshold
        (3) the cooling multiplier for the threshold
        (4) the warming multiplier for the threshold
    :return: a collection of obj_function evolution and best design
    """
    pass



