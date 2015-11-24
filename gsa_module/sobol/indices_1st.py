# -*- coding: utf-8 -*-
"""indices_1st.py: Module to calculate the 1st-order Sobol' indices
"""

__author__ = "Damar Wicaksono"


def evaluate(y_dict: dict,
             estimator="sobol-saltelli",
             bootstrap=True,
             bootstrap_n=10000,
             bootstrap_seed=20151418):
    """Calculate the 1st-order Sobol' sensitivity indices
    """
    pass


def janon():
    """Calculate the 1st-order Sobol' indices using the Janon estimator
    """
    pass


def sobol_saltelli():
    """Calculate the 1st-order Sobol' indices using the Sobol'-Saltelli est.
    """
    pass
