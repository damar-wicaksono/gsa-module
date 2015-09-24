"""Module to generate Sobol' Sequence design matrix
"""
import subprocess
import numpy as np

__author__ = "Damar Wicaksono"


def create(n, d,
           generator="./sa_module/samples/sobol_seq_gen/sobol.o",
           dirnumfile="./sa_modules/samples/sobol_seq_gen/new-joe-kuo-6.21201"):
    r"""Generate `d`-dimensional Sobol' sequence of length `n`

    This function only serves as a wrapper to call a generator from the shell,
    execute it with a file containing the directional numbers.
    The one used here is the generator provided by Joe and Kuo [1] of which the
    technical detail can be found in [2] and [3].

    **Reference:**

    (1) Frances Y. Kuo, Sobol Sequence Generator [C++ Source Code], Feb. 2015,
        http://web.maths.unsw.edu.au/~fkuo/sobol
    (2) S. Joe and F. Y. Kuo, "Remark on Algorithm 659: Implementing Sobol's
        quasirandom sequence generator," ACM Trans. Math. Soft. 29, pp. 49-57,
        2003.
    (3) S. Joe and F. Y. Kuo, "Constructing Sobol sequences with better
        two-dimensional projections," SIAM J. Sci. Comput. 30, pp. 2635-2654,
        2008.

    :param n: (int) the number of samples
    :param d: (int) the number of dimension
    :param generator: (str) the executable fullname for the generator
    :param dirnumfile: (str) the directional numbers fullname
    :returns: (ndarray) a numpy array of `n`-by-`d` filled with Sobol'
        quasirandom sequence
    """
    # input parameters checks
    if (not isinstance(n, int)) or n <= 0:
        raise TypeError
    elif (not isinstance(d, int)) or d <= 0:
        raise TypeError
    else:
        cmd = [generator, str(n), str(d), dirnumfile]

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        # stdout in subprocess is in byte codes
        # convert to string and split into array with newline as separator
        sobol_seq = out.decode("utf-8").split("\n")

        # Remove the last two lines
        sobol_seq.pop(-1)
        sobol_seq.pop(-1)

        # Convert the string into float
        for i in range(len(sobol_seq)):
            sobol_seq[i] = [float(_) for _ in sobol_seq[i].split()]

        # Convert to numpy array
        sobol_seq = np.array(sobol_seq)

    return sobol_seq


def makegen(action="make", gen_sourcedir="./sa_module/samples/sobol_seq_gen"):
    r"""Compile the generator routine from C++ source file

    By default a C++ source is supplied in this module

    :param action: (str) makefile action, make executable or clean
    :param gen_sourcedir: (str) the generator source code directory
    """

    if action == "make":
        cmd = ["make", "all"]
    elif action == "clean":
        cmd = ["make", "clean"]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         cwd=gen_sourcedir)
    out, err = p.communicate()