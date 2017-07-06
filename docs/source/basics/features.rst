.. gsa_module_features:

List of Features
----------------

The following is the main features of the current release (v0.9.0):

 - Capability to generate design of computer experiments using 4 different methods: simple random sampling (srs), latin hypercube sampling (lhs), sobol' sequence, and optimized latin hypercube using either command line interface gsa_create_sample or the module API via import gsa_module
 - Sobol' quasi-random number sequence generator is natively implemented in Python3 based on C++ implementation of Joe and Kuo (2008).
 - Randomization of the Sobol' quasi-random number using random shift procedure
 - Optimization of the latin hypercube design is done via evolutionary stochastic algorithm (ESE)
 - Generation of separate test points based on a given design using Hammersley quasi-random sequence
 - Capability to generate design of computer experiments for screening analysis (One-at-a-time design), based on the trajectory design (original Morris) and radial design (Saltelli et al.)
 - Capability to compute the statistics of elementary effects, standardized or otherwise both for trajectory and radial designs. The statistics (mean, mean of absolute, and standard deviation) are used as the basis of parameter importance ranking.
 - Capability to estimate the first-order (main effect) Sobol' sensitivity indices using two different estimators (Saltelli and Janon).
 - Capability to estimate the total effect Sobol' sensitivity indices using two different estimators (Sobol-Homma and Jansen).
 - All estimated quantities are equipped with their bootstrap samples
 