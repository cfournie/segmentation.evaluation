'''
Tests the segmentation versions of Scott's and Fleiss' Pi.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import unittest
from decimal import Decimal
from segeval.agreement.pi import fleiss_pi_linear
from segeval.data.samples import (KAZANTSEVA2012_G5, KAZANTSEVA2012_G2,
                                  COMPLETE_AGREEMENT, LARGE_DISAGREEMENT,
                                  MULTIPLE_BOUNDARY_TYPES)


class TestPi(unittest.TestCase):

    '''
    Test segmentation versions of Scott's Pi and Fleiss' Multi-Pi.
    '''

    def test_fliess_pi_g5(self):
        '''
        Test Pi upon Group 5 of Kazantseva (2012) data.
        '''
        self.assertAlmostEqual(fleiss_pi_linear(KAZANTSEVA2012_G5),
                               Decimal('0.2399575652197196472212284944'))

    def test_fliess_pi_g5_ch1(self):
        '''
        Test Pi upon Group 5, Chapter 1, of Kazantseva (2012) data.
        '''
        data = {'ch1': KAZANTSEVA2012_G5['ch1']}
        self.assertAlmostEqual(fleiss_pi_linear(data),
                               Decimal('0.2226720647773279352226720649'))

    def test_fleiss_pi_g2(self):
        '''
        Test Pi upon Group 2 of Kazantseva (2012) data.
        '''
        self.assertAlmostEqual(fleiss_pi_linear(KAZANTSEVA2012_G2),
                               Decimal('0.4083169765912929422042553174'))

    def test_fleiss_pi_g2_ch2(self):
        '''
        Test Pi upon Group 2, Chapter 2, of Kazantseva (2012) data.
        '''
        data = {'ch2': KAZANTSEVA2012_G2['ch2']}
        # Test
        self.assertAlmostEqual(fleiss_pi_linear(data),
                               Decimal('0.5335548172757475083056478405'))

    def test_fleiss_pi_disagree(self):
        '''
        Test Pi upon a hypothetical dataset containing large disagreement.
        '''
        data = LARGE_DISAGREEMENT
        self.assertAlmostEqual(fleiss_pi_linear(data),
                               Decimal('-0.3333333333333333333333333333'))

    def test_fleiss_pi(self):
        '''
        Test Fleiss' Pi.
        '''

        data1 = {'i1': {'c1': [2, 8, 2, 1],
                        'c2': [2, 1, 7, 2, 1]}}
        pi1 = fleiss_pi_linear(data1)
        pi1f = fleiss_pi_linear(data1)
        self.assertAlmostEqual(pi1,
                               Decimal('0.7267552182163187855787476281'))
        self.assertEqual(pi1, pi1f)
        data2 = {'i1': {'c1': [2, 8, 2, 1],
                        'c2': [11, 2]}}
        pi2 = fleiss_pi_linear(data2)
        pi2f = fleiss_pi_linear(data2)
        self.assertAlmostEqual(pi2,
                               Decimal('0.1428571428571428571428571429'))
        self.assertEqual(pi2, pi2f)
        self.assertTrue(pi2 < pi1)

    def test_fleiss_pi_complete(self):
        '''
        Test Pi upon a hypothetical dataset containing complete agreement.
        '''

        data_complete = COMPLETE_AGREEMENT
        pi = fleiss_pi_linear(data_complete)
        self.assertEqual(pi, Decimal('1'))

    def test_multiple_boundary_types(self):
        '''
        Test multiple boundaries.
        '''
        value = fleiss_pi_linear(MULTIPLE_BOUNDARY_TYPES)
        self.assertAlmostEqual(value, Decimal('0.4666666666666666666666666667'))

    def test_exception_coders(self):
        '''
        Test exception.
        '''
        data = {'i1': {'c1': [2, 8, 2, 1]}}
        self.assertRaises(Exception, fleiss_pi_linear, data)

    def test_exception_items(self):
        '''
        Test exception.
        '''
        data = {'i1': {'c1': [2, 8, 2, 1],
                       'c2': [2, 8, 2, 1]},
                'i2': {'c1': [2, 1, 7, 2, 1],
                       'c2': [2, 8, 2, 1],
                       'c3': [2, 8, 2, 1]}}
        self.assertRaises(Exception, fleiss_pi_linear, data)
