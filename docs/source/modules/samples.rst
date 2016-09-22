.. _gsa_modules_packages_samples:


Samples Package
===============

Routines to generate generic purpose design of experiment, including simple
random sampling (``srs``), latin hypercube (``lhs``), optimized latin hypercube
(``lhs-opt``), and Sobol' sequence (``sobol``).

.. _srs:

:mod:`gsa_module.samples.srs`
-----------------------------

.. automodule:: gsa_module.samples.srs
    :members:
    :undoc-members:

.. _lhs:

:mod:`gsa_module.samples.lhs`
-----------------------------

.. automodule:: gsa_module.samples.lhs
    :members:
    :undoc-members:

.. _lhs_opt:

:mod:`gsa_module.samples.lhs_opt`
---------------------------------

.. automodule:: gsa_module.samples.lhs_opt
    :members:
    :undoc-members:

.. _sobol:

:mod:`gsa_module.samples.sobol`
-------------------------------

.. automodule:: gsa_module.samples.sobol
    :exclude-members: random_shift
    :members:
    :undoc-members:

Randomization of the quasi-MC samples can be achieved in the easiest manner by
random shift (or the Cranley-Patterson rotation).

.. autofunction:: gsa_module.samples.sobol.random_shift