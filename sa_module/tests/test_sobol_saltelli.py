""" Unit test class to test Sobol'-Saltelli design matrix generator
"""
import unittest
import numpy as np
import env
from sobol import sobol_saltelli

__author__ = 'wicaksono_d'


class SobolSaltelliTestCase(unittest.TestCase):
    """Tests for `sobol_saltelli.py`"""

    def setUp(self):
        """Test fixture build"""
        self.n = 100
        self.d = 20
        self.params_seed = [894, 3490]

    def test_not_acceptable_scheme(self):
        """Is not acceptable scheme handled correctly?"""
        self.assertRaises(NameError, sobol_saltelli.create, self.n, self.d,
                          "other", self.params_seed)

    def test_is_n_other_than_positive_integer_acceptable(self):
        """Is the number of samples other than positive integer acceptable?"""
        self.assertRaises(TypeError, sobol_saltelli.create, 10.1, self.d,
                          "srs", self.params_seed)

    def test_is_k_other_than_positive_integer_acceptable(self):
        """Is the # of parameters other than positive integer acceptable?"""
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, -20,
                          "srs", self.params_seed)

if __name__ == "__main__":
    unittest.main()