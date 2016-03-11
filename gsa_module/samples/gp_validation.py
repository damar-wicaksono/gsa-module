# -*- coding: utf-8 -*-
"""gp_validation.py: Module with functions to generate validation dataset for
Gaussian Process fitting validation
"""
import numpy as np

def create_sequential(dm: np.ndarray,
                      num_points: int,
                      num_candidates: int = 10000,
                      obj_function: str = "w2_discrepancy"):
    """Generate sequential validation dataset for GP metamodel validation

        Below is the implementation of the GP validation process proposed in (1)
        The basic idea is to generate additional points, taken from a
        low discrepancy sequence (here it is Hammersley), to preserve to a
        certain extend the property of the original design but still challenge
        the fitted model in untried input space.

        Simply separately and randomly
        generating validation dataset from the training dataset does not ensure
        that the validation dataset actually challenges the fitted model, while
        the popular leave-one-out cross-validation technique is problematic due
        to special property of the optimized design that might break if any of
        the point is removed.

        The process in generating validation dataset is sequential, where a new
        validation point is generated one at a time, re-evaluating at each
        iteration the objective function of a new design and decide whether to
        accept the new point as validation point.

        If the new configuration yields lower objective function, accept the
        point

    **References**

    (1) B. Iooss, L. Boussouf, V. Feuillard, and A. Marrel, "Numerical studies
        of the metamodel fitting and validation process," IEEE 2009 First
        International Conference on Advances in System Simulation, 20-25 Sept.,
        Porto, 2009

    :param dm:
    :param num_points:
    :param num_candidates:
    :param obj_function:
    :return:
    """
    from . import hammersley
    from . import opt_alg

    # Initialization
    k = dm.shape[1]
    candidates = hammersley.create(num_candidates, k)
    train_data = dm.copy()
    valid_data = np.empty((0, k))

    if obj_function == "w2_discrepancy":
        obj_func = opt_alg.objective_functions.w2_discrepancy_fast
    else:
        raise TypeError("Not Supported")

    # Iterate the requested number of validation points
    for i in range(num_points):
        obj_values = []

        # Iterate the candidates in the low-discrepancy sequence
        for j in range(candidates.shape[0]):
            train_valid = np.vstack((train_data, candidates[j]))
            obj_values.append(obj_func(train_valid) - obj_func(train_data))

        # Get the argument of the minimum of the objective values
        arg_min = np.argmin(obj_values)

        # Update the training_data
        train_data = np.vstack((train_data, candidates[arg_min]))

        # Update the validation_data
        valid_data = np.vstack((valid_data, candidates[arg_min]))

        # Remove the selected point from the candidates
        candidates = np.delete(candidates, arg_min, 0)

    return valid_data