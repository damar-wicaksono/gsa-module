"""A class that implements Sobol' indices computation via Monte Carlo sampling.
"""

import numpy as np

from typing import Dict, Callable, Union, Optional
from numpy.random import Generator, RandomState

from gsa_module.samples import srs


class SobolIndices:

    def __init__(
        self,
        num_dims: int,
        estimator: str = "ia",
        rng: Optional[Union[int, Generator, RandomState]] = None,
    ):
        if estimator.lower() not in ["ia"]:
            raise ValueError("Invalid estimator")

        self._estimator = estimator.lower()
        self._num_dims = num_dims
        self._rng = rng
        self._indices = None
        self._total_variance = None

    @property
    def indices(self):
        return self._indices

    @property
    def num_dims(self):
        return self._num_dims

    @property
    def main_effects(self):
        out = np.empty(self._num_dims)
        for i in range(self._num_dims):
            out[i] = self._indices[(i + 1, )]
        return out

    @property
    def total_effects(self):
        return self._indices["total"]

    def create_sample(self, sample_size: int):

        num_dims = self._num_dims
        xx = srs.create(sample_size, 2 * num_dims, self._rng)

        a = xx[:, :num_dims]
        b = xx[:, num_dims:]

        sample_dict = {
            "a": a,
            "b": b,
        }
        for i in range(num_dims):
            sample_dict[f"ab_({i + 1},)"] = a.copy()
            sample_dict[f"ab_({i + 1},)"][:, i] = b[:, i]

            sample_dict[f"ba_({i + 1},)"] = b.copy()
            sample_dict[f"ba_({i + 1},)"][:, i] = a[:, i]

        return sample_dict

    def estimate_from_output(self, yy_dict: Dict[str, np.ndarray]):

        num_dims = self._num_dims
        indices = {}

        fa = yy_dict["a"]
        fb = yy_dict["b"]
        total_tmp = np.empty(num_dims)
        for j in range(num_dims):

            fab_j = yy_dict[f"ab_({j + 1},)"]
            fba_j = yy_dict[f"ba_({j + 1},)"]

            # First order indices
            nom = 2 * np.mean((fa - fab_j) * (fba_j - fb))
            denom = np.mean((fa - fb)**2 + (fab_j - fba_j)**2)

            indices[(j + 1, )] = nom / denom

            # Total order indices
            nom = np.mean((fb - fba_j)**2 + (fa - fab_j)**2)
            denom = np.mean((fa - fb)**2 + (fab_j - fba_j)**2)

            total_tmp[j] = nom / denom

        indices["total"] = total_tmp

        self._indices = indices

    def estimate_from_function(self, func: Callable, sample_size: int, max_order: int = 1):
        # Create sample
        # Evaluate sample
        # Estimate indices
        pass
