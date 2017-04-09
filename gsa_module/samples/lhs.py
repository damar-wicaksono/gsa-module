# -*- coding: utf-8 -*-
"""lhs.py: Module to generate design matrix from Latin Hypercube Sampling (LHS)
"""
import numpy as np

__author__ = "Damar Wicaksono"


def create(n: int, d: int, seed: int) -> np.ndarray:
    """Generate `n` samples of `d` dimension design matrix

    The function returns a numpy array of n-row and d-dimension filled with
    randomly generated number from uniform variate of [0, 1].
    The sampling is done in stratified manner to ensure that each 1/n interval
    is represented by the samples, see [1] for additional detail.

    **Reference**:

    (1) Michael D. McKay, R. J. Beckman, and W. J. Conover, "A Comparison of
        Three Methods for Selecting Values of Input Variables in the Analysis
        of Output from a Computer Code," Technometrics, vol. 42(1), pp. 55-61,
        2000.

    :param n: (int) the number of samples
    :param d: (int) the number of dimension
    :param seed: (int) the random seed number
    :returns: (ndarray) a numpy array of `n`-by-`d` filled with randomly
        generated random numbers of uniform variate in LHS class
    """
    if seed is not None:
        np.random.seed(seed)

    dm = np.empty([n, d])

    for j in range(d):
        for i in range(n):
            dm[i, j] = np.random.uniform(low=i/n, high=(i+1)/n)

        if j > 0:
            # Shuffle only the d-1 dimension
            np.random.shuffle(dm[:, j])

    return dm
