# -*- coding: utf-8 -*-
"""
    gsa_module.test_functions.morris_modified
    *****************************************

    Module implementing the 4-dimensional modified Morris function, originally
    appeared as 20-dimensional scalar function appeared in [1].

    **References**

    (1) Max D. Morris, "Factorial Sampling Plan for Preliminary Computational
        Experiments," Technometrics, vol. 33, no. 2, pp. 161 - 174, 1991.
"""
import numpy as np

# Constants, the model coefficients
Bi = np.array([0.05, 0.59, 10.0, 0.21])
Bij = np.array([[0, 80, 60, 40],
                [0, 30, 0.73, 0.18],
                [0, 0, 0.64, 0.93],
                [0, 0, 0, 0.06]])


def evaluate(xx: np.ndarray,
             bi: np.ndarray = Bi, bij: np.ndarray = Bij) -> np.ndarray:
    """Evaluate the modified Morris function

    :param xx: an n-by-3 array
    :param bi: the 1st-order coefficient
    :param bij: the 2nd-order coefficient
    :return: an array of length n
    """
    # Error checking, if the input is within domain
    if (xx.shape[1] != 4):
        raise ValueError("The dimension of inputs <> 4!")
    elif (xx < 1e-4).any():
        raise ValueError("Input is smaller than 0 or too small!")
    elif (xx - 1 > 1e-4).any():
        raise ValueError("Input is larger than 1!")
    else:
        pass

    term1 = np.sum(bi * xx, axis=1)
    term2 = 0.0
    for i in range(4):
        term2 += xx[:, i] * np.sum(bij[i, :]*xx, axis=1)

    return term1+term2
