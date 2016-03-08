# -*- coding: utf-8 -*-
"""objective_functions.py: Module containing various objective functions used to
optimize a given LHS design
"""
import numpy as np

__author__ = "Damar Wicaksono"


def w2_discrepancy(D: np.ndarray) -> float:
    """Calculate the Wrap-around L2-Discrepancy of a design matrix

    The formula for the Wrap-Around L2-Discrepancy is taken from Eq.5 of (1)

    :math:`WD^2(D) = -(4/3)^K + 1/N^2 \Sigma_{i,j=1}^{N} \
    Pi_{k=1}^K [3/2 - |x_k^1 - x_k^2| * (1 - |x_k^1 - x_k^2|)]`

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
        disc = 1.5 - np.multiply(np.abs(x1-x2), (1-np.abs(x1-x2)))
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
