.. gsa_module_implementation_morris:

-----------------------
Morris Screening Method
-----------------------

Elementary Effects
------------------


Statistics of Elementary Effects and Sensitivity Measure
--------------------------------------------------------


Design of Experiment for Screening Analysis
-------------------------------------------

There are two available experimental designs for to carry out the Morris
screening method in ``gsa-module``: the trajectory design and radial OAT design.

Trajectory Design (*Winding Stairs*)
````````````````````````````````````

Trajectory design is the original Morris implementation of the design of
experiment for screening design [1]_. Essentially, it is a randomized
one-at-a-time design where each parameter is perturbed once, similar to that of
the *winding stairs* design proposed by Jansen et al. [2]_. The most important
feature of trajectory design is that it does not return to the original base
point after perturbation, but continue perturbing another dimension for the last
perturbed point. This ensures more efficient parameter space exploration
although requires additional user-defined parameter called *level* [3]_.

A trajectory design is defined by the number of trajectories (`r`),
the number of levels (`p`), and the number of model parameters (`k`).
Each trajectories evaluate the model `(k + 1)` times so the economy of it in
computing the elementary effects statistics is `r * (k+1)` code runs.

A randomized trajectory design matrix is given by :math:`b^*` ([1]_, [4]_),

.. math::

    b^* = (x^* + \frac{\Delta}{2} \times ((2 \times b - j_k) \times d^* + j_k))
    \times p^*

- :math:`b`: a strictly lower triangular matrix of 1s, with dimension of
  `(k + 1)-by-k`
- :math:`x^*`: Random starting point in the parameter space, with dimension of
  `(k + 1)-by-k`
- :math:`d^*`: a k-dimensional diagonal matrix which each element is either +1
  or -1 with equal probability. This matrix determines whether a parameter
  value will decrease or increase.
- :math:`p^*`: `k-by-k` random permutation matrix in which each row contains
  one element equal to 1, all others are 0, and no two columns have 1s in the
  same position. This matrix determines the order in which parameters are
  perturbed.
- :math:`j_k`: `(k + 1)-by-k` matrix of 1s
- :math:`\Delta`: factorial increment in a diagonal matrix of
  `(k + 1)-by-(k + 1)`

Radial Design
`````````````

Miscellaneous Topics
--------------------


References
----------

.. [1] Max D. Morris, "Factorial Sampling Plans for Preliminary Computational
       Experiments", Technometrics, Vol. 33, No. 2, pp. 161-174, 1991.
.. [2] Michiel J.W. Jansen, Walter A.H. Rossing, and Richard A. Daamen, "Monte
       Carlo Estimation of Uncertainty Contributions from Several Independent
       Multivariate Sources," in Predictability and Nonlinear Modelling in
       Natural Sciences and Economics, Dordrecht, Germany, Kluwer Publishing,
       1994, pp. 334 - 343.
.. [3] F. Campolongo, A. Saltelli, and J. Cariboni, "From Screening to
       Quantitative Sensitivity Analysis. A Unified Approach," Computer Physics
       Communications, Vol. 192, pp. 978 - 988, 2011.
.. [4] A. Saltelli et al., "Global Sensitivity Analysis. The Primer," West
       Sussex, John Wiley & Sons, 2008, pp. 114
