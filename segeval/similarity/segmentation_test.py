'''
Tests segmentation similarity (S).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal
from .segmentation import segmentation_similarity
from ..util import SegmentationMetricError
from ..data.samples import HEARST_1997_STARGAZER, HYPOTHESIS_STARGAZER


class TestSegmentation(unittest.TestCase):
    '''
    Test.
    '''
    # pylint: disable=R0904,C0103,C0324
    
    def test_fn(self):
        '''
        Test false negative.
        '''
        value = segmentation_similarity([2, 3, 6], [5, 6])
        self.assertEqual(Decimal('0.9'), value)
    
    def test_fp(self):
        '''
        Test false negative.
        '''
        value = segmentation_similarity([2, 3, 6], [2, 3, 3, 3])
        self.assertEqual(Decimal('0.9'), value)
    
    def test_near_miss(self):
        '''
        Test near miss.
        '''
        value = segmentation_similarity([2, 3, 6], [2, 2, 7])
        self.assertEqual(Decimal('0.95'), value)
    
    def test_clustered_fps(self):
        '''
        Test near miss.
        '''
        value = segmentation_similarity([2, 3, 6], [1, 1, 3, 1, 5])
        self.assertEqual(Decimal('0.8'), value)
    
    def test_parts(self):
        '''
        Test false negative.
        '''
        numerator, denominator  = segmentation_similarity([2, 3, 6], [5, 6],
                                                          return_parts=True)
        self.assertEqual(Decimal('9'), numerator)
        self.assertEqual(Decimal('10'), denominator)
    
    def test_format_exception(self):
        '''
        Test false negative.
        '''
        a = [2, 3, 6]
        b = [2, 2, 7]
        self.assertRaises(SegmentationMetricError, segmentation_similarity,
                          a, b, boundary_format=None)

    def test_mass_exception(self):
        '''
        Test false negative.
        '''
        a = [2, 2, 7]
        b = [2, 2, 8]
        self.assertRaises(SegmentationMetricError, segmentation_similarity,
                          a, b)

    def test_s_datasets(self):
        '''
        Test S upon two datasets.
        '''
        hypothesis = HYPOTHESIS_STARGAZER
        reference = HEARST_1997_STARGAZER
        value = segmentation_similarity(hypothesis, reference)

        # Precision
        self.assertAlmostEquals(float(value['stargazer,h1,1']), 0.85)
        self.assertAlmostEquals(float(value['stargazer,h2,1']), 0.725)
        self.assertAlmostEquals(float(value['stargazer,h1,2']), 0.8)
        self.assertAlmostEquals(float(value['stargazer,h2,2']), 0.7)

