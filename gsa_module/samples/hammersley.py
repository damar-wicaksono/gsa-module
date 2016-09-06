# -*- coding: utf-8 -*-
"""hammersley.py: python module to generate Hammersley sequence. The
implementation below is taken verbatim from (1) based on algorithm in (2)

It is not recommended to generate a Hammersley sequence more than 10 dimension

 **References**

 (1) https://github.com/PhaethonPrime/hammersley
 (2) T-T. Wong, W-S. Luk, and P-A. Heng, "Sampling with Hammersley and Halton
     Points," Journal of Graphics Tools, vol. 2, no. 2, 1997, pp. 9 - 24.
"""
import numpy as np
from six import moves, iteritems

# this list of primes allows up to a size 120 vector
saved_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
                127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
                193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263,
                269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
                349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421,
                431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
                503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593,
                599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659]


def get_phi(p, k):
    p_ = p
    k_ = k
    phi = 0
    while k_ > 0:
        a = k_ % p
        phi += a/p_
        k_ = int(k_/p)
        p_ *= p
    return phi


def generate_hammersley(n_points=100, n_dims=2,  primes=None):
    primes = primes if primes is not None else saved_primes
    for k in moves.range(n_points):
        points = [k/n_points] + \
                 [get_phi(primes[d], k) for d in moves.range(n_dims-1)]
        yield points


def create(n_points=100, n_dims=2):
    """Wrapper function to generate Hammersley sequence
    """
    hammersley_gen = generate_hammersley(n_points, n_dims)
    hammersley_points = []
    for point in hammersley_gen:
        hammersley_points.append(point)

    return np.array(hammersley_points)
