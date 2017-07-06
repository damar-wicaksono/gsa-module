.. _gsa_module_sobol_indices:

--------------------------
Sobol' Sensitivity Indices
--------------------------

Sobol' sensitivity indices in ``gsa_module`` are estimated by Monte Carlo procedure.
The output of the model has to be generated using a particular design called the Sobol'-Saltelli design.
To estimate the main- and total-effect indices, 
the number of model evaluations, are related to the number of Monte Carlo samples (`N`) and the number of input dimensions (:math:`k`):

:math:`n_{runs} = N \times (k + 2)`

A set of :math:`k + 2` design matrix files can be simultaneously generated using the following command::

    > gsa_sobol_generate -n <number of samples> \
                         -d <number of dimensions> \
                         -ss <sampling scheme {srs, lhs, sobol}> \
                         -o <output filename header> \
                         -sep <the delimiter for the files> \
                         -int <include design matrices to estimate 2nd order> \
                         -s <seed number, for SRS and LHS only> \
                         -dirnum <direction number file, Sobol' only>

Brief explanation of these parameters can be shown by invoking::

    > gsa_sobol_generate --help

The table below lists the complete options/flag in detail with their respective default values.

=== =========== ==================== ======= ======== ============================================================ =========
No. Short Name  Long Name            Type    Required Description                                                  Default
=== =========== ==================== ======= ======== ============================================================ =========
1   -h           --help              flag       No    Show help message                                            False
2   -n           --num_samples       integer    Yes   The number of samples/design points                          None
3   -d           --num_dimensions    integer    Yes   The number of dimensions                                     None
4   -ss          --sampling_scheme   string     No    The method to generate sample {srs, lhs, sobol}              srs
5   -o           --output_header     string     No    The output filename header                                   see below
6   -sep         --delimiter         string     No    The delimiter for the file {csv, tsv, txt}                   csv
7   -int         --interaction       flag       No    Flag to also generate matrices to estimate 2nd-order indices False
8   -s           --seed_number       integer    No    The random seed number (only for LHS and Sobol)              None
9   -dirnum      --direction_numbers string     No    The path to Sobol' sequence generator                        None
10  -V           --version           flag       No    Show the program's version number and exit                   False
=== =========== ==================== ======= ======== ============================================================ =========

Note that options number 8 is valid only for SRS- and LHS-based samples, while option number 9 is valid only for Sobol-based samples. 
Without specifying the output filename header explicitly, the design matrices file will be produced with the following naming convention::

    > <method>_<num_samples>_<num_dimensions>_<matrix_ID>.cs

Example
-------

As an example, by invoking the following command in the terminal::

    > gsa_sobol_generate -n 20 -d 3

will produce 5 design matrix files with the following names::

    .
    |
    +--- 
    +--- srs_20_3_a.csv
    +--- srs_20_3_ab1.csv
    +--- srs_20_3_ab2.csv
    +--- srs_20_3_ab3.csv
    +--- srs_20_3_b.csv

Each file has the same structure as the design matrix file produced in :ref:`gsa_module_doe`.

Following the convention of Sobol'-Saltelli design, 2 design of experiments of the same size :math:`N \times k` are first generated.
These are the ones with ``matrix_ID`` ``a`` and ``b``.
Afterward each column of the matrix :math:`A` is replaced by a column from matrix :math:`B`.
For example, ``matrix_ID`` ``ab1`` corresponds to the matrix :math:`A` whose the first column has been replaced by the first column of matrix :math:`B`.

The model then has to be evaluated using the parameters values listed in each of these design matrix files.