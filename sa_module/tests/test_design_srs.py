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

    def test_is_dm_repeatable(self):
        """Is the design matrix repeatable given the same seed number"""
        new_seed = self.seed
        new_n = self.n
        new_d = self.d
        dm_test_1 = design_srs.create(self.n, self.d, self.seed)
        dm_test_2 = design_srs.create(new_n, new_d, new_seed)
        for i in range(dm_test_1.shape[0]):
            for j in range(dm_test_2.shape[1]):
                self.assertEqual(dm_test_1[i, j], dm_test_2[i, j])

if __name__ == "__main__":
    unittest.main()
