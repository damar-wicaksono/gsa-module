# -*- coding: utf-8 -*-
"""
    gsa_module.sobol.indices_total
    ******************************
    
    Module with functions to calculate the total-effect Sobol' indices
"""
import numpy as np

__author__ = "Damar Wicaksono"


def estimate(y_dict: dict,
             str_estimator: str="jansen",
             num_bootstrap: int=10000) -> tuple:
    """Calculate the total-effect Sobol' sensitivity indices
    
    :param y_dict: a dictionary of numpy array of model outputs
    :param estimator: which estimator to use
    :param num_bootstrap: the number of bootstrap samples
    :return: a tuple of two elements, first is a numpy array of all the 
        total-effect indices (length num_dims) and the second is the numpy 
        array of the bootstrap samples (num_bootstrap * num_dims)
    """
    # Get some common parameters
    num_dims = len(y_dict) - 2
    num_smpl = y_dict["a"].shape[0]

    # Select the estimator
    if str_estimator == "jansen":
        estimator = jansen
    elif str_estimator == "sobol":
        estimator = sobol

    # Compute the total-effect sensitivity indices
    sti = np.empty(num_dims)
    for i in range(num_dims):
        key = "ab_{}" .format(i+1)
        sti[i] = estimator(y_dict["a"], y_dict[key])

    # Conduct the bootstrapping
    if num_bootstrap > 0:
        sti_bootstrap = np.empty([num_bootstrap, num_dims])
        for i in range(num_bootstrap):
            idx = np.random.choice(num_smpl, num_smpl, replace=True)
            for j in range(num_dims):
                key = "ab_{}".format(j + 1)
                sti_bootstrap[i, j] = estimator(y_dict["a"][idx],
                                                y_dict[key][idx])
    else:
        sti_bootstrap = None

    return sti, sti_bootstrap


def jansen(fa: np.ndarray, fab_i: np.ndarray) -> float:
    """Calculate the total-effect Sobol' sensitivity indices using Jansen est.
    
    See the explanation in the last paragraph of pp. 37 in [1]
    
    **References:**
    
    (1) M. J. W. Jansen, "Analysis of variance designs for model output,"
        Computer Physics Communications, 117, pp. 35-43, (1999)
    
    :param fa: numpy array of model output evaluated with input matrix A
    :param fab_i: numpy array of model output with matrix AB_i
    :return: the total-effect sensitivity of parameter i
    """
    # Compute the Variance
    var = np.var(fa, ddof=1)

    sti = 0.5 * np.mean((fa - fab_i)**2) / var

    return sti


def sobol(fa: np.ndarray, fab_i: np.ndarray) -> float:
    """Calculate the total-effect Sobol' sensitivity indices using Sobol est.
    
    See Eq.(8) in [1] for the Sobol estimator 
    and Eq.(47) for the Homma estimator
    
    Sobol [1] and Homma [2] total-effect sensitivity index estimator are 
    equivalent if for Homma, f(a) is used to estimate variance 
    and expectation of y
    
    **References:**
    
    (1) I. M. Sobol', "Global sensitivity analysis for nonlinear mathematical
        models and their Monte Carlo estimates," Mathematics and Computers in
        Simulation, 55, pp. 271-280, (2001)
    (2) T. Homma and A. Saltelli, "Importance measures in global sensitivity 
        analysis of nonlinear models," Reliability Engineering and System 
        Safety, 52, pp. 1-17, (1996)
    
    :param fa: numpy array of model output evaluated with input matrix A
    :param fab_i: numpy arary of model output evaluated with input matrix AB_i
    :return: the total-effect sensitivity index of parameter i
    """
    # Compute the variance
    var = np.var(fa, ddof=1)

    sti = np.mean(fa**2 - fa * fab_i) / var

    return sti
