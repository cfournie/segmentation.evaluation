'''
Tests the WindowDiff evaluation metric.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from decimal import Decimal
from ..compute import summarize
from ..format import BoundaryFormat
from ..window.pk import pk
from ..data.samples import (KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, 
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT)
from ..util import SegmentationMetricError
from ..util.test import TestCase


class TestPk(TestCase):
    '''
    Test Pk.
    '''
    # pylint: disable=R0904
    kwargs = {'boundary_format' : BoundaryFormat.position}

    def test_identical(self):
        '''
        Test whether identical segmentations produce 0.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        one_minus_kwargs = dict(TestPk.kwargs)
        one_minus_kwargs['one_minus'] = True
        self.assertEqual(pk(a, b, **self.kwargs), 0.0)
        self.assertEqual(pk(a, b, **one_minus_kwargs), 1.0)

    def test_no_boundaries(self):
        '''
        Test whether no segments versus some segments produce 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(pk(b, a, **self.kwargs),
                         Decimal('1.0'))
        self.assertEqual(pk(a, b, **self.kwargs),
                         Decimal('0.3636363636363636363636363636'))

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 7/11 = 0.636
        erroneous windows.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(pk(a, b, **self.kwargs),
                         Decimal('0.6363636363636363636363636364'))
        self.assertEqual(pk(b, a, **self.kwargs),
                         Decimal('0.6363636363636363636363636364'))

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.assertEqual(pk(a, b, **self.kwargs), 1.0)
        self.assertEqual(pk(b, a, **self.kwargs), 1.0)

    def test_translated_boundary(self):
        '''
        Test whether 2/3 total segments participate in mis-alignment produces
        0.182.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(pk(a, b, **self.kwargs),
                         Decimal('0.1818181818181818181818181818'))
        self.assertEqual(pk(b, a, **self.kwargs),
                         Decimal('0.1818181818181818181818181818'))
    
    def test_extra_boundary(self):
        '''
        Test whether 1/3 segments that are non-existent produces 0.091.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(pk(a, b, **self.kwargs),
                         Decimal('0.09090909090909090909090909091'))
        self.assertEqual(pk(b, a, **self.kwargs),
                         Decimal('0.09090909090909090909090909091'))
    
    def test_full_miss_and_misaligned(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        0.273. 
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(pk(a, b, **self.kwargs),
                         Decimal('0.2727272727272727272727272727'))
        self.assertEqual(pk(b, a, **self.kwargs),
                         Decimal('0.2727272727272727272727272727'))

    def test_all_kwargs_hyp_ref(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        0.273. 
        '''
        # pylint: disable=C0324,C0103
        metric_kwargs = dict(self.kwargs)
        metric_kwargs['hypothesis'] = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        metric_kwargs['reference'] = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(pk(**metric_kwargs),
                         Decimal('0.2727272727272727272727272727'))

    def test_parts(self):
        '''
        Test parts.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        metric_kwargs = dict(self.kwargs)
        metric_kwargs['return_parts'] = True
        self.assertEqual(pk(a, b, **metric_kwargs),
                         (7, 11))
    
    def test_format_exception(self):
        '''
        Test format exception.
        '''
        a = [2, 3, 6]
        b = [2, 2, 7]
        self.assertRaises(SegmentationMetricError, pk,
                          a, b, boundary_format=BoundaryFormat.sets)

    def test_mass_exception(self):
        '''
        Test length mismatch exception.
        '''
        a = [2, 2, 7]
        b = [2, 2, 8]
        self.assertRaises(SegmentationMetricError, pk, a, b)


class TestPairwisePkMeasure(TestCase):
    # pylint: disable=R0904,E1101,W0232
    '''
    Test pairwise Pk.
    '''
    
    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise Pk on Group 5 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertAlmostEquals(summarize(pk(KAZANTSEVA2012_G5)),
                         (Decimal('0.35530058282396693'),
                          Decimal('0.11001760846099215'),
                          Decimal('0.012103874171476172'),
                          Decimal('0.015879673965138168'),
                          48))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise Pk on Group 2 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertAlmostEquals(summarize(pk(KAZANTSEVA2012_G2)),
                         (Decimal('0.2882256923776327507173609771'),
                          Decimal('0.1454395656787966169084191445'),
                          Decimal('0.02115266726483699483402909754'),
                          Decimal('0.01327675514600517730547602481'),
                          120))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise Pk on a theoretical dataset
        containing large disagreement.
        '''
        self.assertAlmostEquals(summarize(pk(LARGE_DISAGREEMENT)),
                         (1.0,
                          0.0,
                          0.0,
                          0.0,
                          8))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise Pk on a theoretical dataset
        containing complete agreement.
        '''
        self.assertAlmostEquals(summarize(pk(COMPLETE_AGREEMENT)),
                         (0.0,
                          0.0,
                          0.0,
                          0.0,
                          48))
    
    def test_dataset_kwargs(self):
        '''
        Calculate mean permuted pairwise Pk on a theoretical dataset
        containing complete agreement.
        '''
        self.assertAlmostEquals(summarize(pk(dataset=COMPLETE_AGREEMENT)),
                         (0.0,
                          0.0,
                          0.0,
                          0.0,
                          48))