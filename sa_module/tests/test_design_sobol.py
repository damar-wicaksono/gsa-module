"""Unit test class to test Sobol Sequence design matrix generator
"""
import unittest
import env
import numpy as np
import os.path
from samples import design_sobol

__author__ = "Damar Wicaksono"


class DesignSobolTestCase(unittest.TestCase):
    """Test cases for design_sobol.py"""

    def setUp(self):
        """Test fixture build"""
        self.n = 100
        self.d = 20
        self.testpath = "../samples/sobol_seq_gen"
        self.genfull = "../samples/sobol_seq_gen/sobol.o"
        self.inffull = "../samples/sobol_seq_gen/sobol.info"
        self.benchmark = np.loadtxt("/benchmark.txt" .format(self.testpath),
                                    skiprows=1)

    def test_is_make_all_works(self):
        """Test whether make will produce the requested files?"""
        design_sobol.makegen("make", self.testpath)
        self.assertTrue(os.path.exists(self.genfull))
        self.assertTrue(os.path.exists(self.inffull))
        design_sobol.makegen("clean", self.testpath)

    def test_is_make_clean_works(self):
        """Test whether make clean will remove the requested files?"""
        design_sobol.makegen("make", self.testpath)
        self.assertTrue(os.path.exists(self.genfull))
        self.assertTrue(os.path.exists(self.inffull))
        design_sobol.makegen("clean", self.testpath)
        self.assertTrue(not os.path.exists(self.genfull))
        self.assertTrue(not os.path.exists(self.inffull))

    def test_is_n_other_than_integer_acceptable(self):
        """Is other than integer for the number of samples acceptable?"""
        pass

    def test_is_n_negative_acceptable(self):
        """Is negative number of samples acceptable?"""
        pass

    def test_is_d_other_than_integer_acceptable(self):
        """Is other than integer for the number of dimensions acceptable?"""
        pass

    def test_is_d_negative_acceptable(self):
        """Is negative number of dimensions acceptable?"""
        pass

    def test_is_dm_same_as_the_benchmark(self):
        """Is the design matrix match the reference?"""
        pass

    def test_is_dm_below_or_equal_one(self):
        """Is the element values in the design matrix below 1.0?"""
        pass

    def test_is_dm_above_or_equal_zero(self):
        """Is the element values in the design matrix above 0.0?"""
        pass

if __name__ == "__main__":
    unittest.main()
