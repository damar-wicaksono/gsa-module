""" Unit test class to test Sobol'-Saltelli design matrix generator
"""
import unittest
import numpy as np
import env
from sobol import sobol_saltelli
from samples import design_sobol

__author__ = 'wicaksono_d'


class SobolSaltelliTestCase(unittest.TestCase):
    """Tests for `sobol_saltelli.py`"""

    def setUp(self):
        """Test fixture build"""
        self.n = 100
        self.k = 20
        self.params_seed = [894, 3490]
        self.params_sobol = ["../samples/sobol_seq_gen/sobol.o",
                             "../samples/sobol_seq_gen/new-joe-kuo-6.21201"]

    # Sobol'-Saltelli create() function

    def test_not_acceptable_scheme(self):
        """Is not acceptable scheme handled correctly?"""
        self.assertRaises(NameError, sobol_saltelli.create, self.n, self.k,
                          "other", self.params_seed)

    def test_is_n_other_than_positive_integer_acceptable(self):
        """Is the number of samples other than positive integer acceptable?"""
        self.assertRaises(TypeError, sobol_saltelli.create, 10.1, self.k,
                          "srs", self.params_seed)

    def test_is_k_other_than_positive_integer_acceptable(self):
        """Is the # of parameters other than positive integer acceptable?"""
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, -20,
                          "srs", self.params_seed)

    def test_is_params_other_than_list_acceptable(self):
        """Is params arguments other than list acceptable?"""
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.k,
                          "srs", 10)

    def test_is_params_other_than_positive_integer_for_srs_acceptable(self):
        """Is the params arguments other than positive integer acceptable for
        srs? """
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.k,
                          "srs", [-10, 20])
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.k,
                          "srs", [10, -20])

    def test_is_params_other_than_positive_integer_for_lhs_acceptable(self):
        """Is the params arguments other than positive integer acceptable for
        lhs? """
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.k,
                          "lhs", [-10, 20])
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.k,
                          "lhs", [10, -20])

    def test_is_sobol_working(self):
        design_sobol.makegen("make", "../samples/sobol_seq_gen")
        self.assertRaises(TypeError, sobol_saltelli.create, self.n, self.k,
                          "sobol", ["../samples/sobol_seq_gen/sobol.o",
                             "../samples/sobol_seq_gen/new-joe-kuo-6.2121"])
        design_sobol.makegen("clean", "../samples/sobol_seq_gen")

    def test_is_sobol_saltelli_consistent_in_n(self):
        """Is the matrix in the Sobol'-Saltelli design each has n rows?"""
        dm_dict = sobol_saltelli.create(self.n, self.k, "srs", self.params_seed)
        for key in dm_dict:
            self.assertEqual(dm_dict[key].shape[0], self.n)
        dm_dict = sobol_saltelli.create(self.n, self.k, "lhs", self.params_seed)
        for key in dm_dict:
            self.assertEqual(dm_dict[key].shape[0], self.n)
        design_sobol.makegen("make", "../samples/sobol_seq_gen")
        dm_dict = sobol_saltelli.create(self.n, self.k,
                                        "sobol", self.params_sobol)
        for key in dm_dict:
            self.assertEqual(dm_dict[key].shape[0], self.n)
        design_sobol.makegen("clean", "../samples/sobol_seq_gen")

    def test_is_sobol_saltelli_consistent_in_k(self):
        """Is the matrix in the Sobol'-Saltelli design each has n columns?"""
        dm_dict = sobol_saltelli.create(self.n, self.k, "srs", self.params_seed)
        for key in dm_dict:
            self.assertEqual(dm_dict[key].shape[1], self.k)
        dm_dict = sobol_saltelli.create(self.n, self.k, "lhs", self.params_seed)
        for key in dm_dict:
            self.assertEqual(dm_dict[key].shape[0], self.n)
        design_sobol.makegen("make", "../samples/sobol_seq_gen")
        dm_dict = sobol_saltelli.create(self.n, self.k,
                                        "sobol", self.params_sobol)
        for key in dm_dict:
            self.assertEqual(dm_dict[key].shape[1], self.k)
        design_sobol.makegen("clean", "../samples/sobol_seq_gen")

if __name__ == "__main__":
    unittest.main()