'''
Tests the data merge functions and package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import unittest
import os
import re
from segeval.data import DataIOError
from segeval.data.jsonutils import (
    output_linear_mass_json, input_linear_mass_json,
    __write_json__, Field)
from segeval.data.samples import HEARST_1997_STARGAZER


class TestJsonUtils(unittest.TestCase):

    '''
    Test data merge functions.
    '''

    test_data_dir = os.path.split(__file__)[0]

    def test_output_linear_mass_json(self):
        '''
        Test ``Dataset.add()``.
        '''
        # Output specific file
        file_path_new = os.path.join(
            self.test_data_dir, 'hearst1997_test.json')
        file_path_existing = os.path.join(
            self.test_data_dir, 'hearst1997.json')
        output_linear_mass_json(file_path_new, HEARST_1997_STARGAZER)
        self.assertEqual(re.sub(r'\s+', '', open(file_path_new).read()),
                         re.sub(r'\s', '', open(file_path_existing).read()))
        os.remove(file_path_new)
        self.assertFalse(os.path.exists(file_path_new))
        # Output to folder
        file_path_new = os.path.join(self.test_data_dir, 'output.json')
        output_linear_mass_json(self.test_data_dir, HEARST_1997_STARGAZER)
        self.assertEqual(re.sub(r'\s+', '', open(file_path_new).read()),
                         re.sub(r'\s', '', open(file_path_existing).read()))
        os.remove(file_path_new)
        self.assertFalse(os.path.exists(file_path_new))

    def test_input_linear_mass_json(self):
        '''
        Test mass JSON file input.
        '''
        json_file = os.path.join(self.test_data_dir, 'hearst1997.json')
        dataset = input_linear_mass_json(json_file)
        self.assertEqual(dataset, HEARST_1997_STARGAZER)

    def test_input_exception_without_items(self):
        '''
        Test that exceptions occur when missing the field 'items'.
        '''
        json_file = os.path.join(
            self.test_data_dir, 'hearst1997_missing_items.ejson')
        self.assertRaises(DataIOError, input_linear_mass_json, json_file)

    def test_input_exception_format(self):
        '''
        Test that exceptions occur when given an incorrect file type (TSV).
        '''
        file_path = os.path.join(self.test_data_dir, 'hearst1997.tsv')
        self.assertRaises(DataIOError, input_linear_mass_json, file_path)

    def test_input_exception_bad_type(self):
        '''
        Test that exceptions occur when given an incorrect segmentation type.
        '''
        file_path = os.path.join(
            self.test_data_dir, 'hearst1997_bad_type.ejson')
        self.assertRaises(DataIOError, input_linear_mass_json, file_path)

    def test_input_exception_missing_type(self):
        '''
        Test that exceptions occur when missing a segmentation type.
        '''
        file_path = os.path.join(
            self.test_data_dir, 'hearst1997_missing_type.ejson')
        self.assertRaises(DataIOError, input_linear_mass_json, file_path)

    def test_input_type_exception(self):
        file_path_new = os.path.join(
            self.test_data_dir, 'hearst1997_test.json')
        __write_json__(file_path_new,
                       {Field.segmentation_type: 'incorrect',
                        Field.items: {}})
        self.assertRaises(DataIOError, input_linear_mass_json, file_path_new)
        os.remove(file_path_new)
