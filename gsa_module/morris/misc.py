# -*- coding: utf-8 -*-
"""
    gsa_module.misc
    ***************

    Module with collection of utilities related to Morris screening method
    implementation
"""
import numpy as np


def sniff_morris(dm: np.ndarray):
    """Detect the type of Morris design

    It is assumed that if the number of unique absolute grid jump is greater
    than 2 (i.e, 0 and delta) then the design is considered "radial".
    """
    num_dim = dm.shape[1]   # Number of dimensions

    delta = np.array([])
    for i in range(num_dim):
        delta = np.append(delta, np.unique(np.abs(dm[:num_dim,i] - dm[1:(num_dim+1),i])))

    delta = np.unique(delta.round(decimals=4))

    if len(delta) > 2:
        return "radial", None, None
    else:
        num_lev = int(round(2 * delta[1] / (2 * delta[1] - 1)))
        return "trajectory", num_lev, delta[1]
