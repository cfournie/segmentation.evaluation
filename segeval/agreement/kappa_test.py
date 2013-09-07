'''
Tests the segmentation versions of Cohen's and Fleiss' Kappa.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal
from .kappa import fleiss_kappa_linear
from ..data.samples import (KAZANTSEVA2012_G5, KAZANTSEVA2012_G2,
                            COMPLETE_AGREEMENT, LARGE_DISAGREEMENT,
                            MULTIPLE_BOUNDARY_TYPES)


class TestKappa(unittest.TestCase):

    '''
    Test segmentation versions of Cohen's Kappa and Fleiss' Multi-Kappa.
    '''

    def test_fleiss_kappa_linear_g5(self):
        '''
        Test Kappa upon Group 5 of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G5
        self.assertEqual(fleiss_kappa_linear(data),
                         Decimal('0.2374030241245084051985691283'))

    def test_fleiss_kappa_linear_g5_ch1(self):
        '''
        Test Kappa upon Group 5, Chapter 1, of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G5['ch1']
        data = {'ch1': data}
        self.assertEqual(fleiss_kappa_linear(data),
                         Decimal('0.1940298507462686567164179104'))

    def test_fleiss_kappa_linear_g2(self):
        '''
        Test Kappa upon Group 2 of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G2
        self.assertEqual(fleiss_kappa_linear(data),
                         Decimal('0.4068521352341765453201908783'))

    def test_fleiss_kappa_linear_g2_ch2(self):
        '''
        Test Kappa upon Group 2, Chapter 2, of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G2['ch2']
        data = {'ch2': data}
        self.assertEqual(fleiss_kappa_linear(data),
                         Decimal('0.5197205281147376181221097781'))

    def test_fleiss_kappa_disagree(self):
        '''
        Test Kappa upon a hypothetical dataset containing large disagreement.
        '''
        data = LARGE_DISAGREEMENT
        self.assertEqual(fleiss_kappa_linear(data),
                         Decimal('-0.05952156715012243360331512524'))

    def test_fleiss_kappa(self):
        '''
        Test Cohen's and Fleiss' Kappa.
        '''
        data1 = {'i1': {'c1': [2, 8, 2, 1],
                        'c2': [2, 1, 7, 2, 1]}}
        kappa1 = fleiss_kappa_linear(data1)
        kappa1f = fleiss_kappa_linear(data1)
        self.assertEqual(kappa1,
                         Decimal('0.7096774193548387096774193548'))
        self.assertEqual(kappa1, kappa1f)
        data2 = {'i1': {'c1': [2, 8, 2, 1],
                        'c2': [11, 2]}}
        kappa2 = fleiss_kappa_linear(data2)
        kappa2f = fleiss_kappa_linear(data2)
        self.assertEqual(kappa2,
                         Decimal('0.1176470588235294117647058823'))
        self.assertEqual(kappa2, kappa2f)
        self.assertTrue(kappa2 < kappa1)

    def test_fleiss_kappa_complete(self):
        '''
        Test Kappa upon a hypothetical dataset containing complete agreement.
        '''
        data_complete = COMPLETE_AGREEMENT
        kappa = fleiss_kappa_linear(data_complete)
        self.assertEqual(kappa, Decimal('1.0'))

    def test_multiple_boundary_types(self):
        '''
        Test multiple boundaries.
        '''
        value = fleiss_kappa_linear(MULTIPLE_BOUNDARY_TYPES)
        self.assertEqual(value, Decimal('0.3333333333333333333333333333'))

    def test_exception_coders(self):
        '''
        Test exception.
        '''
        data = {'i1': {'c1': [2, 8, 2, 1]}}
        self.assertRaises(Exception, fleiss_kappa_linear, data)

    def test_exception_items(self):
        '''
        Test exception.
        '''
        data = {'i1': {'c1': [2, 8, 2, 1],
                       'c2': [2, 8, 2, 1]},
                'i2': {'c1': [2, 1, 7, 2, 1],
                       'c2': [2, 8, 2, 1],
                       'c3': [2, 8, 2, 1]}}
        self.assertRaises(Exception, fleiss_kappa_linear, data)
