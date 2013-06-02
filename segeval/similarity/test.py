'''
Tests similarity functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal
from . import boundary_confusion_matrix, boundary_statistics
from ..format import BoundaryFormat


class TestSimilarity(unittest.TestCase):
    '''
    Test similarity helper functions.
    '''
    # pylint: disable=R0904,C0103,C0324
    
    def test_boundary_confusion_matrix(self):
        '''
        Test confusion matrix.
        '''
        cm = boundary_confusion_matrix(
            [set([ ]), set([2]), set([]), set([ ]), set([1]), set([1]),
             set([1]), set([1])],
            [set([1]), set([1]), set([]), set([1]), set([ ]), set([1]),
             set([ ]), set([ ])],
            boundary_format=BoundaryFormat.sets)
        self.assertEqual(cm[None][1], 2)
        self.assertEqual(cm[1][None], 1)
        self.assertEqual(cm[None][2], 0)
        self.assertEqual(cm[2][None], 0)
        self.assertEqual(cm[2][1], 1)
        self.assertEqual(cm[1][2], 0)
        self.assertEqual(cm[1][1], 1.5)
        self.assertEqual(cm[2][2], 0)
    
    def test_boundary_statistics(self):
        '''
        Test false negative.
        '''
        value = boundary_statistics([2, 3, 6], [5, 6])
        self.assertEqual(
            {'matches': [1],
             'boundaries_all': 3,
             'pbs': 10,
             'transpositions': [],
             'full_misses': [1],
             'additions': [(1, 'a')],
             'count_edits': Decimal('1'),
             'substitutions': []}, value)

