'''
Tests similarity functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from . import (boundary_string_from_masses, weight_s_scale, weight_t_scale, 
    confusion_matrix)


class TestSimilarity(unittest.TestCase):
    '''
    Test similarity helper functions.
    '''
    # pylint: disable=R0904,C0103,C0324

    def test_boundary_string_from_masses_none(self):
        '''
        No boundaries.
        '''
        string = boundary_string_from_masses([3])
        self.assertEqual(string, [set(), set()])


    def test_boundary_string_from_masses_full(self):
        '''
        Few boundaries.
        '''
        string = boundary_string_from_masses([1,1,1,1])
        self.assertEqual(string, [set([1]), set([1]), set([1])])


    def test_boundary_string_from_masses_one(self):
        '''
        Few boundaries.
        '''
        string = boundary_string_from_masses([2,3])
        self.assertEqual(string, [set(), set([1]), set(), set()])


    def test_weight_s_scale(self):
        '''
        Test to see that penalties for substitution edits are discounted from
        3 to 1.5.
        '''
        transpositions = [[1,2], [1,3], [1,4]]
        weight = weight_t_scale(transpositions, 4)
        self.assertEqual(weight, 1.5)
        

    def test_weight_t_scale(self):
        '''
        Test to see that penalties for transposition edits are discounted from
        3 to 1.5.
        '''
        substitutions = [[1,2], [1,3], [1,4]]
        weight = weight_s_scale(substitutions, 4)
        self.assertEqual(weight, 1.5)
        weight = weight_s_scale(substitutions, 5, 2)
        self.assertEqual(weight, 1.5)
        

    def test_confusion_matrix(self):
        '''
        Test confusion matrix.
        '''
        cm = confusion_matrix([set([ ]), set([2]), set([]), set([ ]), set([1])],
                              [set([1]), set([1]), set([]), set([1]), set([ ])],
                              convert_to_boundary_strings=False)


if __name__ is "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

