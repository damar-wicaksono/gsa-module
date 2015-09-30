"""Module to generate Sobol'-Saltelli design used to estimate Sobol' indices
"""
import numpy as np
from .. import samples

__author__ = 'wicaksono_d'


def create(n, k, scheme, params):
    r"""Generate Sobol'-Saltelli design matrix

    :param n: (int) the number of samples
    :param d: (int) the number of dimension
    :param scheme: (str) the scheme to generate the design. e.g., "srs", "lhs",
        "sobol"
    :param params: (list of int) the seed numbers for "srs" and "lhs"
        (list of str) for "sobol" scheme, the fullname of the executable for the
        generator and the file containing direction numbers
    :returns: (dict of ndArray) a dictionary containing pair of keys and numpy
        arrays of which each rows correspond to the normalized (0, 1) parameter
        values for model evaluation
    """