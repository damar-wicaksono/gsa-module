# -*- coding: utf-8 -*-
"""test_sample.py: Module with functions to generate validation data set,
typically for validation a Gaussian Process metamodel fitting
"""
import numpy as np

__author__ = "Damar Wicaksono"


def create_sequential(dm: np.ndarray,
                      num_tests: int,
                      num_candidates: int,
                      obj_function: str = "w2_discrepancy"):
    """Generate sequential validation data set for GP metamodel validation

        Below is the implementation of the GP validation process proposed in (1)
        The basic idea is to generate additional points, taken from a
        low discrepancy sequence (here, it is the Hammersley sequence), to
        preserve to a certain extend the property of the original design but
        still pose a challenge to the fitted model in untried input space.

        Simply separately and randomly generating validation data set from the
        training data set does not ensure that the validation data set actually
        challenges the fitted model, while the popular leave-one-out
        cross-validation technique is problematic due to special property of the
        optimized design that might break if any of the point in the design
        is removed.

        The process in generating validation data set proposed here is
        sequential, where a new validation point is generated one at a time add
        it to the original design, re-evaluate at each iteration the objective
        function (which measure discrepancy such as the w2-discrepancy) of the
        new design and decide whether to accept the new point as validation
        point. Accept the

    **References**

    (1) B. Iooss, L. Boussouf, V. Feuillard, and A. Marrel, "Numerical studies
        of the metamodel fitting and validation process," IEEE 2009 First
        International Conference on Advances in System Simulation, 20-25 Sept.,
        Porto, 2009

    :param dm: the original design matrix
    :param num_tests: the number of requested validation points
    :param num_candidates: the number of candidates from the Hammersley sequence
    :param obj_function: the objective function or the discrepancy measure used
    :returns: the validation data set of size `num_points`
    """
    from . import hammersley
    from . import opt_alg

    # Initialization
    d = dm.shape[1]     # the number of dimension
    # create large number of test point candidates from Hammersley sequence
    candidates = hammersley.create(num_candidates, d)
    train_data = dm.copy()
    valid_data = np.empty((0, d))

    if obj_function == "w2_discrepancy":
        obj_func = opt_alg.objective_functions.w2_discrepancy_fast
    else:
        raise TypeError("Discrepancy measure not supported!")

    # Iterate the requested number of validation points
    for i in range(num_tests):
        obj_values = []

        # Iterate the candidates in the low-discrepancy sequence
        for j in range(candidates.shape[0]):

            train_valid = np.vstack((train_data, candidates[j]))
            obj_values.append(obj_func(train_valid) - obj_func(train_data))

        # Get the argument of the minimum of the objective values
        ind_min = np.argmin(obj_values)

        # Update the training_data
        train_data = np.vstack((train_data, candidates[ind_min]))

        # Update the validation_data
        valid_data = np.vstack((valid_data, candidates[ind_min]))

        # Remove the selected point from the candidates
        candidates = np.delete(candidates, ind_min, 0)

    return valid_data
