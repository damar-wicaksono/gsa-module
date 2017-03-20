# -*- coding: utf-8 -*-
"""
    gsa_module.morris.analyze
    *************************

    Module implementing method to analyze output computed using one
    of the screening design of experiment.
    The importance of parameter can be assessed based on the statistics
    of their elementary effects.
    The computation of the elementary effects differs for the two different
    designs, the trajectory ([1]) and the radial ([2] and [3]).

    Both of them can also be standardized if a rescaled inputs array
    is specified according to the suggestion in [4],
    if this array is not specified  then the elementary effects are set to zero.

    **References**

    (1) Max D. Morris, "Factorial Sampling Plans for Preliminary Computational
        Experiments", Technometrics, Vol. 33, No. 2, pp. 161-174, 1991.
    (2) Michiel J.W. Jansen, Walter A.H. Rossing, and Richard A. Daamen, "Monte
        Carlo Estimation of Uncertainty Contributions from Several Independent
        Multivariate Sources," in Predictability and Nonlinear Modelling in
        Natural Sciences and Economics, Dordrecht, Germany, Kluwer Publishing,
        1994, pp. 334 - 343.
    (3) F. Campolongo, A. Saltelli, and J. Cariboni, "From Screening to
        Quantitative Sensitivity Analysis. A Unified Approach," Computer Physics
        Communications, Vol. 192, pp. 978 - 988, 2011.
    (4) G. Sin and K. V. Gernaey, "Improving the Morris Method for Sensitivity
        Analysis by Scaling the Elementary Effects," in Proc. 19th European
        Symposium on Computer Aided Process Engineering, 2009
"""
import numpy as np


def trajectory(x_normalized: np.ndarray, x_rescaled: np.ndarray, y: np.ndarray):
        r"""Compute the statistics of elementary effects from trajectory design

        With trajectory Morris design, there is no base point per se
        per replication, thus each of the OAT perturbation is relative to the
        last perturbed point

        :param x_normalized: normalized inputs array
        :param x_rescaled: rescaled inputs array
        :param y: k*6 output array, rows correspond to parameters and columns to
            (mu_ee, mu*_ee, sd_ee, mu_see, mu*_see, sd_see)
        """
        # Setup parameters
        num_dims = x_normalized.shape[1]
        num_runs = x_normalized.shape[0]
        num_reps = round(num_runs / (num_dims + 1))

        # Create an empty elementary effect matrix
        ee  = np.zeros([num_reps, num_dims])    # Regular
        see = np.zeros([num_reps, num_dims])    # Standardized

        # Loop over blocks/replications to calculate all the elementary effects
        # for each parameter
        # There is one elementary effect per parameter, per trajectory.
        for i in range(num_reps):

            # Set up indices for this trajectory
            idx0 = np.arange(num_dims+1) + i * (num_dims + 1)
            idx1 = idx0[:num_dims]
            idx2 = idx0[1:(num_dims+1)]

            # In trajectory, no base point per se per replication
            # OAT perturbation is relative to the last perturbed point
            delta_x = x_normalized[idx2, :] - x_normalized[idx1, :]
            delta_y = y[idx2] - y[idx1]

            # The elementary effect is (change in output) / (change in input)
            # Each parameter has one EE per block, because it is only
            # changed once in a replication
            ee[i,:] = np.linalg.solve(delta_x, delta_y)

            # Standardized elementary effects
            if x_rescaled is not None:
                delta_x = x_rescaled[idx2, :] - x_rescaled[idx1, :]
                delta_y = y[idx2] - y[idx1]

                see[i,:] = np.linalg.solve(delta_x, delta_y)

        # Scale the elementary effects,
        # row-wise Hadamard product with the scale factor for each
        # parameters
        if x_rescaled is not None:
            scale = np.std(x_rescaled, axis=0) / np.std(y)
            see[i,:] *= scale

        # Calculate the statistical summary of the elementary effects
        results = np.empty([num_dims, 6])
        for i in range(num_dims):
            results[i,0] = np.average(ee[:,i])
            results[i,1] = np.average(np.abs(ee[:,i]))
            results[i,2] = np.std(ee[:,i])
            results[i,3] = np.average(see[:,i])
            results[i,4] = np.average(np.abs(see[:,i]))
            results[i,5] = np.std(see[:,i])

        # Return the output
        return results


def radial(x_normalized: np.ndarray, x_rescaled: np.ndarray, y: np.ndarray):
    r"""Compute the statistics of elementary effects from a radial design i/o

    With radial Morris design, there is one base point per replication,
    thus OAT perturbation is relative to that particular base point

    :param x_normalized: normalized inputs array
    :param x_rescaled: rescaled inputs array
    :param y: k*6 output array, rows correspond to parameters and columns to
            (mu_ee, mu*_ee, sd_ee, mu_see, mu*_see, sd_see)
    """
    # Setup parameters
    num_dims = x_normalized.shape[1]
    num_runs = x_normalized.shape[0]
    num_reps = round(num_runs / (num_dims + 1))

    # Create an empty elementary effect matrix
    ee = np.empty([num_reps, num_dims])     # Regular
    see = np.zeros([num_reps, num_dims])    # Standardized

    # Loop over blocks/replications to calculate all the elementary effects
    # for each parameter
    # There is one elementary effect per parameter, per trajectory.
    for i in range(num_reps):

        # Set up indices for this trajectory
        idx0 = np.arange(num_dims + 1) + i * (num_dims + 1)
        idx1 = idx0[0]
        idx2 = idx0[1:(num_dims + 1)]

        # In radial, one base point per replication,
        # OAT perturbation is relative to that particular base point
        x_base = np.repeat([x_normalized[idx1, :]], num_dims, axis=0)
        y_base = np.repeat([y[idx1]], num_dims, axis=0)
        delta_x = x_normalized[idx2, :] - x_base
        delta_y = y[idx2] - y_base

        # The elementary effect is (change in output) / (change in input)
        # Each parameter has one EE per block, because it is only
        # changed once in a replication
        ee[i, :] = np.linalg.solve(delta_x, delta_y)

        # Standardized elementary effects
        if x_rescaled is not None:
            x_base = np.repeat([x_rescaled[idx1, :]], num_dims, axis=0)
            y_base = np.repeat([y[idx1]], num_dims, axis=0)
            delta_x = x_rescaled[idx2, :] - x_base
            delta_y = y[idx2] - y_base

            see[i, :] = np.linalg.solve(delta_x, delta_y)

    # Scale the elementary effects,
    # row-wise Hadamard product with the scale factor for each
    # parameters
    if x_rescaled is not None:
        scale = np.std(x_rescaled, axis=0) / np.std(y)
        see[i,:] *= scale

    # Calculate the statistical summary of the elementary effects
    results = np.empty([num_dims, 6])
    for i in range(num_dims):
        results[i, 0] = np.average(ee[:, i])
        results[i, 1] = np.average(np.abs(ee[:, i]))
        results[i, 2] = np.std(ee[:, i])
        results[i, 3] = np.average(see[:, i])
        results[i, 4] = np.average(np.abs(see[:, i]))
        results[i, 5] = np.std(see[:, i])

    # Return the output
    return results
