# -*- coding: utf-8 -*-
"""
    gsa_module.test_functions.sobol_g_curved
    ****************************************

    Module implementing the 10-dimensional curved version of Sobol-G function
    Taken from G_2^* test function in (1)

    **References:**

    (1) A. Saltelli et al., "Variance based sensitivity analysis of model output. 
        Design and estimator for the total sensitivity index," 
        Computer Physics Communication, vol. 181, no. 2, pp. 259 - 270, 2010.
"""
import numpy as np

# Constants
ai = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.8, 1, 2, 3, 4])
alpha_i = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

def evaluate(xx: np.ndarray,
             delta_i: np.ndarray, 
             alpha_i: np.ndarray=alpha_i, 
             ai: np.ndarray=ai):
    """Evaluate the curved Sobol-G function

    :param xx: an N-by-D array of inputs
    :param delta_i: an array of length D, random noise [0,1)
    :param alpha_i: an array of length D, function coefficients
    :param ai: an array of length D, function coefficients
    :return: an array of length N, function output
    """
    # Check the dimension of the input
    if (xx.shape[1] != delta_i.shape[0]):
        raise ValueError("The dimension of inputs is not consistent!")
    elif (xx.shape[1] != delta_i.shape[0]):
        raise ValueError("The dimension of inputs is not consistent!")
    elif (xx.shape[1] != alpha_i.shape[0]):
        raise ValueError("The dimension of inputs is not consistent!")
    elif (xx.shape[1] != ai.shape[0]):
        raise ValueError("The dimension of inputs is not consistent!")
    else:
        pass
    
    term1 = (1 + alpha_i)
    term2 =  np.power(np.abs(2 * (xx + delta_i - np.modf(xx + delta_i)[1]) - 1), 
                      alpha_i)
    term3 = 1 + ai
    g_i = (term1 * term2 + ai) / term3

    return np.prod(g_i, axis=1)


def top_marginal_variance(alpha_i: np.ndarray=alpha_i,
                          ai: np.ndarray=ai):
    """Evaluate analytical partial variance
    
    :param alpha_i: the `alpha` coefficients of the function
    :param ai: the `a` coefficients of the function
    :return: the analytical top marginal variance of each parameter
    """
    return np.power(alpha_i, 2) / ((1 + 2 * alpha_i) * np.power((1 + ai), 2))


def marginal_variance(alpha_i: np.ndarray=alpha_i,
                      ai: np.ndarray=ai):
    """Evaluate the analytical marginal variance
    
    
    :param alpha_i: the `alpha` coefficients of the function
    :param ai: the `a` coefficients of the function
    :return: the analytical marginal variance of the function
    """
    vi = top_marginal_variance(alpha_i, ai)

    return np.prod(1 + vi) - 1


def bottom_marginal_variance(alpha_i: np.ndarray=alpha_i,
                             ai: np.ndarray=ai):
    """Evaluate the analytical total variance

    :param alpha_i: the `alpha` coefficients of the function
    :param ai: the `a` coefficients of the function
    :return: the analytical bottom marginal variance of each parameter
    """
    if (alpha_i.shape[0] != ai.shape[0]):
        raise ValueError("Dimension is not consistent!")

    num_dims = alpha_i.shape[0]
    vi = top_marginal_variance(alpha_i, ai)
    vti = []

    for i in range(num_dims):
        vj = 1 + vi[[j for j in range(num_dims) if j != i]]
        vti.append(vi[i] * np.prod(vj))

    return np.array(vti)
