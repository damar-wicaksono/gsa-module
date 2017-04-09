.. gsa_module_morris_indices:

Morris Screening Method
-----------------------

Successful installation of ``gsa-module`` will give access to two
executables in the path useful to carry out Morris screening analysis
on model outputs:

 1. ``gsa_morris_generate``: executable to generate Morris (One-at-a-Time, OAT)
    design
 2. ``gsa_morris_analyze``: executable to compute the statistics of the
    elementary effects given model inputs/outputs as files

A more theoretical background of the method can be found in the implementation
section of this documentation.

Generating Morris Design (Sample)
`````````````````````````````````

The first step in conducting sensitivity analysis by Morris screening method
is to generate One-at-a-Time design.
The Morris design generator driver script can be invoked from the  terminal using the
following command::

    > gsa_morris_generate -r <number of blocks/replications> \
                          -d <number of input dimensions> \
                          -o <design matrix output filename> \
                          -sep <delimiter for the output file {csv, tsv, txt}, default = csv> \
                          -ss <sampling scheme {trajectory or radial}> \
                          -p <trajectory scheme only, number of levels> \
                          -s <trajectory scheme only, random seed number> \
                          -sobol <radial scheme only, the fullpath to Sobol' sequence generator executable> \
                          -dirnum <radial scheme only, the fullpath to Sobol' sequence generator direction numbers file>


Brief explanation on this parameter can be shown using the following command::

    > gsa_morris_generate --help

By default the naming convention of the output file (if not explicitly specified is)::

    <sampling scheme>_<number of replications>_<number of input dimensions>_<number of levels, trajectory only>.csv

In general, the larger the number of replications the more accurate the
sensitivity measures are.
On the other hand, a large number of levels (in trajectory design) increases
the granularity in the input parameter space exploration.
However, this only makes sense if there is large number of replications
otherwise there is big risk of using unbalance design
(bias in some part of input parameter space)

**Example**

As an example, consider the following command::

    > gsa_morris_generate -r 10 -d 4 -p 6

The above command will generate a ``csv`` file with the name of
``trajectory_10_4_6.csv`` containing `50` rows and `4` columns.
`50` rows are obtained from the :math:`replicates \times (inputs+1)` formula
and it corresponds to the number of model evaluations, while the number of columns
corresponds to the number of input dimensions.
In OAT design only one parameter is changed between perturbation and in the case
of trajectory scheme there is no base point per se as the perturbations are carried out
one parameter at a time from the last perturbed point.
In the example above the size of grid jump (:math:`\Delta = 2/3`) is locked to
the number of levels.

Another example with more explicit specification of arguments::

    > gsa_morris_generate -r 10 -d 6 -ss radial \
                          -o test_radial \
                          -sep txt \
                          -sobol ./path_to_sobol_gen/sobol_gen.x \
                          -dirnum ./path_to_sobol_gen/dirnum.txt

The above command will generate a space separated file ``test_radial.txt``
containing `70` rows and `6` columns.
The radial OAT design is generated using the specified Sobol' sequence generator.
In the radial design, multiple base points are generated for different replications.
The perturbation per parameter in each replication is relative to the base point.
Furthermore, number of level is not required to be specified as the size of grid
jump differs from parameter to parameter and from replication to replication.

Executing Model
```````````````

Following the design philosophy of ``gsa-module`` the model executions are
implemented outside the module itself. The most important thing to remember is that
the OAT design generated using ``gsa_morris_generate`` is normalized (between [0,1]).
If the actual model has a different scale of parameters or different
probability distribution, the proper transformation of the design point is to
be carried out prior to the model evaluation.
Note also that the results of the execution should be saved inside a text file
with rows corresponding to the results of each model execution.

In general, the number of model evaluations, both for trajectory and
radial scheme, are related to the number of replications (`r`) and
the number of input dimensions (`k`):

:math:`n_{runs} = r \times (k + 1)`

Analyzing the I/O of Morris Experimental Runs
`````````````````````````````````````````````

The last step in conducting the Morris screening analysis is to compute the
statistics of the elementary effects for each input.
The minimum requirements for this computation are the design file
and its corresponding model output.
If necessary, the rescaled design file can also be specified to compute
the standardized version of the elementary effects.
The driver script to analyze the inputs/outputs of Morris experimental run
can be invoked from the terminal using the following command::

    > gsa_morris_analyze -in <the normalized inputs file> \
                         -ir <the rescaled inputs file> \
                         -o <the model/function outputs file> \
                         -output <the results of the analysis output file> \
                         -mc <Verbose model error checking> \

Brief explanation on this parameter can be shown using the following command::

    > gsa_morris_analyze --help

By default, the naming convention of the results of the analysis output file is::

    <normalized inputs filename>-<model outputs file>.csv

The ``-mc`` flag is to verbosely give report on the model specification
consistency. This includes:

 1. Number of input dimensions in the design file
 2. Number of blocks/replications in the design file
 3. Total number of runs
 4. Type of design
 5. Number of levels and grid jump size (trajectory scheme only)
 6. Rescaled inputs if specified

This information (except number 6) is directly inferred from the content of
the normalized design file.

**Example**

As an example, consider that a 4-parameter model was evaluated according to
the OAT design in the file ``trajectory_10_4_10.csv``.
The output of the model was saved inside a file ``4paramsFunction.csv``.

To compute the statistics of the elementary effects of this I/O pair,
invoke the following command::

     > gsa_morris_analyze -in ./trajectory_10_4_10.csv -o ./4paramsFunction.csv -mc

The flag ``-mc`` will result in verbose reporting of the model specification::

    Number of Input Dimensions    = 4
    Number of Blocks/Replications = 10
    Total Number of Runs          = 50
    Type of Design                = trajectory
    Number of levels (trajectory) = 10 (Delta = 0.5556)
    Rescaled Inputs               = None

The results of the analysis is saved inside the file
``trajectory_10_4_10-4paramsFunction.csv`` with the following contents::

    # mu, mu_star, std_dev, std_mu, std_mu_star, std_std_dev
    9.738333e+01,9.738333e+01,3.452392e+01,0.000000e+00,0.000000e+00,0.000000e+00
    6.596656e+01,6.596656e+01,3.181203e+01,0.000000e+00,0.000000e+00,0.000000e+00
    3.814122e+01,3.814122e+01,2.275404e+01,0.000000e+00,0.000000e+00,0.000000e+00
    2.529044e+01,2.529044e+01,1.261223e+01,0.000000e+00,0.000000e+00,0.000000e+00

Each column corresponds to the appropriate sensitivity measure as indicated
above. Note that the standardized version of the elementary effects are
taken to be zero as the rescaled input file was not specified.
The parameter is ordered according to the design matrix file
(the first column is the first parameter, etc.)
