.. gsa_module_implementation_sobol:

--------------------------
Sobol' Sensitivity Indices
--------------------------

Variance-based methods for global sensitivity analysis use variance as the basis to define a measure of input parameter influence on the overall output variation [1]_.
In a statistical framework of sensitivity and uncertainty analysis,
this choice is natural because variance (or standard deviation, a related concept) is often used as a measure of dispersion or variability in the model prediction [2]_.
A measure of such dispersion, in turn, indicates the precision of the prediction due to variations in the input parameters.

This section of the documentation discusses the origin of Sobol' sensitivity indices and the method to estimate them by Monte Carlo simulation.

High-Dimensional Model Representation
-------------------------------------

Consider once more a mathematical model :math:`f: \mathbf{x} \in [0,1]^D \mapsto y = f(\mathbf{x}) \in \mathbb{R}`.
The high-dimensional model representation (HDMR) of :math:`f(\mathbf{x})` is a linear combination of functions with increasing dimensionality [3]_,

.. math::
    f(\mathbf{x}) = f_o + \sum_{d=1,2,...D} f_d(x_d) + \sum_{1\leq d < e \leq D} f_{d,e} (x_d, x_e) + \cdots + f_{1,2,\cdots,D} (x_1, x_2, \cdots, x_D)
    :label: hdmr

where :math:`f_o` is a constant.

The representation in the above equation is unique given the following condition [4]_:

.. math::
    & \int_{0}^{1} f_{i1, i2, \cdots is}(x_{i1}, x_{i2}, \cdots, x_{is}) d_{x_{im}} = 0 \\
    & \quad \text{for}\quad m = 1,2,\cdots,s;\quad 1\leq i_1 < i_2 < \cdots < i_s \leq D; \\
    & \text{and} \quad s \in {1,\cdots,D}
    :label: unicity

Assume now that :math:`\mathbf{X}` is a random vector of independent and uniform random variables over a unit hypercube
:math:`\{\Omega = \mathbf{x} | 0 \leq x_i  \leq 1; i = 1,\cdots D\}` such that

.. math::

    Y = f(\mathbf{X})

where :math:`Y` is a random variable, resulting from the transformation of random vector :math:`\mathbf{X}` by function :math:`f`.
Using Eq. :eq:`unicity` to express each term in Eq. :eq:`hdmr`, it follows that

.. math::
    f_o & = \mathbb{E}[Y] \\
    f_d(x_d) & = \mathbb{E}_{\sim d}[Y|X_d] - \mathbb{E}[Y] \\
    f_{d,e}(x_d,x_e) & = \mathbb{E}_{\sim d,e} [Y|X_d, X_e] - \mathbb{E}_{\sim d}[Y|X_d] - \mathbb{E}_{\sim e}[Y|X_e] - \mathbb{E}[Y]
    :label: conditional_expectation

The same follows for higher-order terms in the decomposition.
In Eq. :eq:`conditional_expectation`, :math:`\mathbb{E}_{\sim e} [Y|X_e]` corresponds to the conditional expectation operator,
and the :math:`\sim\circ` in the subscript means that the integration over the parameter space is carried out over all parameters except the specified parameter in the subscript.
For instance, :math:`\mathbb{E}_{\sim 1} [Y|X_1]` refers to the conditional mean of :math:`Y` given :math:`X_1`,
and the integration is carried out for all possible values of parameters in :math:`\mathbf{x}` except :math:`x_1`.
Note that because :math:`X_1` is a random variable, the expectation conditioned on it is also a random variable.

Assuming that :math:`f` is a square integrable function, applying the variance operator on :math:`Y` results in

.. math::
    \mathbb{V}[Y] = \sum_{d=1}^{D} \mathbb{V}[f_d (x_D)] + \sum_{1 \leq d < e \leq D} \mathbb{V} [f_{d,e} (x_d, x_e)] + \cdots + \mathbb{V} [f_{1,2,\cdots,D} (x_1, x_2, \cdots, x_D)]
    :label: variance_decomposition

Sobol' Sensitivity Indices
--------------------------

Division by :math:`\mathbb{V}[Y]` aptly normalizes Eq. :eq:`variance_decomposition`

.. math::
  1 = \sum_{d = 1}^{D} S_d + \sum_{1 \leq d < e \leq D} S_{d,e} + \cdots + S_{1,2,\cdots,D}

The Sobol' main-effect sensitivity index :math:`S_d` is defined as,

.. math::
    S_d = \frac{\mathbb{V}_d [\mathbb{E}_{\sim d} [Y|X_d]]}{\mathbb{V}[Y]}
    :label: main_effect_index

The numerator is the variance of the conditional expectation,
and the index is a global sensitivity measure interpreted as the amount of variance reduction in the model output if the parameter :math:`X_d` is fixed (i.e., its variance is reduced to zero).

A closely related sensitivity index proposed by Homma and Saltelli [5]_ is the Sobol' total-effect index defined as,

.. math::
    ST_{d} & = \frac{\mathbb{E}_{\sim d}[\mathbb{V}_{d}[Y|\mathbf{X}_{\sim d}]]}{\mathbb{V}[Y]}
    :label: total_effect_index

The index, also a global sensitivity measure, can be interpreted as the amount of variance left in the output if the values of all input parameters,
*except* :math:`x_d`, can be fixed.

These two sensitivity measures can be related to the objectives of global SA for model assessment as proposed by Saltelli et al. ([2]_ [6]_).
The main-effect index is relevant to parameter prioritization in the context of identifying the most influential parameter
since fixing a parameter with the highest index value would, *on average*, lead to
the greatest reduction in the output variation.

The total-effect index, on the other hand,
is relevant to parameter fixing (or screening) in the context of identifying the least influential set of parameters since fixing any parameter that has a very small
total-effect index value would not lead to significant reduction in the output variation.
The use of total-effect index to identify which parameter can be fixed or excluded is similar to that of the elementary effect statistics of the Morris method,
albeit more exact but also more computationally expensive to compute.
And finally, the difference between the two indices of a given parameter (Eqs. :eq:`total_effect_index` and :eq:`main_effect_index`)
is used to quantify the amount of all interactions involving that parameters in the model output.

The Sobol'-Saltelli Method
--------------------------

Monte Carlo Integration
```````````````````````

In principle,
the estimation of the Sobol' indices defined by Eqs. :eq:`main_effect_index` and :eq:`total_effect_index` can be directly carried out using Monte Carlo (MC) simulation.
The most straightforward, though rather naive,
implementation of MC simulation to conduct the estimation is using two nested loops for the computation of the conditional variance and expectation appeared in both equations.

In the estimation of the main-effect index of parameter :math:`x_d`, for instance,
the outer loop samples values of :math:`X_d` while the inner loop samples values of :math:`\mathbf{X}_{\sim d}`
(anything else other than :math:`x_d`).
These samples, in turn, are used to evaluate the model output.
In the inner loop, the mean of the model output (for a given value of :math:`X_d` but over many values of :math:`\mathbf{X}_{\sim d}`) is taken.
Afterward, in the outer loop, the variance of the model output (over many values of :math:`X_d`) is taken.
This approach can easily become prohibitively expensive as the nested structure requires two :math:`N^2` model evaluations *per input dimension* for either the main-effect and total-effect indices,
while :math:`N` (the size of MC samples) are typically in the range of :math:`10^2 - 10^4` for a reliable estimate.

Sobol' [4]_ and Saltelli [7]_ proposed an alternative approach that circumvent the nested structure of MC simulation to estimate the indices.
The formulation starts by expressing the expectation and variance operators in their integral form.
As the following formulation is defined on a unit hypercube of :math:`D`-dimension parameter space where each parameter is a uniform and independent random variable,
explicit writing of the distribution within the integration as well as the integration range are excluded for conciseness.

First, the variance operator shown in the numerator of Eq. :eq:`main_effect_index` is written as

.. math::
    \mathbb{V}_{d}[\mathbb{E}_{\sim d}[Y|X_d]] & = \mathbb{E}_{d}[\mathbb{E}_{\sim d}^{2}[Y|X_d]] - \left(\mathbb{E}_{d}[\mathbb{E}_{\sim d}[Y|X_d]]\right)^2 \\
                                               & = \int \mathbb{E}_{\sim d}^{2}[Y|X_d] dx_d - \left(\int \mathbb{E}_{\sim d}[Y|X_d] dx_d\right)^2
    :label: ss_variance_integral

The notation :math:`\mathbb{E}_{\sim \circ}[\circ | \circ]` was already explained in the previous subsection,
while :math:`\mathbb{E}_{\circ} [\circ]` corresponds to the marginal expectation operator
where the integration is carried out over the range of parameters specified in the subscript.

Next, consider the term conditional expectation shown in Eq. :eq:`ss_variance_integral`, which per definition reads

.. math::
    \mathbb{E}_{\sim d} [Y|X_d] = \int f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}_{\sim d}
    :label: ss_expectation_integral

Note that :math:`\mathbf{x} = \{\mathbf{x}_{\sim d}, x_d\}`.

Following the first term of Eq. :eq:`ss_variance_integral, by squaring Eq. :eq:`ss_expectation_integral
and by defining a dummy vector variable :math:`\mathbf{x}^{\prime}_{\sim d}`,
the product of the two integrals can be written in terms of a single multiple integrals

.. math::
    \mathbb{E}_{\sim d}^{2} [Y|X_d] & = \int f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}_{\sim d} \cdot \int f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}_{\sim d} \\
                                    & = \int \int f(\mathbf{x}^{\prime}_{\sim d}, x_d) f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}^{\prime}_{\sim d} d\mathbf{x}_{\sim d}
    :label: ss_multiple_integrals


Returning to the full definition of variance of conditional expectation in Eq. :eq:`ss_variance_integral`,

.. math::
    \mathbb{V}_{d}[\mathbb{E}_{\sim d}[Y|X_d]] & = \int \int f(\mathbf{x}^{\prime}_{\sim d}, x_d) f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}^{\prime}_{\sim d} d\mathbf{x}_{\sim d} \\
                                               & \quad - \left(\int f(\mathbf{x}) d\mathbf{x}\right)^2
    :label: ss_variance_integral_single

Finally, the main-effect sensitivity index can be written as an integral as follows:

.. math::
    S_d & = \frac{\mathbb{V}_d [\mathbb{E}_{\sim d} [Y|X_d]]}{\mathbb{V}[Y]} \\
        & = \frac{\int \int f(\mathbf{x}^{\prime}_{\sim d}, x_d) f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}^{\prime}_{\sim d} d\mathbf{x} - \left(\int f(\mathbf{x}) d\mathbf{x}\right)^2}{\int f(\mathbf{x})^2 d\mathbf{x} - \left( \int f(\mathbf{x}) d\mathbf{x}\right)^2}
    :label: ss_main_effect_integral

The integral form given above dispenses with the nested structure of multiple integrals in the original definition of main-effect index.
The multidimensional integration is over :math:`2 \times D - 1` dimensions
and it is the basis of estimating sensitivity index using MC simulation in this implementation,
hereinafter referred to as the Sobol'-Saltelli method.
The same procedure applies to derive the total effect-index which yields,

.. math::
    ST_d & = \frac{\mathbb{E}_{\sim d}[\mathbb{V}_{d}[Y|\mathbf{X}_{\sim d}]]}{\mathbb{V}[Y]} \\
         & = \frac{\int f^2(\mathbf{x}) d\mathbf{x} - \int \int f(\mathbf{x}_{\sim d}, x^{\prime}_d) f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}^{\prime}_{d} d\mathbf{x}}{\int f(\mathbf{x})^2 d\mathbf{x} - \left( \int f(\mathbf{x}) d\mathbf{x}\right)^2}
    :label: ss_total_effect_integral

For :math:`N` number of MC samples and :math:`D` number of model parameters,
MC simulation procedure to estimate the sensitivity indices follows the sampling and resampling approach adopted in [4]_, [5]_, [7]_ described in the following.

Procedures
``````````

**First**, generate two :math:`N \times D` independent random samples from a uniform independent distribution in :math:`D`-dimension, :math:`[0,1]^D`:

.. math::
    A =
    \begin{pmatrix}
    a_{11}  & \cdots  & a_{1D}\\
    \vdots	& \ddots & \vdots\\
    a_{N1}  & \cdots  & a_{ND}\\
    \end{pmatrix}
    ;\quad B =
    \begin{pmatrix}
        b_{11}  & \cdots  & b_{1D}\\
        \vdots	& \ddots & \vdots\\
        b_{N1}  & \cdots  & b_{ND}\\
    \end{pmatrix}
    :label: ss_two_samples

**Second**, construct :math:`D` additional design of experiment matrices
where each matrix is matrix :math:`A` with the :math:`d`-th column substituted by the :math:`d`-th column of matrix :math:`B:

.. math::
  & A_{B}^1 =
  \begin{pmatrix}
    b_{11}  & \cdots  & a_{1D}\\
    \vdots	& \ddots & \vdots\\
    b_{N1}  & \cdots  & a_{ND}\\
  \end{pmatrix} \\
  & A_{B}^{d} =
  \begin{pmatrix}
    a_{11}  & \cdots & b_{1d} & \cdots & a_{1D}\\
    \vdots	& \cdots & \vdots & \cdots & \vdots\\
    a_{N1}  & \cdots & b_{Nd} & \cdots & a_{ND}\\
  \end{pmatrix} \\
  & A_{B}^{D} =
  \begin{pmatrix}
    a_{11}  & \cdots  & b_{1D}\\
    \vdots	& \ddots & \vdots\\
    a_{N1}  & \cdots  & b_{ND}\\
  \end{pmatrix}

**Third**, rescale each element in the matrices of samples to the actual values of model parameters according to their actual range of variation through iso-probabilistic transformation.

**Fourth**, evaluate the model multiple times using input vectors that correspond to each row of :math:`A`, :math:`B`, and all the :math:`A_B^d`.

**Fifth** and finally, extract the quantities of interest (QoIs) from all the outputs and recast them as vectors.
The main-effect and total-effect indices are then estimated using the estimators described below.

Monte Carlo Estimators
``````````````````````

For the main-effect sensitivity index, two estimators are considered.
One is proposed by Saltelli [7]_, and the other, as an alternative, is proposed by Janon et al. [8]_.
The latter proved to be more efficient, especially for a large variation around a parameter estimate [8]_.


The first term in the numerator of Eq. :eq:`ss_main_effect_integral` is the same for both estimators and is given by

.. math::
  \int \int f(\mathbf{x}^{\prime}_{\sim d}, x_d) f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}^{\prime}_{\sim d} d\mathbf{x}_{\sim d} \approx \frac{1}{N}\sum_{n=1}^N f(B)_n \cdot f(A_B^d)_n
  :label: ss_first_term

where the subscript :math:`n` corresponds to the row of the sampled model parameters
such that :math:`f(B)_n` is the model output evaluated using inputs taken from the :math:`n`-th row of matrix :math:`B`
and :math:`f(A_B^d)_n` is the model output evaluated using inputs taken from the :math:`n`-th row of matrix :math:`A_B^K`.
The MC estimator for the second term in the numerator and for the denominator differ for the two considered estimators given in Table below.

================= ===================================================================== ===================================================================================================================================
Estimator         :math:`\mathbb{E}^2[Y] = \left( \int f d\mathbf{x}\right)^2`          :math:`\mathbb{V}[Y] = \int f^2 d\mathbf{x} - \left( \int f d\mathbf{x}\right)^2`
================= ===================================================================== ===================================================================================================================================
Saltelli [7]_     :math:`\frac{1}{N} \sum f(A)_n \cdot f(B)_n`                          :math:`\frac{1}{N}\sum f(A)_n^2-\left(\frac{1}{N}\sum f(A)_n\right)^2`
Janon et al. [8]_ :math:`\left(\frac{1}{N} \sum \frac{f(B)_n + f(A_B^d)_n}{2}\right)^2` :math:`\frac{1}{N} \sum \frac{f(B)_n^2 + f(A_B^d)_n^2}{2}\quad - \left(\frac{1}{N} \sum \frac{f(B)_n^2 + f(A_B^d)_n^2}{2}\right)^2`
================= ===================================================================== ===================================================================================================================================

The general formula of the main-effect sensitivity index estimator is

.. math::
  \widehat{S}_d = \frac{\frac{1}{N}\sum_{n=1}^N f(B)_n \cdot f(A_B^d)_n - \mathbb{E}^2[Y]}{\mathbb{V}[Y]}
  :label:  ss_main_effect_estimator
where and :math:`\mathbb{E}^2[Y]` and :math:`\mathbb{V}[Y]` are as prescribed in the table above.

The general formula of the total-effect sensitivity indices follows the definition of it as given in :eq:`total_effect_index`.
The denominator :math:`\mathbb{E}_{\sim d}[\mathbb{V}_{d}[Y|\mathbf{X}_{\sim d}]]` is estimated using the estimators listed in the table below,
while :math:`\mathbb{V}[Y]` is estimated by the Saltelli et al. estimator in table above.

================= ==================================================================
Estimator         :math:`\mathbb{E}_{\sim d}[\mathbb{V}_{d}[Y|\mathbf{X}_{\sim d}]]`
================= ==================================================================
Sobol-Homma [5]_  :math:`\frac{1}{N} \sum f^2(A)_n \cdot f(A)_n f(AB^d)_n`
Jansen [10]_      :math:`\frac{1}{2N} \sum \left(f(A)_n - f(AB^d)_n\right)^2`
================= ==================================================================

The computational cost associated with the estimation of all the main-effect and total-effect indices is :math:`N \times (D + 2)` code runs,
where :math:`N` is the number of MC samples and :math:`D` is the number of parameters.
Compare this to the cost of brute force Monte Carlo of :math:`2 \times D \times N^2` code runs to estimate all the main-effect and total-effect sensitivity indices.

As an additional comparison, the cost for Morris method to compute the statistics of elementary effect is :math:`N_R \times (D + 1)` code runs,
where :math`N_R` is the number of OAT design replications.
In either methods, the number of samples :math`N` (in the case of the Sobol'-Saltelli method) and replications :math:`N_R` (in the case of the Morris method)
determines the precision of the estimates.
A larger number of samples (and replications) increases the precision.
Note, however, that in practice the typical number of Morris replications is between :math:`10^1 - 10^2` [10]_,
while the number of \gls{mc} samples for the Sobol' indices estimation amounts to :math:`10^2 - 10^4` [4]_.

References
----------

.. [1] Dan G. Cacuci and Mihaela Ionescu-Bujor,
       "A Comparative Review of Sensitivity and Uncertainty Analysis of Large-Scale Systems - II: Statistical Methods,"
       Nuclear Science and Engineering, vol. 147, no. 3, pp. 204-217, 2004.
.. [2] A. Saltelli et al.,
       "Global Sensitivity Analysis. The Primer,"
       West Sussex, John Wiley & Sons, 2008.
.. [3] Genyuan Li, Carey Rosenthal, and Herschel Rabitz,
       "High Dimensional Model Representations,"
       The Journal of Physical Chemistry A, vol. 105, no. 33, pp. 7765-7777, 2001.
.. [4] I. M. Sobol, "Global Sensitivity Analysis for nonlinear mathematical models and their Monte Carlo estimates,"
       Mathematics and Computers in Simulation, vol. 55, no. 1-3, pp. 271-280, 2001.
.. [5] Toshimitsu Homma and Andrea Saltelli,
       "Importance Measures in Global Sensitivity Analysis of Nonlinear Models,"
       Reliability Engineering and System Safety, vol. 52, no. 1, pp. 1-17, 1996.
.. [6] A. Saltelli et al.,
       "Sensitivity Analysis in Practice: a Guide to Assessing Scientific Models,"
       West Sussex, John Wiley & Sons, 2004.
.. [7] A. Saltelli,
       "Making best use of model evaluations to compute sensitivity indices,"
       Computer Physics Communications, vol. 145, no. 2, pp. 280-297, 2002.
.. [8] A. Janon et al.,
       "Asymptotic normality and efficiency of two Sobol' index estimators,"
       ESAIM: Probability and Statistics, vol. 18, pp. 342-364, 2014.
.. [9] M. J. W. Jansen,
       "Analysis of variance designs for model output,"
       Computer Physics Communications, vol. 117, pp. 35-43, 1999.
.. [10] F. Campolongo, A. Saltelli, and J. Cariboni,
       “From Screening to Quantitative Sensitivity Analysis. A Unified Approach,”
       Computer Physic Communications, vol. 182, no. 4, pp. 978-988, 2011.