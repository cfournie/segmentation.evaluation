'''
Tests similarity functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import unittest
from decimal import Decimal
from segeval.similarity import boundary_confusion_matrix, boundary_statistics
from segeval.format import BoundaryFormat
from segeval.data.samples import HEARST_1997_STARGAZER, HYPOTHESIS_STARGAZER
from segeval.ml import precision, recall, fmeasure


class TestSimilarity(unittest.TestCase):

    '''
    Test similarity helper functions.
    '''

    def test_boundary_confusion_matrix(self):
        '''
        Test confusion matrix.
        '''
        cm = boundary_confusion_matrix(
            [set([]), set([2]), set([]), set([]), set([1]), set([1]),
             set([1]), set([1])],
            [set([1]), set([1]), set([]), set([1]), set([]), set([1]),
             set([]), set([])],
            boundary_format=BoundaryFormat.sets)
        self.assertEqual(cm[None][1], 2)
        self.assertEqual(cm[1][None], 1)
        self.assertEqual(cm[None][2], 0)
        self.assertEqual(cm[2][None], 0)
        self.assertEqual(cm[2][1], 1)
        self.assertEqual(cm[1][2], 0)
        self.assertEqual(cm[1][1], Decimal('1.5'))
        self.assertEqual(cm[2][2], 0)

    def test_boundary_statistics(self):
        '''
        Test boundary statistics.
        '''
        value = boundary_statistics([2, 3, 6], [5, 6])
        self.assertEqual(
            {'matches': [1],
             'boundaries_all': 3,
             'boundary_types': frozenset([1]),
             'pbs': 10,
             'transpositions': [],
             'full_misses': [1],
             'additions': [(1, 'a')],
             'count_edits': Decimal('1'),
             'substitutions': []}, value)

    def test_bed_confusion_matrix(self):
        '''
        Test BED-based confusion matrix upon two segmentations.
        '''
        hypothesis = (5,5,5,5,1)
        reference = HEARST_1997_STARGAZER['stargazer']['2']
        value = boundary_confusion_matrix(hypothesis, reference)
        self.assertAlmostEquals(float(precision(value)), 0.23076923)
        self.assertAlmostEquals(float(recall(value)), 0.23076923)
        self.assertAlmostEquals(float(fmeasure(value)), 0.375)

    def test_bed_confusion_matrix_datasets(self):
        '''
        Test BED-based confusion matrix upon a dataset.
        '''
        hypothesis = HYPOTHESIS_STARGAZER
        reference = HEARST_1997_STARGAZER
        value = boundary_confusion_matrix(hypothesis, reference)
        hyp_p = precision(value)
        hyp_r = recall(value)
        hyp_f = fmeasure(value)
        # Precision
        self.assertAlmostEquals(float(hyp_p['stargazer,h1,1']), 0.57142857)
        self.assertAlmostEquals(float(hyp_p['stargazer,h2,1']), 0.41176470)
        self.assertAlmostEquals(float(hyp_p['stargazer,h1,2']), 0.42857142)
        self.assertAlmostEquals(float(hyp_p['stargazer,h2,2']), 0.33333333)
        # Recall
        self.assertAlmostEquals(float(hyp_r['stargazer,h1,1']), 0.57142857)
        self.assertAlmostEquals(float(hyp_r['stargazer,h2,1']), 0.41176470)
        self.assertAlmostEquals(float(hyp_r['stargazer,h1,2']), 0.42857142)
        self.assertAlmostEquals(float(hyp_r['stargazer,h2,2']), 0.33333333)
        # FMeasure
        self.assertAlmostEquals(float(hyp_f['stargazer,h1,1']), 0.72727272)
        self.assertAlmostEquals(float(hyp_f['stargazer,h2,1']), 0.58333333)
        self.assertAlmostEquals(float(hyp_f['stargazer,h1,2']), 0.6)
        self.assertAlmostEquals(float(hyp_f['stargazer,h2,2']), 0.5)
