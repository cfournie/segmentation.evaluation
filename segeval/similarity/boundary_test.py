'''
Tests boundary similarity (B).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal
from .boundary import boundary_similarity
from .weight import weight_a, weight_s, weight_t
from ..format import BoundaryFormat 
from ..util import SegmentationMetricError
from ..compute import summarize
from ..data.samples import (MULTIPLE_BOUNDARY_TYPES, HEARST_1997_STARGAZER,
                            HYPOTHESIS_STARGAZER)


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
    
    def test_positions(self):
        '''
        Test false negative.
        '''
        a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        value = boundary_similarity(a, b, boundary_format=\
                                    BoundaryFormat.position)
        self.assertEqual(0, value)
    
    def test_format_exception(self):
        '''
        Test false negative.
        '''
        a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertRaises(SegmentationMetricError, boundary_similarity, a, b,
                          boundary_format=None)
    
    def test_arg_exception(self):
        '''
        Test false negative.
        '''
        a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        c = 0
        self.assertRaises(SegmentationMetricError, boundary_similarity, a, b,
                          c)
    
    def test_weight_t(self):
        '''
        Test false negative.
        '''
        value = boundary_similarity([2, 3, 6], [5, 6],
                                    weight=(weight_a, weight_s, weight_t))
        self.assertEqual(0.5, value)
    
    def test_multiple_boundary_types(self):
        '''
        Test false negative.
        '''
        value = summarize(boundary_similarity(MULTIPLE_BOUNDARY_TYPES))
        self.assertEqual((0.375,
                          0.125,
                          0.015625,
                          Decimal('0.08838834764831844055010554528'),
                          2),
                          value)

    def test_b_datasets(self):
        '''
        Test B upon two datasets.
        '''
        hypothesis = HYPOTHESIS_STARGAZER
        reference = HEARST_1997_STARGAZER
        value = boundary_similarity(hypothesis, reference)

        # Precision
        self.assertAlmostEquals(float(value['stargazer,h1,1']), 0.57142857)
        self.assertAlmostEquals(float(value['stargazer,h2,1']), 0.38888888)
        self.assertAlmostEquals(float(value['stargazer,h1,2']), 0.42857142)
        self.assertAlmostEquals(float(value['stargazer,h2,2']), 0.33333333)


