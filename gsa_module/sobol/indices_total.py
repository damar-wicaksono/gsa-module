# -*- coding: utf-8 -*-
"""
    gsa_module.sobol.indices_total
    ******************************
    
    Module with functions to calculate the total-order Sobol' indices
"""
import numpy as np

__author__ = "Damar Wicaksono"


def evaluate(y_dict: dict, estimator: str="jansen") -> dict:
    """Calculate the total-order Sobol' sensitivity indices
    
    :param y_dict: a dictionary of numpy array of model outputs
    :param estimator: which estimator to use
    :return: a numpy array of all the total-order indices
    """
    # Get some common parameters
    num_dimensions = len(y_dict) - 2

    # Compute the 1st-order sensitivity indices
    sti = np.empty(num_dimensions)
    if estimator == "jansen":
        for i in range(num_dimensions):
            key = "ab_{}" .format(i+1)
            sti[i] = jansen(y_dict["a"], y_dict[key])

    return sti


def jansen(fa: np.ndarray, fab_i: np.ndarray) -> float:
    """Calculate the total-order Sobol' sensitivity indices using Jansen est. 
    
    :param fa: numpy array of model output evaluated with input matrix A
    :param fab_i: numpy array of model output with matrix AB_i
    :return: the total order sensitivity of parameter i
    """
    # Compute the Variance
    var = np.var(fa, ddof=1)

    sti = 0.5 * np.mean((fa - fab_i)**2) / var

    return sti
