'''
Tests actual agreement.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal
from . import actual_agreement_linear
from ..data.samples import (KAZANTSEVA2012_G5, KAZANTSEVA2012_G2,
                            COMPLETE_AGREEMENT, LARGE_DISAGREEMENT)


class TestAgreement(unittest.TestCase):

    '''
    Test actual agreement.
    '''

    kwargs = {'return_parts': False}

    def test_agreement_g5(self):
        '''
        Test agreement upon Group 5 of Kazantseva (2012) data.
        '''
        agreement = actual_agreement_linear(KAZANTSEVA2012_G5)
        self.assertTrue(agreement > 0)
        self.assertEqual(agreement,
                         Decimal('0.2564575645756457564575645756'))

    def test_agreement_g5_ch1(self):
        '''
        Test agreement upon Group 5, Chapter 1, of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G5['ch1']
        data = {'ch1': data}
        agreement = actual_agreement_linear(data)
        self.assertTrue(agreement > 0)
        self.assertEqual(agreement,
                         Decimal('0.25'))

    def test_agreement_g2(self):
        '''
        Test agreement upon Group 2 of Kazantseva (2012) data.
        '''
        agreement = actual_agreement_linear(KAZANTSEVA2012_G2)
        self.assertTrue(agreement > 0)
        self.assertEqual(agreement,
                         Decimal('0.4201773835920177383592017738'))

    def test_agreement_g2_ch2(self):
        '''
        Test agreement upon Group 2, Chapter 2, of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G2['ch2']
        data = {'ch2': data}
        agreement = actual_agreement_linear(data)
        self.assertTrue(agreement > 0)
        self.assertEqual(agreement,
                         Decimal('0.5465116279069767441860465116'))

    def test_agreement_complete(self):
        '''
        Test agreement upon a hypothetical dataset containing complete agreement.
        '''
        agreement = actual_agreement_linear(COMPLETE_AGREEMENT)
        self.assertTrue(agreement >= 0)
        self.assertEqual(agreement,
                         Decimal('1'))

    def test_disagreement_large(self):
        '''
        Test agreement upon a hypothetical dataset containing large disagreement.
        '''
        agreement = actual_agreement_linear(LARGE_DISAGREEMENT)
        self.assertTrue(agreement >= 0)
        self.assertEqual(agreement,
                         Decimal('0'))
