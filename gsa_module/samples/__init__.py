# -*- coding: utf-8 -*-
"""
    gsa_module.samples
    ~~~~~~~~~~~~~~~~~~

    Package containing routines to generate design of experiments using
    various sampling schemes.
    It currently includes including simple random sampling (``srs``), 
    latin hypercube (``lhs``), optimized latin hypercube (``lhs-opt``), 
    and Sobol' sequence (``sobol``).
"""
from . import cmdln_args
from . import test_sample
from . import hammersley
from . import lhs
from . import lhs_opt
from . import sobol
from . import srs


__author__ = "Damar Wicaksono"
