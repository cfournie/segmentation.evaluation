'''
Tests the data i/o functions and package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import os
import unittest
from segeval.data import Dataset, load_nested_folders_dict, FILETYPE_JSON, DataIOError
from segeval.data.samples import (HEARST_1997_STARGAZER, COMPLETE_AGREEMENT,
                                  LARGE_DISAGREEMENT)


class TestDataset(unittest.TestCase):

    '''
    Test data i/o functions and package.
    '''

    def test_dataset(self):
        '''
        Test dataset property creation and independence.
        '''
        prop = 'test'
        dataset_a = Dataset()
        dataset_a.properties[prop] = False
        dataset_b = Dataset()
        self.assertFalse(prop in dataset_b.properties)

    def test_add(self):
        '''
        Test ``Dataset.add()``.
        '''
        # Output complete and large disagreement, then merge
        self.assertEqual(set(['an5', 'an6']), LARGE_DISAGREEMENT.coders)
        large_disagreement = LARGE_DISAGREEMENT.copy()
        self.assertEqual(set(['an5', 'an6']), large_disagreement.coders)
        large_disagreement += COMPLETE_AGREEMENT
        self.assertEqual(6, len(large_disagreement.coders))
        self.assertEqual(4, len(large_disagreement))
        self.assertEqual(6, len(large_disagreement['item1']))

    def test_coders(self):
        '''
        Test ``Dataset.add()``.
        '''
        self.assertEqual(
            set(['an4', 'an1', 'an2', 'an3']), COMPLETE_AGREEMENT.coders)

    def test_dataset_property(self):
        '''
        Test dataset property creation and independence.
        '''
        prop = 'test'
        dataset = Dataset(properties={prop: True})
        self.assertTrue(prop in dataset.properties)
        self.assertTrue(dataset.properties[prop])

    def test_add_coders(self):
        '''
        Test dataset property creation and independence.
        '''
        dataset_a = Dataset({'item1': {'a': [2]}})
        dataset_b = Dataset({'item1': {'b': [2]}})
        dataset_c = Dataset({'item1': {'a': [2], 'b': [2]}})

        self.assertNotEqual(dataset_a, dataset_b)
        self.assertEqual(dataset_a + dataset_b, dataset_c)
        self.assertNotEqual(dataset_a, dataset_b)
        self.assertNotEqual(dataset_a, dataset_c)
        self.assertNotEqual(dataset_b, dataset_c)

    def test_add_codings(self):
        '''
        Test dataset property creation and independence.
        '''
        dataset_a = Dataset({'item1': {'a': [2]}})
        dataset_b = Dataset({'item2': {'a': [2]}})
        dataset_c = Dataset({'item1': {'a': [2]},
                             'item2': {'a': [2]}})

        self.assertNotEqual(dataset_a, dataset_b)
        self.assertEqual(dataset_a + dataset_b, dataset_c)
        self.assertNotEqual(dataset_a, dataset_b)
        self.assertNotEqual(dataset_a, dataset_c)
        self.assertNotEqual(dataset_b, dataset_c)

    def test_add_duplicate_codings(self):
        '''
        Test dataset property creation and independence.
        '''
        dataset_a = Dataset({'item1': {'a': [2]}})
        dataset_b = Dataset({'item1': {'a': [2]}})
        exception = False
        try:
            dataset_a + dataset_b
        except DataIOError:
            exception = True
        self.assertTrue(exception, 'Did not throw DataIOError')


class TestUtils(unittest.TestCase):

    '''
    Test data merge functions.
    '''

    test_data_dir = os.path.split(__file__)[0]

    def test_load_nested_folders_dict(self):
        '''
        Test nested folder dict construction.
        '''
        data_dir = os.path.abspath(os.path.join(self.test_data_dir, '../'))
        dataset = load_nested_folders_dict(data_dir, FILETYPE_JSON)
        self.assertEqual(dataset['data,stargazer'],
                         HEARST_1997_STARGAZER['stargazer'])
