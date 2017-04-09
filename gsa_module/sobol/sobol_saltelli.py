# -*- coding: utf-8 -*-
"""
    gsa_module.sobol.sobol_saltelli
    *******************************
    
    Module to generate a set of Sobol'-Saltelli design matrices (or sampling-
    resampling matrices)
    The design matrices will be used to evaluate model which outputs are used 
    to compute the Monte Carlo estimates of the Sobol' indices
"""
import numpy as np
from ..samples import srs, lhs, sobol

__author__ = "Damar Wicaksono"


def create(num_samples: int, num_dimensions: int,
           sampling_scheme: str="srs",
           seed_number: int=None,
           dirnum: np.ndarray=None,
           interaction: bool=False):
    r"""Generate Sobol'-Saltelli design matrices

    Sobol'-Saltelli design matrices are used to calculate the Sobol' sensitivity
    indices using Monte Carlo simulation by sampling-resampling scheme as
    proposed in [1]. The design requires :math:`n \times (k+2)` function
    evaluations for the 1st-order and the total-order sensitivity indices and
    :math:`n \times (2k+2)` function evaluations for additional 2nd-order
    sensitivity indices. Where `n` is the number of samples and `k` is the
    number of parameters.

    **References:**

    (1) Andrea Saltelli, et al., "Variance based sensitivity analysis of model
        output. Design and estimator for the total sensitivity index," Computer
        Physics Communications, 181, pp. 259-270, (2010)

    :param num_samples: the number of Monte Carlo samples to do the estimation
    :param num_dimensions: the number of dimensions (or parameters)
    :param sampling_scheme: the sampling scheme to generate the design
    :param seed_number: the random seed number if sampling_scheme == srs | lhs
    :param dirnum: the direction numbers for Sobol' sequence
    :param interaction: flag to generate matrices used for 2nd order 
        interaction indices estimation
    :return: (dict of ndarray) a dictionary containing pair of keys and numpy
        arrays of which each rows correspond to the normalized (0, 1) parameter
        values for model evaluation
    """
    # short names for local variables
    n = num_samples
    d = num_dimensions

    if sampling_scheme == "lhs":
        ab = lhs.create(n, 2*d, seed_number)
    elif sampling_scheme == "sobol":
        # Exclude the first two rows because each has the same values
        ab = sobol.create(n+2, 2*d, dirnum)
        ab = ab[2:]
    else:
        ab = srs.create(n, 2*d, seed_number)

    a = ab[:,:d]
    b = ab[:,d:]

    sobol_saltelli = dict()
    sobol_saltelli["a"] = a
    sobol_saltelli["b"] = b

    # AB_i: replace the i-th column of A matrix by i-th column of B matrix
    # These sets of samples are used to calculate the first- and total-order
    # Sobol' indices (together with A and B)
    for i in range(num_dimensions):
        key = "ab_{}" .format(str(i+1))
        temp = np.copy(a)
        temp[:, i] = b[:, i]
        sobol_saltelli[key] = temp

    if interaction:
        # BA_i: replace the i-th column of B matrix by i-th column of A matrix
        # these sets of samples are used to calculate the second-order Sobol'
        # indices
        for i in range(num_dimensions):
            key = "ba_{}" .format(i+1)
            temp = np.copy(b)
            temp[:, i] = a[:, i]
            sobol_saltelli[key] = temp

    return sobol_saltelli


def write(sobol_saltelli: dict, output_header: str, fmt="%1.6e"):
    """Write Sobol'-Saltelli design matrices into set of files according to key

    The files will be written in csv format, each is a complete design matrix

    :param sobol_saltelli: (dict of np.ndArray) the Sobol'-Saltelli matrices
    :param output_header: the header for the  filenames, for identifier purpose
    :param fmt: the print format of the number
    """

    for key in sobol_saltelli:
        fname = "{}_{}.csv" .format(output_header, key)
        np.savetxt(fname, sobol_saltelli[key], fmt=fmt, delimiter=",")
