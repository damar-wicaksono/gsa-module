.. _gsa_module_doe:

------------------------------------
General Purpose Design of Experiment
------------------------------------

Successful installation of ``gsa-module`` will give access to two
executables in the path useful to create various designs for computer 
experiment. 
The command line utility ``gsa_create_sample`` can be invoked from the terminal 
to generate the design (or *design matrix file*) using the following command::

    > gsa_create_sample -n <number of samples/points> \
                        -d <number of dimensions/variables> \
                        -m <method of generation {srs, lhs, sobol, lhs-opt}> \
                        -s <random seed number> \
                        -o <design matrix output filename> \
                        -sep <delimiter for the design matrix file> \
                        -dirnumfile <direction number file, Sobol' only> \
                        -excl_nom <exclude nominal file, Sobol' only> \
                        -rand <randomize the Sobol' sequence, Sobol' only> \
                        -nopt <number of optimization iterations, Sobol' only>

Brief explanation of these parameters can be shown by invoking::

    > gsa_create_sample --help

The table below lists the complete options/flag in detail with their respective default values.

=== =========== ==================== ======= ======== ======================================================== =========
No. Short Name  Long Name            Type    Required Description                                              Default
=== =========== ==================== ======= ======== ======================================================== =========
1   -h           --help              flag       No    Show help message                                        False
2   -n           --num_samples       integer    Yes   The number of samples/design points                      None
3   -d           --num_dimensions    integer    Yes   The number of dimensions                                 None
4   -m           --method            string     No    The method to generate sample {srs, lhs, sobol, lhs-opt} srs
5   -s           --seed_number       integer    No    The random seed number                                   None
6   -o           --output_file       string     No    The output filename                                      see below
7   -sep         --delimiter         string     No    The delimiter for the file {csv, tsv, txt}               csv
8   -dirnumfile  --direction_numbers string     No    The path to Sobol' sequence generator                    None
9   -excl_nom    --exclude_nominal   flag       No    Exclude the nominal point {0.5} in the design            False
10  -rand        --randomize_sobol   flag       No    Random shift the Sobol' sequence                         False
11  -nopt        --num_iterations    integer    No    The maximum bumber of optimization iterations            100
12  -V           --version           flag       No    Show the program's version number and exit               False
=== =========== ==================== ======= ======== ======================================================== =========

Note that options number 8-9 are valid only for Sobol' design, while option number 11 is valid only for Optimized LHS.
Without specifying the output filename explicitly, the design matrix file will be produced with the following naming convention::

    > <method>_<num_samples>_<num_dimensions>.csv

Example
-------

For example, upon executing the following command in the terminal::

    > gsa_create_sample -n 20 -d 5 -m sobol

a csv file with filename ``sobol_20_5.csv`` is produced in the current working directory.
The first 5 lines (out of 20) the file are as follow::

    0.000000e+00,0.000000e+00,0.000000e+00,0.000000e+00,0.000000e+00
    5.000000e-01,5.000000e-01,5.000000e-01,5.000000e-01,5.000000e-01
    7.500000e-01,2.500000e-01,2.500000e-01,2.500000e-01,7.500000e-01
    2.500000e-01,7.500000e-01,7.500000e-01,7.500000e-01,2.500000e-01
    3.750000e-01,3.750000e-01,6.250000e-01,8.750000e-01,3.750000e-01

In each line, the listed values correspond to the input parameters at which the model is to be evaluated.
The values are normalized between 0 to 1.
