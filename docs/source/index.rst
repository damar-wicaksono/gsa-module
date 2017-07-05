.. gsa-module documentation master file, created by
   sphinx-quickstart on Thu Sep 22 18:18:31 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

``gsa-module`` Package
======================

``gsa-module`` is a Python3 package implementing several global sensitivity
analysis methods for computer/simulation experiments.
The implementation is based on a black-box approach where the computer model
(or any generic function) is externally implemented to the module itself.
The module accepts the model outputs and the design of experiment (optional,
only for certain methods) and compute the associated sensitivity measures.
The package also includes routines to generate normalized design of experiment
file to be used in the simulation experiment based on several algorithms (such
as simple random sampling or latin hypercube) as well as simple routines to
post-processed multivariate raw code output such as its maximum, minimum, or
average.

The general calculation flow chart involved in using the ``gsa-module`` can
be seen in the figure below.

.. image:: ../figures/flowchart.png

``gsa-module`` Documentation
============================

.. toctree::
   :maxdepth: 2

   basics
   user_guide
   implementation
   developer_guide
   about
   test_gallery

``gsa-module`` Modules reference documentation
==============================================

.. toctree::
   :maxdepth: 1

   modules/samples
   modules/morris
   modules/sobol
   modules/test_functions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

