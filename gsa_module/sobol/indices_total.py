# -*- coding: utf-8 -*-
"""
    gsa_module.sobol.indices_total
    ******************************
    
    Module with functions to calculate the total-order Sobol' indices
"""
import numpy as np

__author__ = "Damar Wicaksono"


def estimate(y_dict: dict, estimator: str="jansen",
             num_bootstrap: int=10000) -> tuple:
    """Calculate the total-order Sobol' sensitivity indices
    
    :param y_dict: a dictionary of numpy array of model outputs
    :param estimator: which estimator to use
    :param num_bootstrap: the number of bootstrap samples
    :return: a tuple of two elements, first is a numpy array of all the 
        total-order indices (length num_dims) and the second is the numpy array
        of the bootstrap samples (num_bootstrap * num_dims)
    """
    # Get some common parameters
    num_dims = len(y_dict) - 2
    num_smpl = y_dict["a"].shape[0]

    # Compute the 1st-order sensitivity indices
    sti = np.empty(num_dims)
    if estimator == "jansen":
        for i in range(num_dims):
            key = "ab_{}" .format(i+1)
            sti[i] = jansen(y_dict["a"], y_dict[key])

    # Conduct the bootstrapping
    if num_bootstrap > 0:
        sti_bootstrap = np.empty([num_bootstrap, num_dims])
        for i in range(num_bootstrap):
            idx = np.random.choice(num_smpl, num_smpl, replace=True)
            for j in range(num_dims):
                key = "ab_{}".format(j + 1)
                sti_bootstrap[i, j] = jansen(y_dict["a"][idx], y_dict[key][idx])
    else:
        sti_bootstrap = None

    return sti, sti_bootstrap


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
