# -*- coding: utf-8 -*-
"""srs.py: Module to generate a design matrix by Simple Random Sample (SRS)
"""
import numpy as np

__author__ = "Damar Wicaksono"


def create(n: int, d: int, seed: int) -> np.ndarray:
    r"""Generate `n` samples of `d` dimension using Simple Random Sampling

    The function returns a numpy array of `n`-rows and `d`-dimension filled
    with randomly generated number from uniform variate of [0, 1].

    :param n: (int) the number of samples
    :param d: (int) the number of dimension
    :param seed: (int) the random seed number
    :returns: (ndarray) a numpy array of `n`-by-`d` filled with randomly
        generated random numbers of uniform variate
    """
    if seed is not None:
        np.random.seed(seed)

    return np.random.rand(n, d)
