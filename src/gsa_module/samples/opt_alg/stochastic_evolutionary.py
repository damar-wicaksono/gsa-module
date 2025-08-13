# -*- coding: utf-8 -*-
"""stochastic_evolutionary.py: Module containing functionalities to optimize
a given Latin Hypercube Design using an implementation of the Enhanced
Stochastic Evolutionary Algorithm proposed by Jin, Chen, and Sudjianto (1).
Details can be found in (1) for the enhanced version and (2) for the original
version.

**References**

 (1) R. Jin, W. Chen, and A. Sudjianto, "An Efficient Algorithm for Constructing
     Optimal Design of Computer Experiments," Proceedings of DETC'03, ASME 2003
     Design Engineering Technical Conferences and Computers and Information in
     Engineering Conference, Chicago, Illinois, Sept. 2-6, 2003.
 (2) Y.G. Saab and V.B. Rao, "Combinatorial Optimization by Stochastic
     Evolution," IEEE Transactions on Computer-Aided Design, vol. 10(4), 1981.
"""
import types
import math
import numpy as np
from . import objective_functions


__author__ = "Damar Wicaksono"


def pick_obj_function(obj_function: str) -> types.FunctionType:
    """Function to select by name the objective function to optimize

    :param obj_function: the name of the objective function
    :return: the objective function (FunctionType data type)
    """
    if obj_function == "w2_discrepancy":
        return objective_functions.w2_discrepancy_fast
    else:
        raise TypeError("Unsupported objective function")


def init_threshold(dm: np.ndarray,
                   obj_func: types.FunctionType,
                   multiplier: float = 0.005) -> float:
    """Calculate the initial threshold as recommended in the article

    The initial threshold is obtained by multiplying the objective function of
    the initial design by a very small multiplier to get a small threshold.

    :param dm: the initial design matrix
    :param obj_func: the objective function (FunctionType data type)
    :param multiplier: the multiplier to have a very small value of threshold
        based on the initial design's objective function (default = 0.005)
    :return: the initial threshold
    """
    return multiplier*obj_func(dm)


def calc_num_candidate(n: int) -> int:
    """Calculate the number of candidates from perturbing the current design

    Recommended in the article is the maximum number of pair combination from a
    given column divided by a factor of 5.

    It is also recommended that the number of candidates to be evaluated does
    not exceed 50

    :param n: the number of elements to be permuted
    :return: the number of candidates from perturbing the current design
        column-wise
    """
    pairs = math.factorial(n) / math.factorial(n-2) / math.factorial(2)
    fac = 5 # The factor recommended in the article

    return min(int(pairs/fac), 50)


def calc_max_inner(n: int, k: int) -> int:
    """Calculate the maximum number of inner iterations

    :math:`\frac{2 \times n_e \times k}{J}`
    It is recommended that the number of inner iterations does not exceed 100

    :param n: the number of samples in the design
    :param k: the number of design dimension
    :return: the maximum number of inner iterations/loop
    """
    pairs = math.factorial(n) / math.factorial(n-2) / math.factorial(2)

    return min(int(2*pairs*k/calc_num_candidate(n)), 100)


def perturb(dm: np.ndarray,
            num_dimension: int,
            num_exchanges: int,
            obj_func: types.FunctionType) -> np.ndarray:
    """Create new configuration of a design matrix according to ESE algorithm

    According to the algorithm, a distinct `num_candidate` designs have to be
    generated from the current design by carrying out a column-wise perturbation
    on a given column `num_dimension`. The best design according to the select
    `obj_function` will be selected as the "perturbed" design

    :param dm: the current design matrix
    :param num_dimension: the column of design matrix to be perturbed
    :param num_exchanges: the number of distinct candidates to be generated
    :param obj_func: the select objective function
    :return: the perturbed state of the current design
    """
    import itertools

    # Create pairs of all possible combination
    num_samples = dm.shape[0]
    pairs = list(itertools.combinations([_ for _ in range(num_samples)], 2))
    # Create random choices for the pair of perturbation, w/o replacement
    rand_choices = np.random.choice(len(pairs), num_exchanges, replace=False)
    # Initialize the search
    obj_func_current = np.inf
    dm_current = dm.copy()
    for i in rand_choices:
        dm_try = dm.copy() # Always perturb from the design passed in argument
        # Do column-wise operation in a given column 'num_dimension'
        dm_try[pairs[i][0], num_dimension] = dm[pairs[i][1], num_dimension]
        dm_try[pairs[i][1], num_dimension] = dm[pairs[i][0], num_dimension]
        obj_func_try = obj_func(dm_try)
        if obj_func_try < obj_func_current:
            # Select the best trial from all the perturbation trials
            obj_func_current = obj_func_try
            dm_current = dm_try.copy()

    return dm_current


def adjust_threshold(threshold: float,
                     flag_imp: bool,
                     flag_explore: bool,
                     n_accepted: int,
                     n_improved: int,
                     num_exchanges: int,
                     improving_params: list,
                     exploring_params: list) -> tuple:
    """Calculate the new threshold based on the results of previous iteration

    :param threshold: the current threshold
    :param flag_imp: the flag indicating whether new best solution was found
    :param flag_explore: the flag indicating whether in exploration mode
    :param n_accepted: the number of accepted solution in the previous iteration
    :param n_improved: the number of new best solution found in previous iter.
    :param num_exchanges: the number of candidates considered from curr. design
    :param improving_params: The 2 parameters used in improving process phase
        (1) the cut-off value to decrease the threshold
        (2) the multiplier to decrease or increase the threshold
    :param exploring_params: The 4 parameters used in exploring process phase
        (1) the cut-off value of acceptance to start increasing the threshold
        (2) the cut-off value of acceptance to start decreasing the threshold
        (3) the cooling multiplier for the threshold
        (4) the warming multiplier for the threshold
    :return: tuple of the update flag_explore (whether still in explore mode)
        and the adjusted threshold
    """
    # Improve vs. Explore Phase and Threshold Update
    if flag_imp:    # Improve
        # New best solution found, carry out improvement process
        if (float(n_accepted/num_exchanges) > improving_params[0]) & \
                (n_accepted > n_improved):
            # Lots acceptance but not all of them is improvement,
            # reduce threshold, make it harder to accept a trial
            threshold *= improving_params[1]
        else:
            # Few acceptance or all trials are improvement, increase threshold
            # make it easier to accept a trial
            threshold /= improving_params[1]

    else:           # Explore, No new best solution found during last iteration
        # Exploring process, warming up vs. cooling down
        if n_accepted < exploring_params[0] * num_exchanges:
            # Reach below limit, increase threshold ("warming up")
            flag_explore = True
        elif n_accepted > exploring_params[1] * num_exchanges:
            # Reach above limit, decrease threshold ("cooling down")
            flag_explore = False

        if flag_explore:
            # Ramp up exploration and below upper limit, increase threshold
            threshold /= exploring_params[3]
        elif not flag_explore:
            # Slow down exploration and above lower limit, decrease threshold
            threshold *= exploring_params[2]

    return flag_explore, threshold


def optimize(dm_init: np.ndarray,
             obj_func_name: str,
             threshold_init: float,
             num_exchanges: int,
             max_inner: int,
             max_outer: int,
             improving_params: list,
             exploring_params: list):
    """Optimize a given design using Enhanced Evolutionary Algorithm

    :param dm_init: the initial design matrix
    :param obj_func_name: the objective function used in the optimization
    :param threshold_init: the initial threshold, if equal or less than zero,
        then calculate from the recommended value
    :param num_exchanges: the number of candidates obtained by perturbing current design,
        0 or less means calculate from the recommended value
    :param max_inner: the maximum number of inner iterations, 0 or less means calculate
        from the recommended value
    :param max_outer: the maximum number of outer iterations, served as the
        stopping criterion for the optimization algorithm
    :param improving_params: The 2 parameters used in improving process phase
        (1) the cut-off value to decrease the threshold
        (2) the multiplier to decrease or increase the threshold
    :param exploring_params: The 4 parameters used in exploring process phase
        (1) the cut-off value of acceptance to start increasing the threshold
        (2) the cut-off value of acceptance to start decreasing the threshold
        (3) the cooling multiplier for the threshold
        (4) the warming multiplier for the threshold
    :return: a collection of obj_function evolution and best design
    """
    import collections

    # Initialize output structure
    OptSolution = collections.namedtuple("OptSolution",
                                         "dm_init dm_best best_evol try_evol")

    # Initialization of Outer Iteration
    n = dm_init.shape[0]     # number of samples
    k = dm_init.shape[1]     # number of dimension
    obj_function = pick_obj_function(obj_func_name)  # Choose objective function
    if threshold_init <= 0.0:
        threshold = init_threshold(dm_init, obj_function)   # Initial threshold
    else:
        threshold = threshold_init
    if num_exchanges <= 0:                  # number of exchanges
        num_exchanges = calc_num_candidate(n)
    if max_inner <= 0:                      # maximum number of inner iterations
        max_inner = calc_max_inner(n, k)

    dm = dm_init.copy()                     # the current design
    obj_func_best = obj_function(dm)        # the best value of obj.func. so far
    obj_func_best_old = obj_function(dm)    # the old value of obj.func.
    flag_explore = False                    # improved flag

    best_evol = []                      # Keep track the best solution
    try_evol = []                       # Keep track the accepted trial solution

    # Begin Outer Iteration
    for outer in range(max_outer):
        # Initialization of Inner Iteration
        n_accepted = 0              # number of accepted trial
        n_improved = 0              # number of improved trial

        # Begin Inner Iteration
        for inner in range(max_inner):
            obj_func = obj_function(dm)
            # Perturb current design
            dm_try = perturb(dm, inner % k, num_exchanges, obj_function)
            obj_func_try = obj_function(dm_try)
            # Check whether solution is acceptable
            if (obj_func_try - obj_func) <= threshold * np.random.rand():
                # Accept solution
                dm = dm_try.copy()
                n_accepted += 1
                try_evol.append(obj_func_try)
                if obj_func_try < obj_func_best:
                    # Best solution found
                    dm_best = dm.copy()
                    obj_func_best = obj_func_try
                    best_evol.append(obj_func_best)
                    n_improved += 1

        # Accept/Reject as Best Solution for convergence checking
        if ((obj_func_best_old - obj_func_best)/obj_func_best) > 1e-6:
            # Improvement found
            obj_func_best_old = obj_func_best
            flag_explore = False  # Reset the explore flag after new best found
            flag_imp = True
        else:
            # Improvement not found
            flag_imp = False

        # Improve vs. Explore Phase and Threshold Update
        flag_explore, threshold = adjust_threshold(threshold, flag_imp,
                                                   flag_explore, n_accepted,
                                                   n_improved,
                                                   num_exchanges,
                                                   improving_params,
                                                   exploring_params)

    output = OptSolution(dm_init = dm_init, dm_best = dm_best,
                         best_evol = best_evol, try_evol = try_evol)

    return output
