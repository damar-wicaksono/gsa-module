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
        self.testpath = "../samples/sobol_seq_gen"
        self.params_sobol = ["../samples/sobol_seq_gen/sobol.o",
                             "../samples/sobol_seq_gen/new-joe-kuo-6.21201"]
        self.benchmark = np.loadtxt("{}/benchmark.txt" .format(self.testpath),
                                    skiprows=1)

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

    def test_is_params_other_than_list_acceptable(self):
        """Is params arguments other than list acceptable?"""
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.d,
                          "srs", 10)

    def test_is_params_more_than_two_acceptable(self):
        """Is the # of params arguments other than 2 acceptable?"""
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.d,
                          "srs", [10, 20, 30])

    def test_is_params_other_than_positive_integer_for_srs_acceptable(self):
        """Is the params arguments other than positive integer acceptable for
        srs? """
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.d,
                          "srs", [-10, 20])
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.d,
                          "srs", [10, -20])

    def test_is_params_other_than_positive_integer_for_lhs_acceptable(self):
        """Is the params arguments other than positive integer acceptable for
        lhs? """
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.d,
                          "lhs", [-10, 20])
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.d,
                          "lhs", [10, -20])


if __name__ == "__main__":
    unittest.main()