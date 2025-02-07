"""
Module with routines to estimate the Shapley effect given evaluated sample.
"""
import numpy as np

from typing import Dict


def estimate(
    permutations: np.ndarray,
    yy: Dict[str, np.ndarray],
) -> np.ndarray:
    """Estimate the values of Shapley effects based on sampled points.

    Parameters
    ----------
    permutations : np.ndarray
        The permutations array of the input variables.
    yy : Dict[str, np.ndarray]
        The blackbox function values evaluated at the sampled points.

    Returns
    -------
    np.ndarray
        The estimated Shapley effect values in a one-dimensional
        array of length $m$, where $m$ is the number of dimensions
        (i.e., input variables)
    """
    sample_size, num_dim = permutations.shape

    thetas = np.zeros((sample_size, num_dim))

    for i in range(sample_size):
        y_0 = yy["a"][i]
        tmp = y_0

        for j in range(num_dim):
            dim_idx = permutations[i, j]
            y_ab = yy[f"ab_{dim_idx + 1}"][i]
            thetas[i, dim_idx] = (y_0 - (tmp + y_ab) / 2.0) * (tmp - y_ab)
            tmp = y_ab

    return np.mean(thetas, axis=0)
