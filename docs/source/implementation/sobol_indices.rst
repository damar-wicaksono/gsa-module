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
    f_d(x_d) & = \mathbb{E}_{\sim d}[Y|X_d] \\
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

In principle, the estimation of the Sobol' indices defined by Eqs.~(\ref{eq:sa_main_effect_index}) and (\ref{eq:sa_total_effect_index}) can be directly carried out using \gls{mc} simulation.
\marginpar{brute force \\ Monte Carlo}
The most straightforward, though rather naive,
implementation of \gls{mc} simulation to conduct the estimation is using two nested loops for the computation of the conditional variance and expectation appeared in both equations.

In the estimation of the main-effect index of parameter $x_d$, for instance,
the outer loop samples values of $X_d$ while the inner loop samples values of $\mathbf{X}_{\sim d}$ (anything else other than $x_d$).
These samples, in turn, are used to evaluate the model output.
In the inner loop, the mean of the model output (for a given value of $X_d$ but over many values of $\mathbf{X}_{\sim d}$) is taken.
Afterward, in the outer loop, the variance of the model output (over many values of $X_d$) is taken.
This approach can easily become prohibitively expensive as the nested structure requires two $N^2$ model evaluations \emph{per input dimension} for either the main-effect and total-effect indices,
while $N$ (the size of \gls{mc} samples) are typically in the range of $10^2 - 10^4$ for a reliable estimate.

Sobol' \cite{Sobol2001} and Saltelli \cite{Saltelli2002} proposed an alternative approach that circumvent the nested structure of \gls{mc} simulation to estimate the indices.
The formulation starts by expressing the the expectation and variance operators in their integral form.
As the following formulation is defined on a unit hypercube of $D$-dimension parameter space where each parameter is a uniform and independent random variable,
explicit writing of the distribution within the integration as well as the integration range are excluded for conciseness.

First, the variance operator shown in the numerator of Eq.~(\ref{eq:sa_main_effect_index}) is written as
\begin{equation}
  \begin{split}
    \mathbb{V}_{d}[\mathbb{E}_{\sim d}[Y|X_d]] & = \mathbb{E}_{d}[\mathbb{E}_{\sim d}^{2}[Y|X_d]] - \left(\mathbb{E}_{d}[\mathbb{E}_{\sim d}[Y|X_d]]\right)^2 \\
                                               & = \int \mathbb{E}_{\sim d}^{2}[Y|X_d] dx_d - \left(\int \mathbb{E}_{\sim d}[Y|X_d] dx_d\right)^2
  \end{split}
\label{eq:ss_variance_integral}
\end{equation}
The notation $\mathbb{E}_{\sim \circ}[\circ | \circ]$ was already explained in Section~\ref{sub:sa_hdmr},
while $\mathbb{E}_{\circ} [\circ]$ corresponds to the marginal expectation operator
where the integration is carried out over the range of parameters specified in the subscript.

Next, consider the term conditional expectation shown in Eq.~(\ref{eq:ss_variance_integral}), which per definition reads
\begin{equation}
  \mathbb{E}_{\sim d} [Y|X_d] = \int f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}_{\sim d}
\label{eq:ss_expectation_integral}
\end{equation}
Note that $\mathbf{x} = \{\mathbf{x}_{\sim d}, x_d\}$.

Following the first term of Eq.~(\ref{eq:ss_variance_integral}), by squaring Eq.~(\ref{eq:ss_expectation_integral})
and by defining a dummy vector variable $\mathbf{x}^{\prime}_{\sim d}$,
the product of the two integrals can be written in terms of a single multiple integrals
\begin{equation}
  \begin{split}
    \mathbb{E}_{\sim d}^{2} [Y|X_d] & = \int f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}_{\sim d} \cdot \int f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}_{\sim d} \\
                                    & = \int \int f(\mathbf{x}^{\prime}_{\sim d}, x_d) f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}^{\prime}_{\sim d} d\mathbf{x}_{\sim d}
  \end{split}
\label{eq:ss_multiple_integrals}
\end{equation}

Returning to the full definition of variance of conditional expectation in Eq.~(\ref{eq:ss_variance_integral}),
\begin{equation}
  \begin{split}
    \mathbb{V}_{d}[\mathbb{E}_{\sim d}[Y|X_d]] & = \int \int f(\mathbf{x}^{\prime}_{\sim d}, x_d) f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}^{\prime}_{\sim d} d\mathbf{x}_{\sim d} \\
                                               & \quad - \left(\int f(\mathbf{x}) d\mathbf{x}\right)^2
  \end{split}
\label{eq:ss_variance_integral_single}
\end{equation}

Finally, the main-effect sensitivity index can be written as an integral as follows:
\begin{equation}
  \begin{split}
    S_d & = \frac{\mathbb{V}_d [\mathbb{E}_{\sim d} [Y|X_d]]}{\mathbb{V}[Y]} \\
        & = \frac{\int \int f(\mathbf{x}^{\prime}_{\sim d}, x_d) f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}^{\prime}_{\sim d} d\mathbf{x} - \left(\int f(\mathbf{x}) d\mathbf{x}\right)^2}{\int f(\mathbf{x})^2 d\mathbf{x} - \left( \int f(\mathbf{x}) d\mathbf{x}\right)^2}
  \end{split}
\label{eq:ss_main_effect_integral}
\end{equation}
The integral form given above dispenses with the nested structure of multiple integrals in the original definition of main-effect index.
The multidimensional integration is over $2 \times D - 1$ dimensions
and it is the basis of estimating sensitivity index using \gls{mc} simulation in this thesis, hereinafter referred to as the Sobol'-Saltelli method.
The same procedure applies to derive the total effect-index which yields,
\begin{equation}
  \begin{split}
    ST_d & = \frac{\mathbb{E}_{\sim d}[\mathbb{V}_{d}[Y|\mathbf{X}_{\sim d}]]}{\mathbb{V}[Y]} \\
        & = \frac{\int f^2(\mathbf{x}) d\mathbf{x} - \int \int f(\mathbf{x}_{\sim d}, x^{\prime}_d) f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}^{\prime}_{d} d\mathbf{x}}{\int f(\mathbf{x})^2 d\mathbf{x} - \left( \int f(\mathbf{x}) d\mathbf{x}\right)^2}
  \end{split}
\label{eq:ss_total_effect_integral}
\end{equation}

As it was the case for the Morris method, an implementation of the Sobol'-Saltelli method is also part of \texttt{gsa-module} python3 package (see Appendix~\ref{app:gsa_module} for detail).
For $N$ number of \gls{mc} samples and $D$ number of model parameters, the \gls{mc} simulation procedure to estimate the sensitivity indices follows the sampling and resampling approach adopted in~\cite{Sobol2001,Saltelli2002,Homma1996} described in the following.

\textsc{First}, generate two $N \times D$ independent random samples from a uniform independent distribution in $D$-dimension, $[0,1]^D$:
\begin{equation}
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
\label{eq:ss_two_samples}
\end{equation}

\textsc{Second}, construct $D$ additional design of experiment matrices where each matrix is matrix $A$ with the $d$-th column substituted by the $d$-th column of matrix $B$:\begin{equation}
  \begin{split}
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
  \end{split}
\label{eq:ss_sampling_resampling}
\end{equation}

\textsc{Third}, rescale each element in the matrices of samples to the actual values of model parameters according to their actual range of variation through iso-probabilistic transformation.

\textsc{Fourth}, evaluate the model multiple times using input vectors that correspond to each row of $A$, $B$, and all the $A_B^d$.

\textsc{Fifth} and finally, extract the \gls{qoi}s from all the outputs and recast them as vectors.
The main-effect and total-effect indices are then estimated using the estimators described below.

For the main-effect sensitivity index, two estimators are considered.
One is proposed by Saltelli~\cite{Saltelli2002}, and the other, as an alternative, is proposed by Janon et al~\cite{Janon2014}.
The latter proved to be more efficient, especially for a large variation around a parameter estimate~\cite{Iooss2015,Janon2014}.

The first term in the numerator of Eq.~(\ref{eq:ss_main_effect_integral}) is the same for both estimators and is given by
\begin{equation}
  \int \int f(\mathbf{x}^{\prime}_{\sim d}, x_d) f(\mathbf{x}_{\sim d}, x_d) d\mathbf{x}^{\prime}_{\sim d} d\mathbf{x}_{\sim d} \approx \frac{1}{N}\sum_{n=1}^N f(B)_n \cdot f(A_B^d)_n
\label{eq:ss_first_term}
\end{equation}
where the subscript $n$ corresponds to the row of the sampled model parameters
such that $f(B)_n$ is the model output evaluated using inputs taken from the $n$-th row of matrix $B$
and $f(A_B^d)_n$ is the model output evaluated using inputs taken from the $n$-th row of matrix $A_B^K$.
The \gls{mc} estimator for the second term in the numerator and for the denominator differ for the two considered estimators given in Table~\ref{tab:ss_main_effect_estimator}.

\begin{table}[h]
	\myfloatalign
	\caption[Monte Carlo estimators to estimate the main-effect indices]{Two \gls{mc} estimators for the terms in Eq.~(\ref{eq:ss_main_effect_integral}) to estimate the main-effect indices (the sum is taken implicitly over all samples $N$)}
	\label{tab:ss_main_effect_estimator}
	\begin{tabularx}{\textwidth}{Xll} \toprule
		\tableheadline{Estimator}         & $\mathbb{E}^2[Y] = \left( \int f d\mathbf{x}\right)^2$          & $\mathbb{V}[Y] = \int f^2 d\mathbf{x} - \left( \int f d\mathbf{x}\right)^2$ \\ \midrule
		Saltelli \cite{Saltelli2002}      & $\frac{1}{N} \sum f(A)_n \cdot f(B)_n$                          & $\frac{1}{N}\sum f(A)_n^2-\left(\frac{1}{N}\sum f(A)_n\right)^2$  \\[0.75cm]
		Janon et~al.~\cite{Janon2014}     & $\left(\frac{1}{N} \sum \frac{f(B)_n + f(A_B^d)_n}{2}\right)^2$ & $\frac{1}{N} \sum \frac{f(B)_n^2 + f(A_B^d)_n^2}{2}$ \\
                                      &                                                                 & $\quad -\left(\frac{1}{N} \sum \frac{f(B)_n^2 + f(A_B^d)_n^2}{2}\right)^2$ \\
		\bottomrule
	\end{tabularx}
\end{table}

The general formula of the main-effect sensitivity index estimator is
\begin{equation}
  \widehat{S}_d = \frac{\frac{1}{N}\sum_{n=1}^N f(B)_n \cdot f(A_B^d)_n - \mathbb{E}^2[Y]}{\mathbb{V}[Y]}
\label{eq:ss_main_effec_estimator}
\end{equation}
where and $\mathbb{E}^2[Y]$ and $\mathbb{V}[Y]$ are as prescribed in Table~\ref{tab:ss_main_effect_estimator}.

To estimate the total-effect sensitivity indices, the Jansen estimator~\cite{Jansen1999} is recommended in~\cite{Saltelli2010a}.
The estimator reads
\begin{equation}
  \widehat{ST}_d = \frac{\frac{1}{2N}\sum_{n=1}^{N}\left(f(A)_n - f(A_B^d)_n\right)^2}{\mathbb{V}[Y]}
\label{eq:ss_jansen_estimator}
\end{equation}
where $\mathbb{V}[Y]$ is estimated by the Saltelli et al. estimator in Table~\ref{tab:ss_main_effect_estimator}.

The computational cost associated with the estimation of all the main-effect and total-effect indices is $N \times (D + 2)$ code runs,
\marginpar{computational cost: \\ brute force Monte Carlo vs. Sobol'-Saltelli}
where $N$ is the number of \gls{mc} samples and $D$ is the number of parameters.
Compare this to the cost of brute force Monte Carlo of $2 \times D \times N^2$ code runs to estimate all the main-effect and total-effect sensitivity indices.

As an additional comparison, the cost for Morris method to compute the statistics of elementary effect is $N_R \times (D + 1)$ code runs,
\marginpar{computational cost: \\ Morris vs. Sobol'-Saltelli}
where $N_R$ is the number of OAT design replications.
In either methods, the number of samples $N$ (in the case of the Sobol'-Saltelli method) and replications $N_R$ (in the case of the Morris method)
determines the precision of the estimates.
A larger number of samples (and replications) increases the precision.
Note, however, that in practice the typical number of Morris replications is between $10^1 - 10^2$~\cite{Saltelli2010},
while the number of \gls{mc} samples for the Sobol' indices estimation amounts to $10^2 - 10^4$~\cite{Sobol2001}.

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