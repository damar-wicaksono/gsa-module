""" Unit test class to test Sobol'-Saltelli design matrix generator
"""
import unittest
import env
import numpy as np
from sobol import sobol_saltelli

__author__ = 'wicaksono_d'


class SobolSaltelliTestCase(unittest.TestCase):
    """Tests for `sobol_saltelli.py`"""

    def setUp(self):
        """Test fixture build"""
        self.n = 100
        self.d = 20
        self.params = [894, 3490]

    def test_not_acceptable_scheme(self):
        """Is not acceptable scheme handled correctly?"""
        self.assertRaises(NameError, sobol_saltelli.create, self.n, self.d,
                          "other", self.params)


if __name__ == "__main__":
    unittest.main()