"""Module to generate Sobol'-Saltelli design used to estimate Sobol' indices
"""
import os
import numpy as np
from . import env
import samples

__author__ = 'wicaksono_d'


def create(n, k, scheme, params):
    r"""Generate Sobol'-Saltelli design matrix

    :param n: (int) the number of samples
    :param k: (int) the number of parameters
    :param scheme: (str) the scheme to generate the design. e.g., "srs", "lhs",
        "sobol"
    :param params: (list of int) the seed numbers for "srs" and "lhs"
        (list of str) for "sobol" scheme, the fullname of the executable for the
        generator and the file containing direction numbers
    :returns: (dict of ndArray) a dictionary containing pair of keys and numpy
        arrays of which each rows correspond to the normalized (0, 1) parameter
        values for model evaluation
    """
    # Check the input arguments for n and k
    if (not isinstance(n, int)) or n <= 0:
        raise TypeError
    elif (not isinstance(k, int)) or k <= 0:
        raise TypeError
    elif (not isinstance(params, list)) or len(params) != 2:
        raise TypeError

    # Check the scheme argument and, if valid, generate 2 sample sets
    # of the same dimensions for "sample" (A) and "resample" (B)
    if scheme == "srs":
        if (not isinstance(params[0], int)) or params[0] <= 0:
            raise TypeError
        elif (not isinstance(params[0], int)) or params[1] <= 0:
            raise TypeError
        else:
            a = samples.design_srs.create(n, k, params[0])
            b = samples.design_srs.create(n, k, params[1])
    elif scheme == "lhs":
        if (not isinstance(params[0], int)) or params[0] <= 0:
            raise TypeError
        elif (not isinstance(params[0], int)) or params[1] <= 0:
            raise TypeError
        else:
            a = samples.design_lhs.create(n, k, params[0])
            b = samples.design_lhs.create(n, k, params[1])
    elif scheme == "sobol":
        if (not isinstance(params[0], str)) or (not os.path.exists(params[0])):
            raise TypeError
        elif (not isinstance(params[1], str)) or (not os.path.exists(params[1])):
            raise TypeError
        else:
            ab = samples.design_sobol.create(n, 2*k, params[0], params[1])
            a = ab[:, 0:k]
            b = ab[:, k:2*k]
    else:
        raise NameError

    # Matrix A and B in a python dict
    sobol_saltelli = dict()
    sobol_saltelli["a"] = a
    sobol_saltelli["b"] = b

    # AB_i: replace the i-th column of A matrix by i-th column of B matrix
    # These sets of samples are used to calculate the first- and total-order
    # Sobol' indices (together with A and B)
    for i in range(k):
        key = "ab_{}" .format(str(i+1))
        temp = np.copy(a)
        temp[:,i] = b[:,i]
        sobol_saltelli[key] = temp

    # BA_i: replace the i-th column of B matrix by i-th column of A matrix
    # these sets of samples are used to calculate the second-order Sobol'
    # indices
    for i in range(k):
        key = "ba_{}" .format(i+1)
        temp = np.copy(b)
        temp[:,i] = a[:,i]
        sobol_saltelli[key] = temp

    return sobol_saltelli

def write(sobol_saltelli_dict, tag, format="%1.6e"):
    r"""Write Sobol'-Saltelli design matrices into set of files according to key

    :param sobol_saltelli_dict: (dict of ndArray) the Sobol'-Saltelli matrices
    :param tag: (str) the tag for matrices filenames
    :param format: (str) the print format of the number
    """

    for key in sobol_saltelli_dict:
        fname = "{}_{}.csv" .format(tag, key)
        np.savetxt(fname, sobol_saltelli_dict[key], fmt=format, delimiter=",")