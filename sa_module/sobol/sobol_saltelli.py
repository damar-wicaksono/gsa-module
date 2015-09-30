"""Module to generate Sobol'-Saltelli design used to estimate Sobol' indices
"""
import numpy as np
from . import env
import samples

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
    # Generate 2 sample sets of the same dimensions for "sample" and "resample"
    if scheme == "srs":
        a = samples.design_srs.create(n, k, params[0])
        b = samples.design_srs.create(n, k, params[1])
    elif scheme == "lhs":
        a = samples.design_lhs.create(n, k, params[0])
        b = samples.design_lhs.create(n, k, params[1])
    elif scheme == "sobol":
        ab = samples.design_sobol.create(n, 2*k, params[0], params[1])
        a = ab[:, 0:k]
        b = ab[:, k:2*k]
    else:
        raise NameError