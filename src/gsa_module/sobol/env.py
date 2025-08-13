"""Add parent directory to python import path so tests can be run, taken from
http://stackoverflow.com/questions/61151/where-do-the-python-unit-tests-go
"""
import sys
import os

__author__ = "Steely Wing"


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
