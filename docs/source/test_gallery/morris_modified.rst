
------------------------
Modified Morris Function
------------------------

A modified version of test function appeared in Morris' original article [1]_
is used as a test function in this module. Instead of 20-dimensional function,
the modified version is only 4-dimensional and truncated as follows,

.. math::

    f(\underline x) = \sum_{i=1}^{4} \beta_i x_i + \sum_{i\leq j}^4 \beta_{i,j} x_i x_j

.. math::

    \beta_i = \left[ 0.05, 0.59, 10.0, 0.21 \right ]

.. math::

    \beta_{i,j} = \left [\begin{matrix}
        0 & 80 & 60   & 40 \\
        0 & 30 & 0.73 & 0.18 \\
        0 & 0  & 0.64 & 0.93 \\
        0 &  0 & 0.0  & 0.06
    \end{matrix} \right ]


References
----------

.. [1] Max D. Morris, "Factorial Sampling Plan for Preliminary Computational
       Experiments," Technometrics, vol. 33, no. 2, pp. 161 - 174, 1991.