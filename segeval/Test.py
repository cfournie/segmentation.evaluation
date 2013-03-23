'''
Tests some general segeval utility functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal
from . import convert_positions_to_masses, convert_masses_to_positions, \
    compute_pairwise
from .data.Samples import KAZANTSEVA2012_G5
from .ml.FbMeasure import f_b_measure


class TestSegeval(unittest.TestCase):
    '''
    segeval utility function tests.
    '''
    #pylint: disable=R0904,C0103
    
    def test_convert_positions_to_masses(self):
        '''
        Test segment position sequence conversion to masses.
        '''
        #pylint: disable=C0324
        self.assertEqual([5,3,5],
                    convert_positions_to_masses([1,1,1,1,1,2,2,2,3,3,3,3,3]))
    
    
    def test_convert_positions_to_masses_none(self):
        '''
        Test segment position sequence conversion from masses.
        '''
        #pylint: disable=C0324
        self.assertEqual([11],
                         convert_positions_to_masses([1,1,1,1,1,1,1,1,1,1,1]))
    
    def test_convert_positions_to_masses_all(self):
        '''
        Test segment position sequence conversion from masses.
        '''
        #pylint: disable=C0324
        self.assertEqual([1,1,1,1,1,1,1,1,1,1,1],
                         convert_positions_to_masses([1,2,3,4,5,6,7,8,9,10,11]))
        
      
    def test_convert_masses_to_positions(self):
        '''
        Test segment position sequence conversion from masses.
        '''
        #pylint: disable=C0324
        self.assertEqual([1,1,1,1,1,2,2,2,3,3,3,3,3],
                         convert_masses_to_positions([5,3,5]))
    
    
    def test_convert_masses_to_positions_none(self):
        '''
        Test segment position sequence conversion from masses.
        '''
        #pylint: disable=C0324
        self.assertEqual(convert_masses_to_positions([11]),
                         [1,1,1,1,1,1,1,1,1,1,1])
    
    def test_convert_masses_to_positions_all(self):
        '''
        Test segment position sequence conversion from masses.
        '''
        #pylint: disable=C0324
        self.assertEqual(convert_masses_to_positions([1,1,1,1,1,1,1,1,1,1,1]),
                         [1,2,3,4,5,6,7,8,9,10,11])
    
    def test_compute_pairwise(self):
        '''
        Tests computing pairwise values from dicts.  Ensures that dicts of
        arbitrary size can still be used.
        '''
        expected = (Decimal('0.2441586812212541867438777318'),
                    Decimal('0.2305169230001435997031211478'),
                    Decimal('0.05313805178945413332341442158'),
                    Decimal('0.04705406986889928477977431108'),
                    24)
        
        self.assertEqual(compute_pairwise(KAZANTSEVA2012_G5,
                                          f_b_measure),
                         expected)
        
        