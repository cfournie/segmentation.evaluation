'''
Tests segmentation format utility functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
from segeval.util.test import TestCase
from segeval.format import (convert_positions_to_masses,
                            convert_masses_to_positions,
                            boundary_string_from_masses,
                            convert_nltk_to_masses)


class TestFormat(TestCase):

    '''
    Segmentation-format-related function tests.
    '''

    def test_convert_positions_to_masses(self):
        '''
        Test segment position sequence conversion to masses.
        '''
        self.assertEqual((5,3,5),
                         convert_positions_to_masses([1,1,1,1,1,2,2,2,3,3,3,3,3]))

    def test_convert_positions_to_masses_none(self):
        '''
        Test segment position sequence conversion from masses.
        '''
        self.assertEqual((11,),
                         convert_positions_to_masses([1,1,1,1,1,1,1,1,1,1,1]))

    def test_convert_positions_to_masses_all(self):
        '''
        Test segment position sequence conversion from masses.
        '''
        self.assertEqual((1,1,1,1,1,1,1,1,1,1,1),
                         convert_positions_to_masses([1,2,3,4,5,6,7,8,9,10,11]))

    def test_convert_masses_to_positions(self):
        '''
        Test segment position sequence conversion from masses.
        '''
        self.assertEqual((1,1,1,1,1,2,2,2,3,3,3,3,3),
                         convert_masses_to_positions([5,3,5]))

    def test_convert_masses_to_positions_none(self):
        '''
        Test segment position sequence conversion from masses.
        '''
        self.assertEqual(convert_masses_to_positions([11]),
                         (1,1,1,1,1,1,1,1,1,1,1))

    def test_convert_masses_to_positions_all(self):
        '''
        Test segment position sequence conversion from masses.
        '''
        self.assertEqual(convert_masses_to_positions([1,1,1,1,1,1,1,1,1,1,1]),
                         (1,2,3,4,5,6,7,8,9,10,11))

    def test_boundary_string_from_masses_none(self):
        '''
        No boundaries.
        '''
        string = boundary_string_from_masses([3])
        self.assertEqual(string, (set(), set()))

    def test_boundary_string_from_masses_full(self):
        '''
        Few boundaries.
        '''
        string = boundary_string_from_masses([1,1,1,1])
        self.assertEqual(string, (set([1]), set([1]), set([1])))

    def test_boundary_string_from_masses_one(self):
        '''
        Few boundaries.
        '''
        string = boundary_string_from_masses([2,3])
        self.assertEqual(string, (set(), set([1]), set(), set()))

    def test_convert_nltk_to_masses_pk_ab(self):
        '''
        NLTK-style segmentations starting with a boundary.
        '''
        self.assertEqual(convert_nltk_to_masses('100'), (1,3))
        self.assertEqual(convert_nltk_to_masses('010'), (2,2))

    def test_convert_nltk_to_masses_pk_long(self):
        '''
        NLTK-style segmentations starting with a boundary.
        '''
        self.assertEqual(convert_nltk_to_masses('0100100000'), (2, 3, 6))
        self.assertEqual(convert_nltk_to_masses('0101000000'), (2, 2, 7))
