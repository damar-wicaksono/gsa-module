"""Unit tests class to test Simple Random Sampling Design generator
"""
import unittest
import env
import numpy as np
from samples import design_srs

__author__ = "Damar Wicaksono"


class DesignSRSTestCase(unittest.TestCase):
    """Tests for `design_srs.py`."""

    def setUp(self):
        """Test fixture build"""
        self.seed = 94385   # the seed
        self.n = 123        # 123 samples
        self.d = 10         # 10-dimensional parameter space
        self.dm = design_srs.create(self.n, self.d, self.seed)

    def test_is_123_the_correct_num_samples(self):
        """Is 123 the number of generated samples?"""
        self.assertEqual(self.dm.shape[0], self.n)

    def test_is_10_the_correct_num_dimension(self):
        """Is 10 the number of dimension?"""
        self.assertEqual(self.dm.shape[1], self.d)

    def test_is_dm_repeatable(self):
        """Is the design matrix repeatable given the same seed number?"""
        new_seed = self.seed
        new_n = self.n
        new_d = self.d
        dm_test_2 = design_srs.create(new_n, new_d, new_seed)
        for i in range(self.dm.shape[0]):
            for j in range(self.dm.shape[1]):
                self.assertEqual(self.dm[i, j], dm_test_2[i, j])

    def test_is_dm_below_one(self):
        """Is the element values in the design matrix less than 1.0?"""
        for i in range(self.dm.shape[0]):
            for j in range(self.dm.shape[1]):
                self.assertLess(self.dm[i, j], 1)

    def test_is_dm_above_zero(self):
        """Is the element values in the design matrix greater than 0.0?"""
        for i in range(self.dm.shape[0]):
            for j in range(self.dm.shape[1]):
                self.assertGreater(self.dm[i, j], 0)

    def test_is_n_other_than_int_acceptable(self):
        """Is other than integer for the parameters is acceptable?"""
        self.assertRaises(TypeError, design_srs.create, 10.1, self.d, self.seed)

    def test_is_n_negative_acceptable(self):
        """Is a negative value for the number of samples acceptable"""
        self.assertRaises(TypeError, design_srs.create, -10, self.d, self.seed)

    def test_is_d_other_than_int_acceptable(self):
        """Is other than integer for the parameters is acceptable?"""
        self.assertRaises(TypeError, design_srs.create, self.n, 1.5, self.seed)

    def test_is_d_negative_acceptable(self):
        """Is a negative value for the number of dimensions acceptable"""
        self.assertRaises(TypeError, design_srs.create, self.n, -10, self.seed)

    def test_is_seed_other_than_int_acceptable(self):
        """Is other than integer for the parameters is acceptable?"""
        self.assertRaises(TypeError, design_srs.create, self.n, self.d, "a")

    def test_is_seed_negative_acceptable(self):
        """Is a negative value for the number of samples acceptable"""
        self.assertRaises(TypeError, design_srs.create, self.n, self.d, -141403)

if __name__ == "__main__":
    unittest.main()
