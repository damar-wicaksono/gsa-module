
-----------------
Ishigami Function
-----------------

Ishigami function is a 3-dimensional function introduce by Ishigami and Homma
[1]_,

.. math::

    f(\underline x) = \sin x_1 + a \sin^2 x_2 + b x^4_3 \sin x_1

.. math::
    x_i \sim U[-\pi, \pi]; i = 1, 2, 3


the parameters `a` and `b` can be adjusted but have default values of 7 and
0.1, respectively.


Morris Screening Results
------------------------

The function was used to test the implementation of the Morris screening and
most precisely that of the two designs of experiment: the trajectory and radial
designs (see :doc:`../implementation/morris_screening_method`).


.. _sec_ishigami_trajectory:

Trajectory sampling design
==========================

The trajectory effect is the original design proposed by Morris. The design
matrix was generated with: 

- number of trajectories (`r`) equal to 10, 100 and 1000 times the number of
  parameter (`k=3`), 
- and levels (`p`) equal to 4, 8, 12 and 20.

Each generated design was used to evaluate the Morris modified function and the
associated elementary effects were calculated.

The following figures show the :math:`\sigma` vs. :math:`\mu^*` plot for the
four parameters of the Ishigami function for different sets of `r` and `p`
values. Each set of (`r`, `p`) value was repeated 1000 times and a histogram of
the results is presented for each parameter in the figures.

.. image:: ../../figures/MustarSigma_Ishigami_trajectory_30_plevels_4_1000_repet.png
.. image:: ../../figures/MustarSigma_Ishigami_trajectory_30_plevels_20_1000_repet.png
.. image:: ../../figures/MustarSigma_Ishigami_trajectory_300_plevels_4_1000_repet.png
.. image:: ../../figures/MustarSigma_Ishigami_trajectory_300_plevels_20_1000_repet.png

Countrary to the :doc:`morris_modified`, the value of
the elementary design with a level `p=4` is quite different that the values
obtained with the other level values. This remains true for a very large number
of trajectories (i.e. 3000). The predictions with a level of 8 or higher are
consistent. 

We also observe that a number of trajectories equals to 10 times the number of
parameter (i.e. 30) is not sufficient to entirely classified the parameters (as
the histograms of parameters 0 and 2 overlap). A minimum number of trajectories
of about 100 times the number of parameter is necessary for the Ishigami
function to separate the parameters.

.. _sec_ishigami_radial:

Radial sampling design
==========================

The radial sampling design has been proposed by Campagnolo et al. and is
described in more details at :doc:`../implementation/morris_screening_method`.
Only a number of trajectories, here called blocks to differentiate from the
previous design, is required. For testing purposes we investigated, as
previously, numbers of blocks (`r`) equal to 10, 100 and 1000 times the number
of parameter (`k=3`).

Each generated design was used to evaluate the Ishigami function and the
associated elementary effects were calculated.

The following figures show the :math:`\sigma` vs. :math:`\mu^*` plot for the
three parameters of the Ishigami function and for the three sets of `r` values.
Countrary to the trajectory design, the radial design uses the Sobol generator,
which is deterministic. As such no repetitions were performed to investigate the
dispersion of the (:math:`\sigma`, :math:`\mu^*`) values.

.. image:: ../../figures/MustarSigmaPlot_Ishigami_radial_block_30.png
.. image:: ../../figures/MustarSigmaPlot_Ishigami_radial_block_300.png
.. image:: ../../figures/MustarSigmaPlot_Ishigami_radial_block_3000.png

The values are found to be quite stable, even for a block value of `r=30`. They
differ, however, significantly from that obtained with the trajectory design
(Section :ref:`sec_ishigami_trajectory`).

The exact value for the elementary effects were not found in litterature.
However, the sensitivity indices are :math:`S_1=0.3138`, :math:`S_2=0.4424` and
:math:`S_3=0` [1]_. Because :math:`\mu^*` and `S` quantify the same
information, we expect them to be ordered in the same way. Therefore the
results obtained with the radial sampling design appear preferable. 

References
----------

.. [1] T. Homma and A. Saltelli, "Importance measures in global sensitivity
       analysis of nonlinear models," Reliability Engineering and System
       Safety, vol. 52, pp. 1-17, 1996.
.. [2] A. Saltelli et al., "Sensitivity Analysis in Practice," John Wiley
       & Sons: West Sussex, 2004, pp. 196
