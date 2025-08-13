# -*- coding: utf-8 -*-
"""
    gsa_module.samples
    ~~~~~~~~~~~~~~~~~~

    Package with a set of modules to compute Sobol' indices by MC sampling for
    quantitatively rank and screen input parameters based on their respective
    importance in global sensitivity analysis setting
"""
from . import cmdln_args
from . import sobol_saltelli
from . import indices_1st
from . import indices_total
from . import misc


__author__ = 'Damar Wicaksono'
