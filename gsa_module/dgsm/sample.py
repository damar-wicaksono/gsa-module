"""
Module with routines to generate sample for estimating DGSM.
"""
import numpy as np

from numpy.random import Generator, RandomState
from typing import Dict, Optional, Union


def create_srs(
    sample_size: int,
    num_dim: int,
    bounds: np.ndarray,
    *,
    delta: Optional[float] = 1e-6,
    rng: Optional[Union[Generator, RandomState]] = None,
) -> Dict[str, np.ndarray]:
    """Create a sample for estimating DGSM with simple random sampling.

    The total number of required function evaluations to estimate DGSM
    for all input variables is given by

    .. math::

        N (m + 1)

    where:

    - :math:`N` is the sample size
    - :math:`m` is the number of dimensions

    Parameters
    ----------
    sample_size: int
        The (random) sample size to estimate DGSMs.
    num_dim: int
        The number of sample dimension (i.e., input variables).
    bounds: np.ndarray
        An array of shape ``(m, 2)`` where ``m`` is the number of dimensions;
        the first column and second column indicate the lower and upper bounds,
        respectively. Each row corresponds to an input variable.
    delta: float, optional
        The relative perturbation from a base point.
    rng: Union[Generator, RandomState], optional
        The random number generator to generate random sample points.

    Returns
    -------
    Dict[str, np.ndarray]
        The sample input values for evaluation of a function to estimate
        its DGSM. The number of keys is :math:`m + 1`. The key ``x0`` indicates
        the base/reference/nominal points and the keys ``x1*``, ``x2*``, etc.
        indicate the perturbed sample points along a single dimension.
    """

    # --- Create RNG
    if rng is None:
        rng = np.random.default_rng()

    # --- Create a sample of base points
    base_sample = rng.random((sample_size, num_dim))
    # Scale the sample according to uniform bounds
    base_sample = (
        bounds[:, 0] + np.diff(bounds, axis=1).reshape(-1) * base_sample
    )

    # --- Initialize output array
    dgsm_sample = {"x0": base_sample}

    perturbation = delta * base_sample

    # --- Loop over dimension
    for j in range(num_dim):
        tmp = base_sample.copy()
        # Perturb each base point according to the select dimension
        tmp[:, j] += perturbation[:, j]

        # Currently assumed it's a bounded domain
        tmp[tmp[:, j] < bounds[j, 0], j] = bounds[j, 0]
        tmp[tmp[:, j] > bounds[j, 1], j] = bounds[j, 1]

        key = f"x{j + 1}*"
        dgsm_sample[key] = tmp

    return dgsm_sample
