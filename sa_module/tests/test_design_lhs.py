"""Unit test class to test the implementation of LHS design generator
"""
import unittest
import env
import numpy as np
from samples import design_lhs

__author__ = "Damar Wicaksono"


class DesignLHSTestCase(unittest.TestCase):
    """Tests for design_lhs.py"""

    def setUp(self):
        """Test fixture build"""
        self.seed = 7893457     # Seed number
        self.n = 100            # Number of samples
        self.d = 20             # Number of dimension
        self.dm = design_lhs.create(self.n, self.d, self.seed)

    def test_is_n_other_than_integer_acceptable(self):
        """Is other than integer for the number of samples acceptable?"""
        self.assertRaises(TypeError, design_lhs.create, 25.8, self.d, self.seed)

    def test_is_n_negative_acceptable(self):
        """Is a negative value for the number of samples acceptable?"""
        self.assertRaises(TypeError, design_lhs.create, -100, self.d, self.seed)

    def test_is_d_other_than_integer_acceptable(self):
        """Is other than integer for the number of dimensions acceptable?"""
        self.assertRaises(TypeError, design_lhs.create, self.n, "ab", self.seed)

    def test_is_d_negative_acceptable(self):
        """Is a negative value for the number of samples acceptable?"""
        self.assertRaises(TypeError, design_lhs.create, self.n, -15, self.seed)

    def test_is_seed_other_than_integer_acceptable(self):
        """Is other than integer for the seed number accepatable?"""
        self.assertRaises(TypeError, design_lhs.create, self.n, self.d, 1.234)

    def test_is_n_negative_acceptable(self):
        """Is a negative value for the number of samples acceptable?"""
        self.assertRaises(TypeError, design_lhs.create, self.n, self.d, -123)

if __name__ == "__main__":
    unittest.main()