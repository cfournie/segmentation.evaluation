'''
Tests boundary similarity (B).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import unittest
from decimal import Decimal
from segeval.similarity.boundary import boundary_similarity
from segeval.similarity.weight import weight_a, weight_s, weight_t
from segeval.util import SegmentationMetricError
from segeval.format import BoundaryFormat
from segeval.compute import summarize
from segeval.data.samples import (
    MULTIPLE_BOUNDARY_TYPES, HEARST_1997_STARGAZER,
    HYPOTHESIS_STARGAZER)


class TestBoundary(unittest.TestCase):

    '''
    Test segmenation boundary comparison functions.
    '''

    def test_fn(self):
        '''
        Test false negative.
        '''
        value = boundary_similarity([2, 3, 6], [5, 6])
        self.assertEqual(Decimal('0.5'), value)

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
        self.assertEqual(Decimal('0.75'), value)

    def test_one_minus(self):
        '''
        Test one minus.
        '''
        value = boundary_similarity([2, 3, 6], [2, 2, 7], one_minus=True)
        self.assertEqual(Decimal('0.25'), value)

    def test_boundary_format_nltk(self):
        '''
        Test the nltk boundary format.
        '''
        value = boundary_similarity(
            '01001000000',
            '01010000000',
            boundary_format=BoundaryFormat.nltk)
        self.assertAlmostEqual(Decimal('0.75'), value)

    def test_clustered_fps(self):
        '''
        Test clustered fps.
        '''
        value = boundary_similarity([2, 3, 6], [1, 1, 3, 1, 5])
        self.assertEqual(Decimal('0.5'), value)

    def test_positions(self):
        '''
        Test position-format.
        '''
        a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        b = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]
        value = boundary_similarity(a, b, boundary_format=
                                    BoundaryFormat.position)
        self.assertEqual(Decimal('0'), value)

    def test_int_as_param(self):
        '''
        Test using an int instead of a tuple (common mistake)
        '''
        value = boundary_similarity([11], [5, 6])
        self.assertEqual(Decimal('0'), value)
        value = boundary_similarity([5, 6], [11])
        self.assertEqual(Decimal('0'), value)

    def test_format_exception(self):
        '''
        Test incorrect format exception.
        '''
        a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        b = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]
        self.assertRaises(SegmentationMetricError, boundary_similarity, a, b,
                          boundary_format=None)

    def test_arg_exception(self):
        '''
        Test incorrect argument exception.
        '''
        a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        b = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]
        c = 0
        self.assertRaises(SegmentationMetricError, boundary_similarity, a, b,
                          c)

    def test_weight_t(self):
        '''
        Test transposition weighting.
        '''
        value = boundary_similarity([2, 3, 6], [5, 6],
                                    weight=(weight_a, weight_s, weight_t))
        self.assertEqual(0.5, value)

    def test_multiple_boundary_types(self):
        '''
        Test multiple boundary types with auto boundary type identification.
        '''
        value = summarize(boundary_similarity(MULTIPLE_BOUNDARY_TYPES))
        self.assertEqual((Decimal('0.50'),
                          Decimal('0.25'),
                          Decimal('0.0625'),
                          Decimal('0.1767766952966368811002110906'),
                          2),
                         value)

    def test_multiple_boundary_types_boundary_type(self):
        '''
        Test multiple boundary types with manual boundary type identification.
        '''
        value = summarize(
            boundary_similarity(MULTIPLE_BOUNDARY_TYPES,
                                boundary_types=set([1])))
        self.assertEqual((Decimal('0.50'),
                          Decimal('0.25'),
                          Decimal('0.0625'),
                          Decimal('0.1767766952966368811002110906'),
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
