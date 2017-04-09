# -*- coding: utf-8 -*-
"""
    gsa_module.test_functions.ishigami
    **********************************

    Module implementing the Ishigami function given in [1]

    **References**

    (1) T. Homma and A. Saltelli, "Importance measures in global sensitivity
        analysis of nonlinear models," Reliability Engineering and System
        Safety, vol. 52, pp. 1-17, 1996.
"""
import numpy as np


def evaluate(xx: np.ndarray, a: float=7, b: float=0.1) -> np.ndarray:
    """Evaluate the Ishigami function

    The default values of the coefficient are taken from [1]

    **References**

    (1) A. Saltelli et al., "Sensitivity Analysis in Practice,"
        John Wiley & Sons: West Sussex, 2004, pp. 196

    :param xx: an n-by-3 array
    :param a: first-order coefficient
    :param b: second-order coefficient
    :return: an array of length n
    """
    # Error checking, if the input is within domain
    if xx.shape[1] != 3:
        raise ValueError("The dimension of inputs <> 3!")
    elif (xx + np.pi < 1e-4).any():
        raise ValueError("Input is smaller than -pi!")
    elif (xx - np.pi > 1e-4).any():
        raise ValueError("Input is larger than +pi!")
    else:
        pass

    ishigami = np.sin(xx[:, 0]) + \
               a * np.sin(xx[:, 1])**2 + \
               b * xx[:, 2]**4 * np.sin(xx[:, 0])

    return ishigami
