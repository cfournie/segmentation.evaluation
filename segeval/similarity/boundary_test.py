'''
Tests boundary similarity (B).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal
from .boundary import boundary_similarity


class TestBoundary(unittest.TestCase):
    '''
    Test.
    '''
    # pylint: disable=R0904,C0103,C0324
    
    def test_fn(self):
        '''
        Test false negative.
        '''
        value = boundary_similarity([2, 3, 6], [5, 6])
        self.assertEqual(0.5, value)
    
    def test_fp(self):
        '''
        Test false negative.
        '''
        value = boundary_similarity([2, 3, 6], [2, 3, 3, 3])
        self.assertAlmostEquals(Decimal('0.66666'), value, 4)
    
    def test_near_miss(self):
        '''
        Test near miss.
        '''
        value = boundary_similarity([2, 3, 6], [2, 2, 7])
        self.assertEqual(0.75, value)
    
    def test_clustered_fps(self):
        '''
        Test near miss.
        '''
        value = boundary_similarity([2, 3, 6], [1, 1, 3, 1, 5])
        self.assertEqual(0.5, value)

