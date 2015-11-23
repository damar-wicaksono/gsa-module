# Global Sensitivity Analysis Package

Python3 package to carry out Variance-based GSA.

**GSA-Module** is a python3 implementation of several global methods for 
sensitivity analysis.
The implementation is based on a black-box approach where the function 
is implemented externally to the module.  
Function here is defined in a generic term; it can be another code that 
gives an output for a given set of inputs.

## Scope
 
The package contains several sub-package to carry out this task:
1. `sample`: the package responsible to generate pseudorandom and/or
  low-discrepancy sequences
2. `qoi`: the package responsible to extract the quantity of interest 
  from a set of csv files
3. `sobol`: the package responsible to generate set of sobol-saltelli 
  sampling-resampling design matrices, read the set of csv output files,
  and calculate the 1st-order, 2nd-order, and total-order indices
4. `morris`: the package used to generate Morris trajectories matrix, read 
  the set of csv output files, and calculate the elementary effects and their
  statistics
5. `pearson`: the package to calculate the Person correlation from a set of csv 
  output files.
 
All of these packages as well as modules and functions within them are stiched
together with the use of *driver* script. 
A *driver* script is custom made and tailored for a certain analysis. 
The generic use of such script is exemplified as follow:
 
1. Generate design matrix, either for a specific application such as the 
  Sobol'-Saltelli and Morris, or for general purpose such as simple random
  sampling, latin hypercube, etc.
2. Use the design matrix to evaluate a function that produced an output in 
  a set of csv files. This function can simply be an external code as long 
  as the produced files are csv.
3. If the output is not directly a scalar, then the functions within the 
  `qoi` package can be used to post-process them further
4. From a set of csv files containing scalar output, the sensitivity measures
  can be computed (e.g., Sobol' indices, statistics of elementary effects, etc.)
 
 ## `sample` package
 
 ## `qoi` package
 
 ## `sobol` package
 
 ## `morris` package
 
 ## `pearson` package