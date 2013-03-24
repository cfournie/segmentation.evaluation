'''
Tests the data i/o functions and package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import os
import unittest
from . import Dataset, load_nested_folders_dict, FILETYPE_JSON
from .tsv import input_linear_mass_tsv, input_linear_positions_tsv
from .jsonutils import input_linear_mass_json
from .samples import HEARST_1997_STARGAZER


class TestData(unittest.TestCase):
    '''
    Test data i/o functions and package.
    '''
    #pylint: disable=R0904,C0103
    
    test_data_dir = os.path.split(__file__)[0]

    def test_load_nested_folders_dict(self):
        '''
        Test nested folder dict construction.
        '''
        dataset = load_nested_folders_dict(
                        os.path.abspath(os.path.join(self.test_data_dir,
                                                     '../')),
                                           FILETYPE_JSON)
        self.assertEqual(dataset['data,stargazer'],
                         HEARST_1997_STARGAZER['stargazer'])
    
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
    
    def test_input_linear_mass_json(self):
        '''
        Test mass JSON file input.
        '''
        json_file = os.path.join(self.test_data_dir, 'hearst1997.json')
        dataset = input_linear_mass_json(json_file)
        self.assertEqual(dataset, HEARST_1997_STARGAZER)
    
    def test_dataset(self):
        '''
        Test dataset property creation and independence.
        '''
        prop = 'test'
        
        dataset_a = Dataset()
        dataset_a.properties[prop] = False
        
        dataset_b = Dataset()
        
        self.assertFalse(prop in dataset_b)
        
        
        
        
        
        