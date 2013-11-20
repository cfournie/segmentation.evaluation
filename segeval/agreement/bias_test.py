'''
Tests the segmentation version of Arstein and Poesio's bias [ArtsteinPoesio2008]_.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import unittest
from decimal import Decimal
from segeval.agreement.bias import artstein_poesio_bias_linear
from segeval.data.samples import (KAZANTSEVA2012_G5, KAZANTSEVA2012_G2,
                                  COMPLETE_AGREEMENT, LARGE_DISAGREEMENT,
                                  MULTIPLE_BOUNDARY_TYPES)


class TestBias(unittest.TestCase):

    '''
    Test Arstein and Poesio's (2008) annotator bias.
    '''

    def test_bias_g5(self):
        '''
        Test bias upon Group 5 of Kazantseva (2012) data.
        '''
        bias = artstein_poesio_bias_linear(KAZANTSEVA2012_G5)
        self.assertTrue(bias > 0)
        self.assertAlmostEqual(bias,
                               Decimal('0.00277829320319822615823397979'))

    def test_bias_g5_ch1(self):
        '''
        Test bias upon Group 5, Chapter 1, of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G5['ch1']
        data = {'ch1': data}
        bias = artstein_poesio_bias_linear(data)
        self.assertTrue(bias > 0)
        self.assertAlmostEqual(bias,
                               Decimal('0.00390625000000000000000000011'))

    def test_bias_g2(self):
        '''
        Test bias upon Group 2 of Kazantseva (2012) data.
        '''
        bias = artstein_poesio_bias_linear(KAZANTSEVA2012_G2)
        self.assertTrue(bias > 0)
        self.assertAlmostEqual(bias,
                               Decimal('0.00393636062003502686364542151'))

    def test_bias_g2_ch2(self):
        '''
        Test bias upon Group 2, Chapter 2, of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G2['ch2']
        data = {'ch2': data}
        bias = artstein_poesio_bias_linear(data)
        self.assertTrue(bias > 0)
        self.assertAlmostEqual(bias,
                               Decimal('0.00090702947845804988662131528'))

    def test_bias_complete(self):
        '''
        Test bias upon a hypothetical dataset containing complete agreement.
        '''
        bias = artstein_poesio_bias_linear(COMPLETE_AGREEMENT)
        self.assertTrue(bias >= 0)
        self.assertEqual(bias,
                         Decimal('0.008099721956129627956849957112'))

    def test_multiple_boundary_types(self):
        '''
        Test multiple boundaries.
        '''
        value = artstein_poesio_bias_linear(MULTIPLE_BOUNDARY_TYPES)
        self.assertAlmostEqual(value, Decimal('0.00916666666'))

    def test_bias_large(self):
        '''
        Test bias upon a hypothetical dataset containing large disagreement.
        '''
        bias = artstein_poesio_bias_linear(LARGE_DISAGREEMENT)
        self.assertTrue(bias >= 0)
        self.assertEqual(bias,
                         Decimal('0.25'))

    def test_parts(self):
        '''
        Test bias upon a hypothetical dataset containing large disagreement.
        '''

        A_pi_e, A_fleiss_e = artstein_poesio_bias_linear(LARGE_DISAGREEMENT,
                                                         return_parts=True)
        self.assertEqual(A_pi_e,
                         Decimal('0.25'))
        self.assertEqual(A_fleiss_e,
                         Decimal('0.0'))
        self.assertEqual(A_pi_e - A_fleiss_e,
                         Decimal('0.25'))

    def test_exception_coders(self):
        '''
        Test exception.
        '''
        data = {'i1': {'c1': [2, 8, 2, 1]}}
        self.assertRaises(Exception, artstein_poesio_bias_linear, data)

    def test_exception_items(self):
        '''
        Test exception.
        '''
        data = {'i1': {'c1': [2, 8, 2, 1],
                       'c2': [2, 8, 2, 1]},
                'i2': {'c1': [2, 1, 7, 2, 1],
                       'c2': [2, 8, 2, 1],
                       'c3': [2, 8, 2, 1]}}
        self.assertRaises(Exception, artstein_poesio_bias_linear, data)
