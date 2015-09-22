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

    def test_is_123_the_correct_num_samples(self):
        """Is 123 the number of generated samples?"""
        dm_test = design_srs.create(self.n, self.d, self.seed)
        self.assertEqual(dm_test.shape[0], self.n)

    def test_is_10_the_correct_num_dimension(self):
        """Is 10 the number of dimension?"""
        dm_test = design_srs.create(self.n, self.d, self.seed)
        self.assertEqual(dm_test.shape[1], self.d)

if __name__ == "__main__":
    unittest.main()
