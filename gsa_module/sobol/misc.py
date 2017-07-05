# -*- coding: utf-8 -*-
"""
    gsa_module.sobol.misc
    *********************

    Module with collection of utilities related to Sobol' sensitivity analysis
    implementation
"""
import numpy as np


def bootstrap_ci(si_bootstrap: np.ndarray,
                 std_err: float=1.96,
                 pct: float=95.) -> np.ndarray:
    """Compute the confidence intervals based on the bootstrap samples

    Two kind of confidence intervals are provided, by default both are the
    95% confidence intervals:

    1. Standard error (normality assumption, +/-1.96*SE gives the coverage)
    2. Percentile confidence intervals, by using order statistics

    **References:**

    (1) G.E.B Archer, A. Saltelli, and I.M. Sobol', "Sensitivity measures,
        ANOVA-like techniques and the use of bootstrap," Journal of Statistical
        Computation and Simulation," vol. 58, pp. 99-120, 1997

    :param si_bootstrap: the bootstrap samples of sensitivity indices estimates
    :param std_err: a factor to multiply the standard error
    :param pct: the percentile confidence interval
    :return: the bootstrap confidence intervals num_dims * 3, 1st column is
        the 1.96 standard error, 2nd column is the (100-pct)/2 percentile,
        and the 3rd column is (100+pct)/2 percentile.
    """
    num_dims = si_bootstrap.shape[1]

    si_bootstrap_ci = np.empty([num_dims, 3])
    si_bootstrap_ci[:, 0] = std_err * np.std(si_bootstrap, axis=0)
    si_bootstrap_ci[:, 1] = np.percentile(si_bootstrap, q=(100 - pct) / 2,
                                          axis=0)
    si_bootstrap_ci[:, 2] = np.percentile(si_bootstrap, q=(100 + pct) / 2,
                                          axis=0)

    return si_bootstrap_ci
