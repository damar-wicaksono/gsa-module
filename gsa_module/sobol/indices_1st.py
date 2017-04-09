# -*- coding: utf-8 -*-
"""
    gsa_module.sobol.indices_1st
    ****************************
    
    Module with functions to calculate the 1st-order Sobol' indices
"""
import numpy as np

__author__ = "Damar Wicaksono"


def evaluate(y_dict: dict, estimator: str="sobol-saltelli") -> np.ndarray:
    """Calculate the 1st-order Sobol' sensitivity indices and create a dict

    This is a driver function to call several choices of 1st-order index
    estimators. The input is a dictionary of output vectors.

    :param y_dict: a dictionary of numpy array of model outputs
    :param estimator: which estimator to use
    :return: a numpy array of all the first-order indices
    """
    # Get some common parameters
    num_dimensions = len(y_dict) - 2

    # Compute the 1st-order sensitivity indices
    si = np.empty(num_dimensions)
    if estimator == "sobol-saltelli":
        for i in range(num_dimensions):
            key = "ab_{}" .format(i+1)
            si[i] = sobol_saltelli(y_dict["a"], y_dict["b"], y_dict[key])
    elif estimator == "janon":
        for i in range(num_dimensions):
            key = "ab_{}" .format(i+1)
            si[i] = janon(y_dict["b"], y_dict[key])

    return si


def bootstrap(y_dict: dict, estimator="sobol-saltelli",
              n_samples=10000, seed=20151418) -> dict:
    """Generate bootstrap samples and calculate the confidence intervals

    Two kind of confidence intervals are provided, both are 95% confidence
    intervals:
        1. Standard error (normality assumption, +/-1.96*SE gives the coverage)
        2. Percentile confidence intervals, by using order statistics

    **References:**

    (1) G.E.B Archer, A. Saltelli, and I.M. Sobol', "Sensitivity measures,
        ANOVA-like techniques and the use of bootstrap," Journal of Statistical
        Computation and Simulation," vol. 58, pp. 99-120, 1997

    :param y_dict: a dictionary of numpy array of model outputs
    :param estimator: (str)
    :param n_samples:
    :param seed:
    """
    pass


def janon(fb: np.ndarray, fab_i: np.ndarray) -> float:
    """Calculate the 1st-order Sobol' indices using the Janon estimator

    This function is an implementation of Janon's second estimator given by
    Equation (6), pp. 4, in [1].

    **References:**

    (1) A. Janon, et al., "Asymptotic normality and efficiency of two Sobol'
        index estimators," ESAIM: Probability and Statistics, EDP Sciences,
        2003

    :param fb: numpy array of model output with matrix B
    :param fab_i: numpy array of model output with matrix AB_i
    :return: (float) the 1st-order index for parameter-i
    """
    # Compute the squared mean according to Janon et al. formulation
    mean_squared = (np.mean((fb + fab_i)/2))**2

    nominator = np.mean(fb * fab_i) - mean_squared
    denominator = np.mean((fb**2 + fab_i**2)/2) - mean_squared

    si = nominator / denominator

    return si


def sobol_saltelli(fa: np.ndarray, fb: np.ndarray, fab_i: np.ndarray) -> float:
    """Calculate the 1st-order index for parameter-i using Sobol'-Saltelli

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

    :param fa: numpy array of model output evaluated with input matrix A
    :param fb: numpy array of model output evaluated with input matrix B
    :param fab_i: numpy array of model output with matrix AB_i
    :return: the first order sensitivity of parameter i
    """
    # Compute the Squared Mean (f(a) * f(b))
    mean_squared = np.mean(fa * fb)

    # Compute the Variance
    var = np.var(fa, ddof=1)

    # Compute the first order sensitivity
    si = (np.mean(fb * fab_i) - mean_squared) / var

    return si
