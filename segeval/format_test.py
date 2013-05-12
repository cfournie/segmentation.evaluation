'''
Tests some general segeval utility functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from format import convert_positions_to_masses, convert_masses_to_positions


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

        