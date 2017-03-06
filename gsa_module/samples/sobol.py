# -*- coding: utf-8 -*-
"""sobol.py: Module to generate design matrix by Sobol' sequences
"""
import subprocess
import numpy as np
import os.path

__author__ = "Damar Wicaksono"


def create(n: int, d: int,
           generator: str, dirnumfile: str, incl_nom: bool,
           randomize: bool,
           seed: int) -> np.ndarray:
    r"""Generate `d`-dimensional Sobol' sequence of length `n`

    This function only serves as a wrapper to call a generator from the shell,
    make and execute it with a file containing the directional numbers.
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
    :param incl_nom: (bool) the flag to include the nominal point at [0.5]^d
    :param randomize: (bool) the flag to randomize the Sobol' design
    :param seed: seed for randomization in random-shift procedure
    :returns: (np.ndarray) a numpy array of `n`-by-`d` filled with Sobol'
        quasirandom sequence
    """
    # input parameters checks
    if (not isinstance(generator, str)) or (not os.path.exists(generator)):
        raise TypeError
    elif (not isinstance(dirnumfile, str)) or (not os.path.exists(dirnumfile)):
        raise TypeError

    if not incl_nom:
        # Add one more point as nominal values will be removed
        n += 1

    cmd = [generator, str(n), str(d), dirnumfile]

    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()

    # stdout in subprocess is in byte codes
    # convert to string and split into array with newline as separator
    sobol_seq = out.decode("utf-8").split("\n")

    # Remove the last two lines
    sobol_seq.pop(-1)
    sobol_seq.pop(-1)

    if not incl_nom:
        # Remove the second as it was only the "nominal" set of parameters
        sobol_seq.pop(1)

    # Convert the string into float
    for i in range(len(sobol_seq)):
        sobol_seq[i] = [float(_) for _ in sobol_seq[i].split()]

    # Convert to numpy array
    sobol_seq = np.array(sobol_seq)

    # Randomize the design if requested
    if randomize:
        return random_shift(sobol_seq, seed)
    else:
        return sobol_seq


def random_shift(dm: np.ndarray, seed: int) -> np.ndarray:
    """Randomize a given Sobol' design by random shifting

    **Reference:**

    (1) C. Lemieux, "Monte Carlo and Quasi-Monte Carlo Sampling," Springer
        Series in Statistics 692, Springer Science+Business Media, New York,
        2009

    :param dm: Original Sobol' design matrix, n-by-d
    :param seed: seed number for randomization
    :returns: Randomized Sobol' design matrix
    """
    if seed is not None:
        np.random.seed(seed)

    # Generate random shift matrix from uniform distribution
    shift = np.repeat(np.random.rand(1, dm.shape[1]), dm.shape[0], axis=0)

    # Return the shifted Sobol' design
    return (dm + shift) % 1
