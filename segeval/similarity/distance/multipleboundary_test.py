'''
Tests multiple-boundary edit distance.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import unittest
from segeval.similarity.distance.multipleboundary import (
    boundary_edit_distance, __additions_substitutions__,
    __additions_substitutions_sets__, __has_substitutions__)


class TestMultipleBoundaries(unittest.TestCase):

    '''
    Test multiple boundary edit distance.
    '''

    def test_edit_distance_identity(self):
        '''
        Test a mixed example of additions, substitutions and transpositions.
        '''
        a = [set(), set([1]), set(), set(), set([1]), set(), set(), set(), set(), set()]
        b = a

        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([], [], []),
                         (additions, substitutions, transpositions))

    def test_edit_distance_compliment(self):
        '''
        Test a mixed example of additions, substitutions and transpositions.
        '''
        a = [set(), set(), set(), set(), set(), set(), set(), set(), set(), set()]
        b = [set([1]), set([1]), set([1]), set([1]), set([1]), set([1]), set([1]), set([1]), set([1]), set([1])]

        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([(1, 'b'), (1, 'b'), (1, 'b'), (1, 'b'), (1, 'b'), (1, 'b'), (1, 'b'), (1, 'b'), (1, 'b'), (1, 'b')], [], []),
                         (additions, substitutions, transpositions))

    def test_edit_distance(self):
        '''
        Test a mixed example of additions, substitutions and transpositions.
        '''
        a = [set(), set([1]), set(), set(), set([1]), set(), set(), set(), set(), set()]
        b = [set(), set([2, 3]), set(), set(), set(), set([1]), set(), set(), set([3]), set()]

        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([(3, 'b'), (3, 'b')], [(1, 2)], [(4, 5, 1)]),
                         (additions, substitutions, transpositions))

    def test_edit_distance_two_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([2]), set(), set(), set([2]), set(), set(), set()]
        b = [set(), set(), set(), set(), set(), set([2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([(2, 'a')], [], [(5, 6, 2)]),
                         (additions, substitutions, transpositions))

    def test_edit_distance_no_two_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set([2]), set(), set(), set([2]), set([2]), set(), set(), set()]
        b = [set(), set(), set(), set(), set(), set([2]), set([2]), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([(2, 'a')], [], []),
                         (additions, substitutions, transpositions))

    def test_edit_distance_two_transpositions_equal(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set(), set([2]), set(), set([2]), set(), set(), set()]
        b = [set(), set(), set(), set(), set(), set([2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([(2, 'a')], [], [(4, 5, 2)]),
                         (additions, substitutions, transpositions))

    def test_edit_distance_two_substitutions_into_two_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([2]), set(), set([1]), set(), set(), set(), set()]
        b = [set(), set(), set(), set([1]), set(), set([2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b, n_t=3)
        self.assertEqual(([], [(2, 1), (1, 2)], []),
                         (additions, substitutions, transpositions))

    def test_edit_distance_two_substitutions_into_no_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([2]), set(), set([3]), set(), set(), set(), set()]
        b = [set(), set(), set(), set([1]), set(), set([2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b, n_t=3)
        self.assertEqual(([], [(2,1), (3,2)], []),
                         (additions, substitutions, transpositions))

    def test_edit_distance_two_substitutions_one_ad_into_one_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([2,4]), set(), set([3]), set(), set(), set(), set()]
        b = [set(), set(), set(), set([1]), set(), set([2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b, n_t=3)
        self.assertEqual(([(4, 'a')], [(2, 1), (3, 2)], []),
                         (additions, substitutions, transpositions))

    def test_edit_distance_two_substitutions_one_ad_into_no_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([2]), set(), set([3]), set(), set(), set(), set()]
        b = [set(), set(), set(), set([1,4]), set(), set([2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b, n_t=3)
        self.assertEqual(([(4, 'b')], [(2,1), (3,2)], []),
                         (additions, substitutions, transpositions))

    def test_edit_distance_three_transpositions_overlapping(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([1,2,3]), set(),    set(), set(), set(), set(), set()]
        b = [set(), set(), set(), set(), set([3]), set([1,2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b, n_t=3)
        self.assertEqual(([], [], [(3,4,3),(3,5,1),(3,5,2)]),
                         (additions, substitutions, transpositions))


class TestInnerFncOfMultipleBoundaries(unittest.TestCase):

    '''
    Test private functions for multiple boundary edit distance calculation.
    '''

    def test_has_substitutions_not_present(self):
        '''
        '''
        self.assertFalse(__has_substitutions__(1, 1, 1, set()))

    def test_additions_substitutions(self):
        '''
        Test the expected functionality of __additions_substitutions__
        '''
        a_i = set([1, 2, 3, 4])
        b_i = set([1, 6])

        a = a_i - b_i
        b = b_i - a_i
        d = a_i ^ b_i

        self.assertEqual((2, 1),
                         __additions_substitutions__(d, a, b))

    def test_additions_substitutions_sets(self):
        '''
        Test the expected functionality of __additions_substitutions_sets__
        '''
        a_i = set([1, 2, 3, 4])
        b_i = set([1, 6])

        a = a_i - b_i
        b = b_i - a_i
        d = a_i ^ b_i

        self.assertEqual(([(2, 'a'), (3, 'a')], set([(4, 6)])),
                         __additions_substitutions_sets__(d, a, b))
