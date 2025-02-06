# -*- coding: utf-8 -*-
"""srs.py: Module to generate a design matrix by Simple Random Sample (SRS)
"""
import numpy as np

from typing import Union, Optional
from numpy.random import Generator, RandomState

__author__ = "Damar Wicaksono"


def create(
    n: int,
    d: int,
    seed: Optional[Union[int, Generator, RandomState]],
) -> np.ndarray:
    r"""Generate `n` samples of `d` dimension using Simple Random Sampling

    The function returns a numpy array of `n`-rows and `d`-dimension filled
    with randomly generated number from uniform variate of [0, 1].

    Parameters
    ----------
    n : int
        The number of sample points (i.e., the sample size).
    d : int
        The number of dimension of the input space.
    seed : Optional[Union[int, Generator, RandomState]]
        The seed or the random number generator object.

    Returns
    -------
    np.ndarray
        A numpy array of `n`-by-`d` filled with randomly generated random
        numbers of uniform variate
    """
    if seed is None:
        rng = np.random.default_rng()
    elif isinstance(seed, int):
        rng = np.random.default_rng(seed)
    else:
        rng = seed

    return rng.random((n, d))
