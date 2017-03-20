# -*- coding: utf-8 -*-
"""sobol.py: Module to generate design matrix by Sobol' sequences

It is based on almost verbatim python conversion of cpp code by Kuo (copyright
below), implementing algorithm by Joe and Kuo [1].

Below is the original copyright notice which includes the copyright for the
included direction number files in "./dirnumfiles/new-joe-kuo-6.21201"

/ Frances Y. Kuo
/
/ Email: <f.kuo@unsw.edu.au>
/ School of Mathematics and Statistics
/ University of New South Wales
/ Sydney NSW 2052, Australia
/
/ Last updated: 21 October 2008
/
/  You may incorporate this source code into your own program
/  provided that you
/  1) acknowledge the copyright owner in your program and publication
/  2) notify the copyright owner by email
/  3) offer feedback regarding your experience with different direction numbers
/
/
/ -----------------------------------------------------------------------------
/ Licence pertaining to sobol.cc and the accompanying sets of direction numbers
/ -----------------------------------------------------------------------------
/ Copyright (c) 2008, Frances Y. Kuo and Stephen Joe
/ All rights reserved.
/
/ Redistribution and use in source and binary forms, with or without
/ modification, are permitted provided that the following conditions are met:
/
/     * Redistributions of source code must retain the above copyright
/       notice, this list of conditions and the following disclaimer.
/
/     * Redistributions in binary form must reproduce the above copyright
/       notice, this list of conditions and the following disclaimer in the
/       documentation and/or other materials provided with the distribution.
/
/     * Neither the names of the copyright holders nor the names of the
/       University of New South Wales and the University of Waikato
/       and its contributors may be used to endorse or promote products derived
/       from this software without specific prior written permission.
/
/ THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
/ EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
/ WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
/ DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
/ DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
/ (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
/ LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
/ ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
/ (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
/ SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
/ -----------------------------------------------------------------------------

    *References*:

    [1] S. Joe and F. Y. Kuo, "Constructing Sobol sequences with better two-
        dimensional projections," SIAM Journal of Scientific Computing,
        vol. 30, pp. 2635-2654 (2008).
"""
import numpy as np

__author__ = "Damar Wicaksono"


def read_dirnumfile(dirnumfile: str, d: int) -> np.ndarray:
    r"""Parser to read direction number file provided by Joe & Kuo

    The parser read direction number file to get parameters "s", "a", and
    "m_i". It only output as many as the requested dimension

    The structure of the file is the following:

        d       s       a       m_i
        2       1       0       1
        3       2       1       1 3
        4       3       1       1 3 1
        5       3       2       1 1 1
        6       4       1       1 1 3 3
        ...

    note that the header is included in the file and the parameters started
    with dimension 2. Dimension 1 is irrelevant as it can be generated without
    direction number. The first column is just the dimension number

    :param dirnumfile: the fullname of the text file containing dir. number
    :param d: the requested dimension number, >= 2
    :return: structured array with columns correspond to params s, a, and m_i
    """
    # Open and read the file
    with open(dirnumfile, "rt") as f:
        lines = f.read().splitlines()
    lines.pop(0)    # Remove first line

    # Prepare the output (d, s, a, m_i)
    max_s = list(map(int, lines[d-1].strip().split()))[1]
    dirnum = np.zeros(d,
                      dtype=[("s", "uint32"),
                             ("a", "uint32"),
                             ("m", "({},)uint32" .format(max_s))])

    # Read and parse line by line
    for i in range(d):
        line = list(map(int, lines[i].strip().split()))
        for j in range(2):
            dirnum[i][j] = line[j+1]
        for j in range(line[1]):
            dirnum[i][2][j] = line[j+3]

    return dirnum


def create(n: int, d: int,
           dirnum: np.ndarray = None,
           excl_nom: bool = False,
           randomize: bool = False,
           seed: int = None) -> np.ndarray:
    r"""Sobol points generator based on graycode order

    This implementation is a verbatim copy of a C++ source code by Joe and Kuo.
    See the module header for complete copyright and references.

    :param n: Number of samples (cannot be greater than 2**32)
    :param d: Number of dimensions
    :param dirnum: the parameters from direction numbers file ("s", "a", "m")
    :param excl_nom: flag to exclude nominal value
    :param randomize: Randomize Sobol' sequence by random shifting
    :param seed: seed number for random shifting randomization
    :return: 2-dimensional design matrix of quasi-random Sobol' sequence
    """
    import math
    import os

    # Use default value for direction number file
    if dirnum is None:
        dirnum = read_dirnumfile(os.path.join(os.path.dirname(__file__),
                                 "./dirnumfiles/new-joe-kuo-6.21201"), d)

    if excl_nom:
        # Add additional point if {0.5} is to be excluded
        n += 1

    # Check if requested number of samples is too large
    if n > 2**32:
        raise ValueError("Number of samples too large (>2**32)!")

    # Check if dirnum is in accordance with the requested dimension
    if d > dirnum.shape[0] + 1:
        raise ValueError("More dimension is asked than the available data!")

    # Copy dirnum structured array to local variable
    s = dirnum["s"]
    a = dirnum["a"]
    m = dirnum["m"]

    # L = Maximum number of bits needed
    L = math.ceil(math.log(float(n))/math.log(2.0))

    # C[i] = index from the right of the first zero bit of i (samples)
    C = np.empty(n, dtype=np.uint32)
    C[0] = 1
    for i in range(1, n):
        C[i] = 1
        value = i
        while value & 1:
            value >>= 1  # (bitwise) right-shift value by 1
            C[i] += 1

    # POINTS[i][j] = the jth component of the ith point with the i indexed from
    #                zero to n-1 and j indexed from 0 to d-1
    # Initialize
    POINTS = np.empty([n,d], dtype=np.float64)
    # First sample is zero
    POINTS[0,:] = 0

    if n > 1:

        # ----- Compute the first dimension -----

        # Compute direction numbers V[1] to V[L], scaled by 2**32
        V = np.empty(L+1, dtype=np.uint32)
        for i in range(1, L+1):
            V[i] = 1 << (32 - i)    # (bitwise) left-shift value by 31

        # Evaluate X[0] to X[n-1], scaled by 2**32, the values of
        # first dimension from i = 1 to i = n-1
        X = np.empty(n, dtype=np.uint32)
        X[0] = 0
        for i in range(1, n):
            X[i] = X[i-1] ^ V[C[i-1]]
            POINTS[i,0] = np.float64(X[i]/2.0**32)

        # ----- Compute the remaining dimension -----
        for j in range(1, d):
            # Outer: loop over dimensions

            # Compute direction numbers V[1] to V[L], scaled by 2**32
            V = np.empty(L+1, dtype=np.uint32)
            if L <= s[j-1]:
                for i in range(1, L+1):
                    V[i] = m[j-1,i-1] << (32 - i)
            else:
                for i in range(1, s[j-1]+1):
                    V[i] = m[j-1,i-1] << (32 - i)
                for i in range(s[j-1]+1, L+1):
                    V[i] = V[i - s[j-1]] ^ (V[i - s[j-1]] >> s[j-1])
                    for k in range(1, s[j-1]):
                        V[i] ^= (((a[j-1] >> s[j-1] - 1 - k) & 1) * V[i-k])

            # Evaluate X[0] to X[N-1], scaled by 2**32
            X = np.empty(n, dtype=np.uint32)
            X[0] = 0
            for i in range(1, n):
                # Inner: loop over samples
                X[i] = X[i - 1] ^ V[C[i - 1]]
                POINTS[i,j] = np.float64(X[i]/2.0**32)

        if excl_nom:
            # Remove the second as it was only the "nominal" set of parameters
            POINTS = np.delete(POINTS, 1, 0)

        # Randomize the design if requested
        if randomize:
            return random_shift(POINTS, seed)

    return POINTS


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
