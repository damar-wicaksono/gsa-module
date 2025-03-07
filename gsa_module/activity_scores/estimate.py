import numpy as np

from typing import Dict


def estimate_cc(
    xx: Dict[str, np.ndarray],
    yy: Dict[str, np.ndarray],
    bounds: np.ndarray,
):
    """Estimate the C matrix for the subspace method.

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
        The estimated C matrix.
    """

    # --- Parse input
    sample_size, num_dim = xx["x0"].shape
    diff_bounds = np.diff(bounds, axis=1)

    # --- Initialize output array
    df = np.empty((sample_size, num_dim))

    # Loop over dimension
    for j in range(num_dim):
        key = f"x{j + 1}*"

        # Compute df_dx
        dx_j = xx[key][:, j] - xx["x0"][:, j]
        # C is defined with respect to the domain [-1, 1]^m
        df_dx_j = diff_bounds[j] / 2 * (yy[key] - yy["x0"]) / dx_j
        # Compute nu
        df[:, j] = df_dx_j

    # Compute the C matrix
    cc = np.zeros((num_dim, num_dim))
    for i in range(sample_size):
        cc += df[i, np.newaxis].T @ df[i, np.newaxis]
    cc = cc / sample_size

    return cc


def estimate_scores(
    xx: Dict[str, np.ndarray],
    yy: Dict[str, np.ndarray],
    bounds: np.ndarray,
) -> np.ndarray:
    """Estimate the activity scores.

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
        The estimated activity scores
    """

    # Compute the C matrix
    cc = estimate_cc(xx, yy, bounds)

    # SVD on the matrix
    _, ss, vv_t = np.linalg.svd(cc)

    return np.sum(vv_t.T**2 * ss, axis=1)
