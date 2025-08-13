# -*- coding: utf-8 -*-
"""
    gsa_module.sobol.indices_1st
    ****************************
    
    Module with functions to calculate the 1st-order Sobol' indices
"""
import numpy as np

__author__ = "Damar Wicaksono"


def estimate(y_dict: dict,
             str_estimator: str="saltelli",
             num_bootstrap: int=10000) -> tuple:
    """Calculate the 1st-order Sobol' sensitivity indices and create a dict

    This is a driver function to call several choices of 1st-order sensitivity
    indices estimators. 
    The input is a dictionary of output vectors with conventional keys: 'a', 
    'b', 'ab_1', etc.

    **References:**

    (1) G.E.B Archer, A. Saltelli, and I.M. Sobol', "Sensitivity measures,
        ANOVA-like techniques and the use of bootstrap," Journal of Statistical
        Computation and Simulation," vol. 58, pp. 99-120, 1997
        
    :param y_dict: a dictionary of numpy array of model outputs
    :param str_estimator: which estimator to use
    :param num_bootstrap: the size of bootstrap sample
    :return: a tuple of two elements, the first is a numpy array of all the 
        first-order indices (length num_dims) and the second is the bootstrap
        samples of the estimates (num_bootstrap * num_dims)
    """
    # Get some common parameters
    num_dims = len(y_dict) - 2
    num_smpl = y_dict["a"].shape[0]

    # Select the estimator
    if str_estimator == "saltelli":
        estimator = saltelli
    elif str_estimator == "janon":
        estimator = janon
    else:
        raise ValueError("Estimator not supported!")

    # Compute the 1st-order sensitivity indices
    si_estimates = np.empty(num_dims)
    for i in range(num_dims):
        key = "ab_{}".format(i + 1)
        si_estimates[i] = estimator(y_dict["b"], y_dict[key], y_dict["a"])

    # Conduct the bootstrapping
    if num_bootstrap > 0:
        si_bootstrap = np.empty([num_bootstrap, num_dims])
        for i in range(num_bootstrap):
            idx = np.random.choice(num_smpl, num_smpl, replace=True)
            for j in range(num_dims):
                key = "ab_{}".format(j + 1)
                si_bootstrap[i, j] = estimator(y_dict["b"][idx],
                                               y_dict[key][idx],
                                               y_dict["a"][idx])
    else:
        si_bootstrap = None

    return si_estimates, si_bootstrap


def janon(fb: np.ndarray, fab_i: np.ndarray, fa: np.ndarray=None) -> float:
    """Calculate the 1st-order Sobol' indices using the Janon estimator

    This function is an implementation of Janon's second estimator given by
    Equation (6), pp. 4, in [1].

    **References:**

    (1) A. Janon, et al., "Asymptotic normality and efficiency of two Sobol'
        index estimators," ESAIM: Probability and Statistics, EDP Sciences,
        2003

    :param fb: numpy array of model output with matrix B
    :param fab_i: numpy array of model output with matrix AB_i
    :param fa: numpy array of model output evaluated w input matrix A (not used)
    :return: (float) the 1st-order index for parameter-i
    """
    # Compute the squared mean according to Janon et al. formulation
    mean_squared = (np.mean((fb + fab_i)/2))**2

    nominator = np.mean(fb * fab_i) - mean_squared
    denominator = np.mean((fb**2 + fab_i**2)/2) - mean_squared

    si = nominator / denominator

    return si


def saltelli(fb: np.ndarray, fab_i: np.ndarray, fa: np.ndarray) -> float:
    """Calculate the 1st-order index for parameter-i using Saltelli estimator

    The implementation below is based on the Sobol'-Saltelli Design given in
    Table 2 of [1] (equation (b)). This estimator is still the same as the one
    proposed in the older publication, given in Table 1 of [2].

    **References:**

    (1) A. Saltelli, et al., "Variance based sensitivity analysis of model
        output. Design and estimator for the total sensitivity index,"
        Computer Physics Communications, 181, pp. 259-270, 2010
    (2) A. Saltelli, "Making best use of model evaluations to compute
        sensitivity indices," Computer Physics Communications, 145, 
        pp. 280-297, 2002

    :param fb: numpy array of model output evaluated with input matrix B
    :param fab_i: numpy array of model output with matrix AB_i
    :param fa: numpy array of model output evaluated with input matrix A
    :return: the first order sensitivity of parameter i
    """
    # Compute the Squared Mean (f(a) * f(b))
    mean_squared = np.mean(fa * fb)

    # Compute the Variance
    var = np.var(fa, ddof=1)

    # Compute the first order sensitivity
    si = (np.mean(fb * fab_i) - mean_squared) / var

    return si
