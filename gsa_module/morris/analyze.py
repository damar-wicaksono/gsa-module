# -*- coding: utf-8 -*-
"""
    gsa_module.morris.analyze
    *************************

    Module implementing method to analyze output computed using one
    of the screening design of experiment.
    The importance of parameter can be assessed based on the statistics
    of their elementary effects.
    The computation of the elementary effects differs for the two different
    design. Both of them can also be standardized if necessary.
"""
import numpy as np
import pandas as pd


def trajectory(x_normalized: np.ndarray, x_rescaled: np.ndarray,
               y: np.ndarray, param_names: list):
    r"""Compute the statistics of elementary effects from trajectory design

    :param x_normalized:
    :param x_rescaled:
    :param y:
    :param param_names:
    """
    pass


def radial(x_normalized: np.ndarray, x_rescaled: np.ndarray,
           y: np.ndarray, param_names:list):
    r"""Compute the statistics of elementary effects from radial design

    :param x_normalized:
    :param x_rescaled:
    :param y:
    :param param_names:
    """