"""
Module with routines to estimate DGSM given evaluated sample points.
"""
import numpy as np

from typing import Dict


def estimate_nu(
    xx: Dict[str, np.ndarray],
    yy: Dict[str, np.ndarray],
):
    """Estimate nu sensitivity measures based on evaluated sample values.

    Parameters
    ----------
    xx : Dict[str, np.ndarray]
        The (input) sample points.
    yy :  Dict[str, np.ndarray]
        The (output) sample points, i.e., the values of the black-box function
        evaluated on the sample points.

    Returns
    -------
    np.ndarray
        The estimated nu for all input variables.

    Notes
    -----
    - nu is the mean squared derivative of a given black-box function with
      respect to each of the inpit variables.
    """

    # --- Parse input
    num_dim = xx["x0"].shape[1]

    # --- Initialize output array
    nu = np.empty(num_dim)

    # Loop over dimension
    for j in range(num_dim):
        key = f"x{j + 1}*"

        # Compute df_dx
        dx_j = xx[key][:, j] - xx["x0"][:, j]
        df_dx_j = (yy[key] - yy["x0"]) / dx_j
        # Compute nu
        nu[j] = np.mean(df_dx_j ** 2)

    return nu


def estimate_dgsm(
    xx: Dict[str, np.ndarray],
    yy: Dict[str, np.ndarray],
    bounds: np.ndarray,
):
    """Estimate DGSM based on evaluated sample values.

    Parameters
    ----------
    xx : Dict[str, np.ndarray]
        The (input) sample points.
    yy :  Dict[str, np.ndarray]
        The (output) sample points, i.e., the values of the black-box function
        evaluated on the sample points.
    bounds : np.ndarray
        An array of shape ``(m, 2)`` where ``m`` is the number of dimensions;
        the first column and second column indicate the lower and upper bounds,
        respectively. Each row corresponds to an input variable.

    Returns
    -------
    np.ndarray
        The estimated DGSM for all input variables.

    Notes
    -----
    - DGSM is the upper bound of the Sobol' total sensitivity index computed
      from nu while taking into account the domain of the probabilistic input
      space.
    - The estimated DGSM below is only valid for function with
      a uniform bounded domain.
    """

    # --- Parse input
    num_dim = bounds.shape[0]

    # --- Compute the output variance
    var_yy = np.var(yy["x0"])

    # --- Initialize output array
    dgsm = np.empty(num_dim)

    # --- Loop over dimension
    # Compute nu
    nu = estimate_nu(xx, yy)
    diff_bounds = np.diff(bounds, axis=1)
    for j in range(num_dim):
        # Compute DGSM (only applies for uniform domains)
        dgsm_j = nu[j] * diff_bounds[j] ** 2 / var_yy / np.pi ** 2

        dgsm[j] = dgsm_j[0]

    return dgsm
