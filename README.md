# Global Sensitivity Analysis - Sobol

Variance-based GSA using Sobol' method

**GSA-Sobol** is a python3 implementation of the Sobol'-Saltelli method to 
compute the Sobol' indices.
The implementation is based on a black-box approach where the function 
is implemented externally to the module.  
Function here is defined in a generic term; it can be another code the 
gives an output for a given input.
The module is responsible for the following task:

 1. Creating a design matrix of input parameters
 2. Carrying out the function evaluations based on the design matrix
 3. Post-process the results and obtain the Sobol' indices
 4. Save all the results in a format easy to manipulate later 