"""Module to generate Sobol' Sequence design matrix
"""

__author__ = "Damar Wicaksono"


def create(n, d, seed, generator, dirnumfile):
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