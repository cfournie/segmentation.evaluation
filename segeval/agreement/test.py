'''
Tests actual agreement.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import unittest
from decimal import Decimal
from segeval.agreement import (actual_agreement_linear,
                               __potential_boundaries__,
                               __boundaries__, BoundaryFormat)
from segeval.util import SegmentationMetricError
from segeval.data.samples import (KAZANTSEVA2012_G5, KAZANTSEVA2012_G2,
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

    def test_potential_boundaries_mass(self):
        '''
        Test counting the number of potential boundaries for BoundaryFormat.mass.
        '''
        kwargs = {
            'boundary_format': BoundaryFormat.mass,
            'boundary_types': (1,)
        }
        self.assertEqual(4, __potential_boundaries__([2, 3], [1, 4], **kwargs))

    def test_potential_boundaries_position(self):
        '''
        Test counting the number of potential boundaries for BoundaryFormat.position.
        '''
        kwargs = {
            'boundary_format': BoundaryFormat.position,
            'boundary_types': (1,)
        }
        self.assertEqual(
            4, __potential_boundaries__([1, 1, 1, 2, 2], [1, 1, 2, 2, 3], **kwargs))

    def test_potential_boundaries_sets(self):
        '''
        Test counting the number of potential boundaries for BoundaryFormat.sets.
        '''
        kwargs = {
            'boundary_format': BoundaryFormat.sets,
            'boundary_types': (1,)
        }
        self.assertEqual(
            4, __potential_boundaries__([(), (), (1,), ()], [(), (1,), (), ()], **kwargs))
        self.assertEqual(
            8, __potential_boundaries__([(), (), (1,2), ()], [(), (1,), (), ()], **kwargs))

    def test_potential_boundaries_nltk(self):
        '''
        Test counting the number of potential boundaries for BoundaryFormat.nltk.
        '''
        kwargs = {
            'boundary_format': BoundaryFormat.nltk,
            'boundary_types': (1,)
        }
        self.assertEqual(4, __potential_boundaries__('0010', '0100', **kwargs))

    def test_boundaries_mass(self):
        '''
        Test counting the number of potential boundaries for BoundaryFormat.mass.
        '''
        kwargs = {
            'boundary_format': BoundaryFormat.mass,
            'boundary_types': (1,)
        }
        self.assertEqual(1, __boundaries__([2, 3], **kwargs))

    def test_boundaries_position(self):
        '''
        Test counting the number of potential boundaries for BoundaryFormat.position.
        '''
        kwargs = {
            'boundary_format': BoundaryFormat.position,
            'boundary_types': (1,)
        }
        self.assertEqual(
            1, __boundaries__([1, 1, 1, 2, 2], **kwargs))

    def test_boundaries_sets(self):
        '''
        Test counting the number of potential boundaries for BoundaryFormat.sets.
        '''
        kwargs = {
            'boundary_format': BoundaryFormat.sets,
            'boundary_types': (1,)
        }
        self.assertEqual(
            1, __boundaries__([(), (), (1,), ()], **kwargs))
        self.assertEqual(
            3, __boundaries__([(2,1), (), (1,), ()], **kwargs))

    def test_boundaries_nltk(self):
        '''
        Test counting the number of potential boundaries for BoundaryFormat.nltk.
        '''
        kwargs = {
            'boundary_format': BoundaryFormat.nltk,
            'boundary_types': (1,)
        }
        self.assertEqual(1, __boundaries__('0010', **kwargs))

    def test_potential_boundaries_exception(self):
        '''
        Test an incorrect format when counting the number of potential boundaries.
        '''
        kwargs = {
            'boundary_format': 'incorrect',
            'boundary_types': (1,)
        }
        self.assertRaises(
            SegmentationMetricError,
            __potential_boundaries__,
            '0010', '0100',
            **kwargs)

    def test_boundaries_exception(self):
        '''
        Test an incorrect format when counting the number of potential boundaries.
        '''
        kwargs = {
            'boundary_format': 'incorrect',
            'boundary_types': (1,)
        }
        self.assertRaises(
            SegmentationMetricError,
            __boundaries__,
            '0010',
            **kwargs)
