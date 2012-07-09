'''
Tests the data i/o functions and package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2012, Chris Fournier
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#       
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================
import os
import unittest
from . import Dataset, load_nested_folders_dict, FILETYPE_JSON
from .TSV import input_linear_mass_tsv, input_linear_positions_tsv
from .JSON import input_linear_mass_json
from .Samples import HEARST_1997_STARGAZER


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
        
        
        
        
        
        