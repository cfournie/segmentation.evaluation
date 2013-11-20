'''
Tests the data merge functions and package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import unittest
import os
from segeval.data.tsv import (input_linear_mass_tsv, input_linear_positions_tsv)
from segeval.data.samples import HEARST_1997_STARGAZER


class TestTsv(unittest.TestCase):

    '''
    Test data merge functions.
    '''

    test_data_dir = os.path.split(__file__)[0]

    def test_input_linear_mass_tsv(self):
        '''
        Test mass TSV file input.
        '''
        tsv_file = os.path.join(self.test_data_dir, 'hearst1997.tsv')
        dataset = input_linear_mass_tsv(tsv_file)
        self.assertEqual(dataset['hearst1997'],
                         HEARST_1997_STARGAZER['stargazer'])

    def test_input_linear_positions_tsv(self):
        '''
        Test position TSV file input.
        '''
        tsv_file = os.path.join(self.test_data_dir, 'hearst1997_positions.csv')
        dataset = input_linear_positions_tsv(tsv_file, delimiter=',')
        self.assertEqual(dataset['hearst1997_positions'],
                         HEARST_1997_STARGAZER['stargazer'])
