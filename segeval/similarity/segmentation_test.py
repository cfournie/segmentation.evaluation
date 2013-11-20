'''
Tests segmentation similarity (S).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import, division
import unittest
from decimal import Decimal
from segeval.similarity.segmentation import segmentation_similarity
from segeval.util import SegmentationMetricError
from segeval.format import BoundaryFormat
from segeval.data.samples import (HEARST_1997_STARGAZER, HYPOTHESIS_STARGAZER,
                                  MULTIPLE_BOUNDARY_TYPES, KAZANTSEVA2012_G5)


class TestSegmentation(unittest.TestCase):

    '''
    Test.
    '''

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

    def test_one_minus(self):
        '''
        Test one minus.
        '''
        value = segmentation_similarity([2, 3, 6], [2, 2, 7], one_minus=True)
        self.assertEqual(Decimal('0.05'), value)

    def test_boundary_format_nltk(self):
        '''
        Test the nltk boundary format.
        '''
        value = segmentation_similarity(
            '0100100000',
            '0101000000',
            boundary_format=BoundaryFormat.nltk)
        self.assertAlmostEqual(Decimal('0.95'), value)

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
        numerator, denominator = segmentation_similarity([2, 3, 6], [5, 6],
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

        self.assertAlmostEquals(float(value['stargazer,h1,1']), 0.85)
        self.assertAlmostEquals(float(value['stargazer,h2,1']), 0.725)
        self.assertAlmostEquals(float(value['stargazer,h1,2']), 0.8)
        self.assertAlmostEquals(float(value['stargazer,h2,2']), 0.7)

    def test_s_datasets_return_parts(self):
        '''
        Test S upon two datasets and return fnc parts.
        '''
        hypothesis = HYPOTHESIS_STARGAZER
        reference = HEARST_1997_STARGAZER
        value = segmentation_similarity(
            hypothesis,
            reference,
            return_parts=True)

        self.assertEquals(value['stargazer,h1,1'], (Decimal('17'), 20))

    def test_s_datasets_exception(self):
        '''
        Test S upon two datasets that produces an exception.
        '''
        hypothesis = MULTIPLE_BOUNDARY_TYPES
        reference = HEARST_1997_STARGAZER
        self.assertRaises(
            SegmentationMetricError,
            segmentation_similarity,
            hypothesis,
            reference)

    def test_s_datasets_continue(self):
        '''
        Test S upon two datasets that compares no items.
        '''
        hypothesis = KAZANTSEVA2012_G5
        reference = HEARST_1997_STARGAZER
        value = segmentation_similarity(hypothesis, reference)
        self.assertEqual(value, {})
