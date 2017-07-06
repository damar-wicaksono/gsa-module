.. _gsa_module_implementation_gsa:

--------------------------------------
Sensitivity Analysis: Local vs. Global
--------------------------------------

An essential part of model development and assessment is properly describing and understanding the impact of model parameter variations on the model prediction.
Sensitivity analysis (SA) is an important methodological step in that context [1]_.
SA is the process of investigating the role of input parameters in determining the model output [2]_. 
It seeks to quantify the importance of each model input parameter on the output.

Various classifications exist in the literature to categorize SA techniques [3]_ [4]_ [5]_ [6]_ [2]_.
In the review by Ionescu-Bujor and Cacuci [4]_ [5]_, 
SA techniques are classified with respect to their scope (local vs. global) and to their framework (deterministic vs. statistical).
In the review of SA methods by Iooss and Lemaître [2]_, 
and the work by Saltelli et al. [6]_ and by Santner et al. [7]_, 
the statistical framework is implicitly assumed deriving ideas from design of experiment, 
and the classification is based on the parameter space of interest (local vs. global).

Local analysis is based on calculating the effect on the model output of small perturbations around a nominal parameter value. 
Often the perturbation is done one parameter at a time thus approximating the first-order partial derivative of the model output with respect to the perturbed parameter. 
The derivative can be computed through efficient adjoint formulation [8]_ [9]_ capable of handling large number of parameters.

Besides being numerically efficient, 
sensitivity coefficients obtained from local deterministic sensitivity analysis have the advantage of being intuitive in their interpretation, 
irrespective of the method employed [10]_. 
The intuitiveness stems from the aforementioned equivalence to the derivative of the output with respect to each parameter [4]_ around a specifically defined point (i.e., nominal parameter values). 
Thus the coefficients can be readily compared over different modeled systems, independently of the range of parameters variations.

The global analysis, on the other hand, 
seeks to explore the input parameters space across its range of variation and then quantify the input parameter importance based on a characterization of the resulting output response surface. 
In global deterministic framework [4]_[9]_, 
the characterization is aimed at the identification of the system’s critical points (e.g., maxima, minima, saddle points, etc.). 
In statistical global methods [6]_ [11]_, 
the characterization is aimed at measuring the dispersion of the output based on variance [12]_ [13]_, 
correlation [14]_, or elementary effects [15]_.

Due to the different characterizations, 
the global statistical framework can potentially give spurious results not comparable to the results from local method 
as there is no unique definition of sensitivity coefficient provided by different global methods [10]_.
In some cases, different methods can give different and inconsistent parameters importance ranking [6]_ [8]_. 
Furthermore, the result of the analysis can be highly dependent to the assumed input parameters probability distribution and/or their range of variation [5]_ [9]_.

Yet, despite the aforementioned shortcomings, 
the global statistical framework has three particular attractive features relevant to the present study. 
First, the statistical method for sensitivity analysis is non-intrusive in the sense that minimal or no modification to the original code is required. 
In other words, the code can be taken as a black box and the analysis is focused on the input/output relationship [6]_ of the code. 
This is the case especially in comparison to adjoint-based sensitivity [16]_ [17]_ which is a highly efficient and accurate method applicable to a large number of parameters, 
provided that the code is designed/modified for adjoint analysis.

Second, no a priori knowledge on the model structure (linearity, additivity, etc.) is required. 
Depending on the model complexity and as the parameter variation range can be large, 
the linearity or additivity assumption might not hold.

Third and finally, 
the choice of a statistical framework for sensitivity analysis fits the Monte Carlo (MC)-based uncertainty propagation method widely adopted in nuclear reactor evaluation models \cite{Boyack1990, Nutt2004, Wallis2007, Glaeser2008}. 
The method prescribes that the uncertain model input and parameters (modeled as random variables) 
should be simultaneously and randomly perturbed across their range of variations. 
Multiple randomly generated input values are then propagated through the code to quantify the dispersion of the prediction (e.g., peak cladding temperature) 
which serves as a measure of the prediction reliability. 
Statistical global sensitivity analysis thus complements the propagation step 
by addressing the follow-up question on the identification of the most important parameters in driving the prediction uncertainty. 

References
----------

.. [1] T.G. Trucano, L.P. Swiler, T. Igusa, W.L. Oberkampf, and M. Pilch,
       "Calibration, validation, and sensitivity analysis: What's what,"
       Reliability Engineering and System Safety, vol. 91, no. 10-11, pp. 1331-1357, 2006.
.. [2] B. Iooss and P. Lemaitre,
       "A review on global sensitivity analysis methods,"
       in Uncertainty Management in Simulation-Optimization of Complex Systems, pp. 101-122, Springer, 2015.
.. [3] H.C. Frey and S.R. Patil,
       "Identification and Review of Sensitivity Analysis Methods,"
       Risk Analysis, vol. 22, no. 3, pp. 553--578, 2002.
.. [4] M. Ionescu-Bujor and D.G. Cacuci,
       "A Comparative Review of Sensitivity and Uncertainty Analysis of Large-Scale Systems - I: Deterministic Methods,"
       Nuclear Science and Engineering, vol. 147, pp. 189-203, 2004.
.. [5] D.G. Cacuci and M. Ionescu-Bujor,
       "A Comparative Review of Sensitivity and Uncertainty Analysis of Large-Scale Systems - II: Statistical Methods,"
       Nuclear Science and Engineering, vol. 147, pp. 204-217, 2004.
.. [6] A. Saltelli et al.,
       "Global Sensitivity Analysis. The Primer,"
       West Sussex, John Wiley & Sons, 2008.
.. [7] T.J. Santner, B.J. Williams, and W.I. Notz,
       "The Design and Analysis of Computer Experiments,"
       Springer, 2003.
.. [8] D.G. Cacuci,
       "Sensitivity and Uncertainty Analysis, Volume I: Theory,"
       Chapman & Hall/CRC, 2003.
.. [9] D.G. Cacuci and M. Ionescu-Bujor,
       "Sensitivity and Uncertainty Analysis, Data Assimilation, and Predictive Best-Estimate Model Calibration,"
       Handbook of Nuclear Engineering, Springer, pp. 1913-2051, 2010.
.. [10] S. Razavi and H.V. Gupta,
        "What do we mean by sensitivity analysis? The need for comprehensive characterization of “global” sensitivity in Earth and Environmental systems models," 
        Water Resources Research, vol. 51, pp. 3070-3092, 2015.
.. [11] A. Saltelli et al.,
        "Sensitivity Analysis in Practice: a Guide to Assessing Scientific Models,"
        West Sussex, John Wiley & Sons, 2004.
.. [12] I. M. Sobol, 
        "Global Sensitivity Analysis for nonlinear mathematical models and their Monte Carlo estimates,"
        Mathematics and Computers in Simulation, vol. 55, no. 1-3, pp. 271-280, 2001.
.. [13] R. Cukier, H. Levine, K. Shuler,
        "Nonlinear Sensitivity Analysis of Multiparameter Model Systems," 
        Journal of Computational Physics, vol. 26, pp. 1-42, 1978.
.. [14] J.C. Helton,
        "Uncertainty and sensitivity analysis techniques for use in performance assessment for radioactive waste disposal," 
        Reliability Engineering & System Safety, vol. 42, pp. 327-367, 1993.
.. [15] Max D. Morris, 
       "Factorial Sampling Plans for Preliminary Computational Experiments", Technometrics, Vol. 33, No. 2, pp. 161-174, 1991.
.. [16] D.G. Cacuci and M. Ionescu-Bujor,
        "Adjoint Sensitivity Analysis of the RELAP5/MOD3.2 Two-Fluid Thermal-Hydraulic Code System - I: Theory," 
        Nuclear Science and Engineering, vol. 136, pp. 59-84, 2000.
.. [17] M. Ionescu-Bujor and D.G. Cacuci,
        "Adjoint Sensitivity Analysis of the RELAP5/MOD3.2 Two-Fluid Thermal-Hydraulic Code System - II: Applications,"
        Nuclear Science and Engineering, vol. 136, pp. 85-121, 2000.
