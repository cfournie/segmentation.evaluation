'''
Tests the data merge functions and package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
import copy
from .samples import LARGE_DISAGREEMENT, COMPLETE_AGREEMENT


class TestMerge(unittest.TestCase):
    '''
    Test data merge functions.
    '''
    #pylint: disable=R0904,C0103
    
