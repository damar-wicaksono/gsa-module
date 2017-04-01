# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/)

## Unreleased

### Fixed
- Fixed the issue with stability of linear solution when standardization 
  is used

## [0.7.1] - 2017-03-20

### Changed
- Default values for the built-in `dirnumfiles` = `new-joe-kuo-6.21201` is 
  asserted when the built-in Sobol' sequence generator is called 

### Fixed
- Fix the risk to have zero-valued rows in the perturbation matrix for 
  radial design used in the Morris method
- Fix the interface to generate Morris radial design calling the internally 
  implemented Sobol' sequence generator

## [0.7.0] - 2017-03-06

### Added
- Natively implement [Joe & Kuo] Sobol' sequence generator in Python. Pure 
  conversion from the C++ source code to Python.
  
### Deprecated
- The compiled C++ source code of `sobol.cc` is deprecated. Any reference 
  to call the wrapper to execute this executable in order to generate Sobol'
  sequence will be removed in the subsequent releases.

## [0.6.0] - 2017-03-06

### Added
- Capability to generate design of computer experiments for screening analysis
  (one-at-a-time, OAT, design) based on the trajectory desing (original Morris)
  and radial design (Saltelli et al.)
- Capability to compute the statistics of elementary effects, standardized or 
  otherwise, bot for trajectory and radial designs. The statistics (mean, mean 
  of absolute, and standard deviation) are used as the basis of parameter 
  importance ranking
- Update the module `sphinx-doc` documentation for the Morris method

## [0.5.3] - 2016-09-09

### Fixed
- Wrong implementation of random shifting the Sobol' sequence

## [0.5.2] - 2016-09-07

### Fixed
- Issue with trying to optimized LHS of dimension 1

## [0.5.1] - 2016-09-06

### Fixed
- Wrong implementation of random shifting the Sobol' quasi-random sequence

## [0.5.0] - 2016-09-06

### Added
- Generation of separate test points based on a given design using Hammersley
  quasi-random sequence

## [0.4.0] - 2016-09-06

### Added
- Randomization of the Sobol' quasi-random sequence using random shift 
  procedure

## [0.3.0] - 2016-08-31

### Added
- Optimization of the latin hypercube design is done via evolutionary 
  stochastic algorithm (ESE)
  
## [0.2.0] - 2016-08-30

### Added
- Sobol' quasi-random sequence generator is a wrapper around the implementation
  by [Joe & Kuo] (2008). Two binaries are made available for linux64 and 
  windows64
  
## 0.1.0 - 2016-11-23

### Added
- Capability to generate design of experiments using 4 different methods:
  simple random sampling (SRS) and latin hypercube sampling (LHS) using command
  line interace

[Unreleased]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/develop%0Dv0.7.0
[0.7.1]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/v0.7.1%0Dv0.7.0
[0.7.0]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/v0.7.0%0Dv0.6.0
[0.6.0]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/v0.6.0%0Dv0.5.3
[0.5.3]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/v0.5.3%0Dv0.5.2
[0.5.2]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/v0.5.2%0Dv0.5.1
[0.5.1]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/v0.5.1%0Dv0.5.0
[0.5.0]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/v0.5.0%0Dv0.4.0
[0.4.0]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/v0.4.0%0Dv0.3.0
[0.3.0]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/v0.3.0%0Dv0.2.0
[0.2.0]: https://bitbucket.org/lrs-uq/gsa-module/branches/compare/v0.2.0%0Dv0.1.0

[Joe & Kuo]: http://web.maths.unsw.edu.au/~fkuo/sobol/
