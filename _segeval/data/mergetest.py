'''
Tests the data merge functions and package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
import copy
from .Samples import LARGE_DISAGREEMENT, COMPLETE_AGREEMENT


class TestMerge(unittest.TestCase):
    '''
    Test data merge functions.
    '''
    #pylint: disable=R0904,C0103
    
    def testAdd(self):
        '''
        Test ``Dataset.add()``.
        '''
        # Output complete and larege disagreement, then merge
        large_disagreement = copy.deepcopy(LARGE_DISAGREEMENT)
        large_disagreement.add(COMPLETE_AGREEMENT)
        self.assertTrue(6, len(large_disagreement.coders))
        self.assertTrue(4, len(large_disagreement))
        self.assertTrue(2, len(large_disagreement['item1']))
        
