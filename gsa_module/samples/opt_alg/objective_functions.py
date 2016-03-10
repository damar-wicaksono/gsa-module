# -*- coding: utf-8 -*-
"""objective_functions.py: Module containing various objective functions used to
optimize a given LHS design
"""
import numpy as np

__author__ = "Damar Wicaksono"


def w2_discrepancy_fast(D: np.ndarray) -> float:
    """The vectorized version of wrap-around L2-discrepancy calculation, faster!

    The formula for the Wrap-Around L2-Discrepancy is taken from Eq.5 of (1)

    :math:`WD^2(D) = -(4/3)^K + 1/N^2 \Sigma_{i,j=1}^{N} \
    Pi_{k=1}^K [3/2 - |x_k^1 - x_k^2| * (1 - |x_k^1 - x_k^2|)]`

    The implementation below uses a vector operation of numpy array to avoid the
    nested loop in the more straightforward implementation

    :param D: the design matrix
    :return: the wrap-around L2-discrepancy
    """

    n = D.shape[0]      # the number of samples
    k = D.shape[1]      # the number of dimension
    delta = [None] * k
    for i in range(k):
        # loop over dimension to calculate the absolute difference between point
        # in a given dimension, note the vectorized operation
        delta[i] = np.abs(D[:, i] - np.reshape(D[:, i], (len(D[:, i]), 1)))

    product = 1.5 - delta[0] * (1 - delta[0])
    for i in range(1, k):
        product *= (1.5 - delta[i] * (1 - delta[i]))

    w2_disc = -1 * (4.0/3.0)**k + 1/n**2 * np.sum(product)

    return w2_disc


def w2_discrepancy(D: np.ndarray) -> float:
    """Calculate the Wrap-around L2-Discrepancy of a design matrix

    The formula for the Wrap-Around L2-Discrepancy is taken from Eq.5 of (1)

    :math:`WD^2(D) = -(4/3)^K + 1/N^2 \Sigma_{i,j=1}^{N} \
    Pi_{k=1}^K [3/2 - |x_k^1 - x_k^2| * (1 - |x_k^1 - x_k^2|)]`

    The implementation below is the most straightforward to calculate the
    discrepancy. The problem is that it involves nested loop which can give a
    performance hit especially for tens of thousand evaluations

    **References**

    (1) K.T. Fang and C.X. Ma, "Wrap-Around L2-Discrepancy of Random Sampling,
    Latin Hypercube, and Uniform Designs," Journal of Complexity, vol. 17,
    pp. 608-624, 2001.

    :param D: The design matrix
    :return: The Wrap-around L2-Discrepancy
    """
    # Auxiliary functions
    def discrepancy(x1, x2):
        """Calculate the discrepancy between two points in the design

        :math: `Pi_{k=1}^K [3/2 - |x_k^1 - x_k^2| * (1 - |x_k^1 - x_k^2|)]`

        where `k` is the index for design dimension

        :param x1: First point in the design
        :param x2: Second point in the design
        :return: Discrepancy between the two points
        """
        disc = 1.5 - np.multiply(np.abs(x1-x2), (1.0 - np.abs(x1-x2)))
        return np.prod(disc)

    def discrepancy_matrix(D):
        """Construct discrepancy matrix for all points in the design

        :param D: The design matrix
        :return: A matrix with elements of discrepancy between points
        """
        N = D.shape[0]
        disc_matrix = np.empty((N, N))
        for i in range(N):
            for j in range(N):
                disc_matrix[i,j] = discrepancy(D[i,:], D[j,:])

        return disc_matrix

    disc_matrix = discrepancy_matrix(D)
    N = D.shape[0]  # Number of points, rows in D
    K = D.shape[1]  # Number of dimensions, columns in D
    w2_disc = -1 * (4.0/3.0)**K + 1.0/N**2 * np.sum(disc_matrix)

    return w2_disc
