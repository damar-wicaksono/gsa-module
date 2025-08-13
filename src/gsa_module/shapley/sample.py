"""
Module with routines to generate sample for estimating the Shapley effects.
"""
import numpy as np

from numpy.random import Generator, RandomState
from typing import Dict, Optional, Tuple, Union


GENERATOR_TYPES = Union[Generator, RandomState]


def create_srs(
    sample_size: int,
    num_dim: int,
    rng: Optional[GENERATOR_TYPES] = None,
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """Generate dictionary of sample points to estimate Shapley effects.

    Following the estimator of Goda.

    Parameters
    ----------
    sample_size : int
        The sample size to estimate the Shapley effects.
    num_dim: int
        The number of sample dimension (i.e., input variables).
    rng : GENERATOR_TYPES, optional
        Random number generator; if not specified, a default NumPy random
        number generator will be created using the system state.

    Returns
    -------
    Tuple[np.ndarray, Dict[str, np.ndarray]]
        The random permutation array and the dictionary of sample input values.
        The dictionary keys are "a", "ab_1", "ab_2", etc.
    """
    # --- Parse the RNGs
    if rng is None:
        rng = np.random.default_rng()

    # --- Create two independent sample points
    xx = rng.random((sample_size, num_dim))
    yy = rng.random((sample_size, num_dim))

    # --- Initialize outputs
    permutations = np.zeros(shape=(sample_size, num_dim), dtype=int)
    xy = [np.zeros((sample_size, num_dim)) for i in range(num_dim)]

    for i in range(sample_size):
        permutations[i, :] = rng.permutation(num_dim)

        # Deal with the first element of permutation array
        dim_idx = permutations[i, 0]
        # Take the all values from the first sample
        xy[dim_idx][i, :] = xx[i]
        # but, replace the value at dim_idx with the second sample
        xy[dim_idx][i, dim_idx] = yy[i, dim_idx]

        # Loop over the rest of the elements in the permutation array
        for j in range(1, num_dim):
            dim_idx_1 = permutations[i, j - 1]
            dim_idx_2 = permutations[i, j]
            # Fill in the values from previous estimated dimension
            xy[dim_idx_2][i, :] = xy[dim_idx_1][i, :]
            # but replace the value at the dimension with the second sample
            xy[dim_idx_2][i, dim_idx_2] = yy[i, dim_idx_2]

    input_values = {f"ab_{i + 1}": xy[i] for i in range(num_dim)}
    input_values["a"] = xx

    return permutations, input_values
