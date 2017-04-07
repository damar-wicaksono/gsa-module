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


def ee(xx_normalized: np.ndarray,
       y: np.ndarray,
       bootstrap: int = 10000,
       xx_rescaled: np.ndarray = None) -> tuple:
        """Compute the statistics of elementary effects and bootstrap samples

        the function will detect whether xx_normalized is of radial or 
        trajectory design

        :param xx_normalized: normalized inputs array
        :param y: model output array
        :param bootstrap: the number of bootstrap samples
        :param xx_rescaled: rescaled inputs array
        :return: k*6 array, rows correspond to parameters and columns to
            (mu_ee, mu*_ee, sd_ee, mu_see, mu*_see, sd_see) and 
            bootstrap * k * 6 array, 1st dimension is bootstrap replication, 
            2nd dimension is the parameter, and 3rd dimension is statistics 
            of elementary effects
        """
        from .misc import sniff_morris

        # Compute the elementary effects for each replications
        if sniff_morris(xx_normalized)[0] == "trajectory":
            ee, see = trajectory_ee(xx_normalized, y, xx_rescaled)
        elif sniff_morris(xx_normalized)[0] == "radial":
            ee, see = radial_ee(xx_normalized, y, xx_rescaled)
        else:
            raise ValueError("type of morris design cannot be determined!")

        num_dims = ee.shape[1]  # number of dimensions
        num_reps = ee.shape[0]  # number of replications
        # Calculate the statistical summary of the elementary effects
        estimate_results = ee_statistics(ee, see)

        # Do bootstrap
        if bootstrap > 0:
            bootstrap_results = np.empty([bootstrap, num_dims, 6])
            for i in range(bootstrap):
                idx = np.random.choice(num_reps, num_reps, replace=True)
                if see is not None:
                    bootstrap_results[i, :, :] = ee_statistics(ee[idx, :],
                                                               see[idx, :])
                else:
                    bootstrap_results[i, :, :] = ee_statistics(ee[idx, :])
        else:
            bootstrap_results = None

        # Return the output
        return estimate_results, bootstrap_results


def ee_statistics(ee: np.ndarray, see: np.ndarray = None) -> np.ndarray:
    """Compute the statistics of elementary effects

    :param ee: the elementary effects, all dimensions and replications (reps.)
    :param see: the standardized elementary effects, all dimensions and reps.
    :return: k*6 output array, rows correspond to parameters and columns to
        (mu_ee, mu*_ee, sd_ee, mu_see, mu*_see, sd_see)
    """
    # Get some parameters
    num_dims = ee.shape[1]  # number of dimensions
    results = np.empty([num_dims, 6])
    for i in range(num_dims):
        results[i, 0] = np.average(ee[:, i])
        results[i, 1] = np.average(np.abs(ee[:, i]))
        results[i, 2] = np.std(ee[:, i])

    if see is not None:
        for i in range(num_dims):
            results[i, 3] = np.average(see[:, i])
            results[i, 4] = np.average(np.abs(see[:, i]))
            results[i, 5] = np.std(see[:, i])

    return results


def trajectory_ee(xx_normalized: np.ndarray,
                  y: np.ndarray,
                  xx_rescaled: np.ndarray = None) -> tuple:
    """Compute the elementary effects for all blocks in trajectory design
    
        With trajectory Morris design, there is no base point per se
        per replication, thus each of the OAT perturbation is relative to the
        last perturbed point

    :param xx_normalized: normalized ([0,1]) inputs array
    :param y: model output array
    :param xx_rescaled: rescaled inputs array, default is None
    :return: a tuple of two r * k arrays with elementary effects, 
            one for regular and another for standardized
    """
    # Setup parameters
    num_dims = xx_normalized.shape[1]    # number of dimensions
    num_runs = xx_normalized.shape[0]    # number of runs/model evaluations
    num_reps = round(num_runs / (num_dims + 1)) # number of blocks/replicates

    # Create an empty elementary effect matrix
    ee = np.zeros([num_reps, num_dims])  # Regular

    # Compute the scaling factor for each parameter and the output
    if xx_rescaled is not None:
        see = np.zeros([num_reps, num_dims])    # Standardized EE
        scale_xx = np.std(xx_rescaled, axis=0)  # Scaling factor for input
        scale_y = np.std(y)                     # Scaling factor for output
    else:
        see = None

    # Loop over blocks/replications to calculate all the elementary effects
    # for each parameter
    # There is one elementary effect per parameter, per trajectory.
    for i in range(num_reps):

        # Set up indices for this trajectory
        idx0 = np.arange(num_dims + 1) + i * (num_dims + 1)
        idx1 = idx0[:num_dims]
        idx2 = idx0[1:(num_dims + 1)]

        # In trajectory, no base point per se per replication
        # OAT perturbation is relative to the last perturbed point
        delta_xx = xx_normalized[idx2, :] - xx_normalized[idx1, :]
        delta_y = y[idx2] - y[idx1]

        # The elementary effect is (change in output) / (change in input)
        # Each parameter has one EE per block, because it is only
        # changed once in a replication
        ee[i, :] = np.linalg.solve(delta_xx, delta_y)

        # Standardized elementary effects
        if xx_rescaled is not None:
            # Scale the elementary effects,
            # row-wise Hadamard product with the scale factor for each
            # parameters, scaling is done before solving linear equation to
            # avoid numerical issue
            delta_xx = (xx_rescaled[idx2, :] - xx_rescaled[idx1, :]) / scale_xx
            delta_y = (y[idx2] - y[idx1]) / scale_y

            see[i, :] = np.linalg.solve(delta_xx, delta_y)

    # Return the output
    return ee, see


def radial_ee(xx_normalized: np.ndarray,
              y: np.ndarray,
              xx_rescaled: np.ndarray = None) -> tuple:
    """Compute the elementary effects for all blocks in radial design
    
    With radial Morris design, there is one base point per replication,
    thus OAT perturbation is relative to that particular base point

    :param xx_normalized: normalized ([0,1]) inputs array
    :param y: model output array
    :param xx_rescaled: rescaled inputs array, default is None
    :return: a tuple of two r * k arrays with elementary effects, 
        one for regular and another for standardized
    """
    # Setup parameters
    num_dims = xx_normalized.shape[1]   # number of dimensions
    num_runs = xx_normalized.shape[0]   # number of runs/model evaluations
    num_reps = round(num_runs / (num_dims + 1)) # number of replications

    # Create an empty elementary effect matrix
    ee = np.empty([num_reps, num_dims])     # Regular

    # Compute the scaling factor for each parameter and the output
    if xx_rescaled is not None:
        see = np.zeros([num_reps, num_dims])    # Standardized EE
        scale_xx = np.std(xx_rescaled, axis=0)  # Scaling factor for input
        scale_y = np.std(y)                     # Scaling factor for output
    else:
        see = None

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
        xx_base = np.repeat([xx_normalized[idx1, :]], num_dims, axis=0)
        y_base = np.repeat([y[idx1]], num_dims, axis=0)
        delta_xx = xx_normalized[idx2, :] - xx_base
        delta_y = y[idx2] - y_base

        # The elementary effect is (change in output) / (change in input)
        # Each parameter has one EE per block, because it is only
        # changed once in a replication
        ee[i, :] = np.linalg.solve(delta_xx, delta_y)

        # Standardized elementary effects
        if xx_rescaled is not None:
            xx_base = np.repeat([xx_rescaled[idx1, :]], num_dims, axis=0)
            y_base = np.repeat([y[idx1]], num_dims, axis=0)
            # Scale the elementary effects,
            # row-wise Hadamard product with the scale factor for each
            # parameters, scaling is done before solving linear equation to
            # avoid numerical issue
            delta_xx = (xx_rescaled[idx2, :] - xx_base) / scale_xx
            delta_y = (y[idx2] - y_base) / scale_y

            see[i, :] = np.linalg.solve(delta_xx, delta_y)

    return ee, see
