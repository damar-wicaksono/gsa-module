.. gsa_module_implementation_morris:

-----------------------
Morris Screening Method
-----------------------

Elementary Effects
------------------

The elementary effect of parameter `i` is defined [1]_ as follow,

:math:`EE_i = \frac{Y(x_1, x_2, \ldots, x_i + \Delta, \ldots, x_k)
- Y(x_1, x_2, \ldots, x_k)}{\Delta}`

Where :math:`\Delta` is the grid jump.

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

The following is an example of a trajectory design in 2-dimensional input space
with 4 trajectories (or *replicates*).
The input parameter space is uniformly divided into 6 levels.
The filled circles are the random base (nominal) points from which
the random perturbation of the same size (i.e., the grid jump) is
carried out one-at-a-time.

.. image:: ../../figures/trajectory.png

Radial Design
`````````````

Radial design is a design for screening analysis proposed in [3]_.
Similar to trajectory design it is based on an extension of one-at-a-time
design. In the implementation of [3]_, Sobol' quasi-random sequence is
used as the basis. Its main advantage over the trajectory design is
the specification of input discretization level by user is no longer required.
Furthermore, the grid jump will also be varying from one input dimension
to another, and from replicate to replicate incorporating additional
possible sources of variation in the method.

The procedure to generate radial design of `r` replicates is as follow:
 1. Generate Sobol' sequence with dimension `(r+R, 2*k)`. `R` is the shift
    to avoid repetition in the sequence (`R = 4` following [3]_).
 2. The first half of the matrix up to the `r`-th row will serve as the
    base points: :math:`a_i = (x_{i,1}, x_{i,2}, \ldots x_{i,k}) \; ; i = 1,\ldots r`.
    The second half of the matrix, starting from the `R+1`-th
    row will serve as the auxiliary points, from which the perturbed states
    of the base point are created: :math:`b_i = (x_{R+i,k+1}, x_{R+i,k+2}, \ldots x_{R+i,2k}) \; ; i = 1,\ldots r`
 3. For each row of the base points, create a set of perturbed states by
    substituting the value at each dimension by the value from the
    auxiliary points at the same dimension, one at a time.
    For each base point, there will be additional `k` perturbed points.
    For instance the 1st perturbed point of the `i`-th base point is,
    :math:`a^{*,1}_i = (x_{R+i,k+1}, x_{i,2}, \ldots x_{i,k})`, while
    the second is :math:`a^{*,2}_i = (x_{i,1}, x_{R+i,k+2}, \ldots x_{i,k})`.
    In general the `j`-th perturbed point of the `i`-th base point is,
    :math:`a^{*,j}_i = (x_{i,1}, \ldots x_{R+i,k+j}, \ldots x_{i,k})`
 4. A single elementary effect for each input dimension can be computed
    on the basis of function evaluations at `k+1` points:
    1 base point and `k` perturbed points.
 5. Repeat the process until the requested `r` replications have been
    constructed.

As such the radial design has the same economy as the trajectory design,
that is `r * (k+1)` computations for `k`-dimensional model with
`r` replications. The computation of the elementary effect :math:`EE_i`,
however, is slightly different due to the fact that now the grid jump
differs for each input dimension at each replication.

.. math::

    EE^{i}_j = \left|\frac{y(a^{*,j}_i) - y(a_i)}{x_{R+i,k+j} - x_{i,j}}\right|


- :math:`y(a^{*,j}_i)`: function value at `j`-th perturbed point of the `i`-th replicate.
- :math:`y(a_i)`: function value at the base point of the `i`-th replicate.
- :math:`x_{R+i,k+j}`: the perturbed input at dimension `j` of the `i`-th replicate.
- :math:`x_{i,j}`: the base input at dimension `j` of the `i`-th replicate.

As can be seen the average over many replications of the elementary effect
defined above will automatically yield :math:`\mu^*`.

The following is an example of a radial design in 2-dimensional input space
with 4 base points (filled circles), located not necessarily in a specific grid.
The perturbations are carried out from these base points (crosses).
The size of the perturbation differs from input dimension to input
dimension and from replicate to replicate.

.. image:: ../../figures/radial.png

Miscellaneous Topics
--------------------

Optimized Trajectory Design
```````````````````````````

Standardized Elementary Effect
``````````````````````````````

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
