'''
Tests the WindowDiff evaluation metric.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
from decimal import Decimal
from segeval.compute import summarize
from segeval.format import BoundaryFormat
from segeval.window.pk import pk
from segeval.data.samples import (KAZANTSEVA2012_G5, KAZANTSEVA2012_G2,
                                  COMPLETE_AGREEMENT, LARGE_DISAGREEMENT)
from segeval.util import SegmentationMetricError
from segeval.util.test import TestCase
from segeval.data.samples import HEARST_1997_STARGAZER, HYPOTHESIS_STARGAZER


class TestPk(TestCase):

    '''
    Test Pk.
    '''

    kwargs = {'boundary_format': BoundaryFormat.position}

    def test_one_minus(self):
        '''
        Test one minus.
        '''
        value = pk([2, 3, 6], [2, 2, 7], one_minus=True)
        self.assertAlmostEqual(Decimal('0.77777777'), value)

    def test_return_parts(self):
        '''
        Test one minus.
        '''
        value = pk(KAZANTSEVA2012_G5, return_parts=True)
        self.assertEqual((3, 10), value['ch1,an3,an1'])

    def test_return_parts_dataset(self):
        '''
        Test one minus.
        '''
        value = pk([2, 3, 6], [2, 2, 7], return_parts=True)
        self.assertEqual((2, 9), value)

    def test_identical(self):
        '''
        Test whether identical segmentations produce 0.0.
        '''

        a = [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3]
        b = [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3]
        one_minus_kwargs = dict(TestPk.kwargs)
        one_minus_kwargs['one_minus'] = True
        self.assertEqual(pk(a, b, **self.kwargs), Decimal('0.0'))
        self.assertEqual(pk(a, b, **one_minus_kwargs), Decimal('1.0'))

    def test_no_boundaries(self):
        '''
        Test whether no segments versus some segments produce 1.0.
        '''

        a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        b = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]
        self.assertEqual(pk(b, a, **self.kwargs),
                         Decimal('1.0'))
        self.assertEqual(pk(a, b, **self.kwargs),
                         Decimal('0.3636363636363636363636363636'))

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 7/11 = 0.636
        erroneous windows.
        '''

        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        b = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]
        self.assertEqual(pk(a, b, **self.kwargs),
                         Decimal('0.6363636363636363636363636364'))
        self.assertEqual(pk(b, a, **self.kwargs),
                         Decimal('0.6363636363636363636363636364'))

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 1.0.
        '''

        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        b = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(pk(a, b, **self.kwargs), Decimal('1.0'))
        self.assertEqual(pk(b, a, **self.kwargs), Decimal('1.0'))

    def test_translated_boundary(self):
        '''
        Test whether 2/3 total segments participate in mis-alignment produces
        0.182.
        '''

        a = [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3]
        b = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]
        self.assertEqual(pk(a, b, **self.kwargs),
                         Decimal('0.1818181818181818181818181818'))
        self.assertEqual(pk(b, a, **self.kwargs),
                         Decimal('0.1818181818181818181818181818'))

    def test_extra_boundary(self):
        '''
        Test whether 1/3 segments that are non-existent produces 0.091.
        '''

        a = [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3]
        b = [1, 1, 1, 1, 1, 2, 3, 3, 4, 4, 4, 4, 4]
        self.assertEqual(pk(a, b, **self.kwargs),
                         Decimal('0.09090909090909090909090909091'))
        self.assertEqual(pk(b, a, **self.kwargs),
                         Decimal('0.09090909090909090909090909091'))

    def test_full_miss_and_misaligned(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        0.273.
        '''

        a = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]
        b = [1, 1, 1, 1, 1, 2, 3, 3, 4, 4, 4, 4, 4]
        self.assertEqual(pk(a, b, **self.kwargs),
                         Decimal('0.2727272727272727272727272727'))
        self.assertEqual(pk(b, a, **self.kwargs),
                         Decimal('0.2727272727272727272727272727'))

    def test_all_kwargs_hyp_ref(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        0.273.
        '''

        metric_kwargs = dict(self.kwargs)
        metric_kwargs['hypothesis'] = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]
        metric_kwargs['reference'] = [1, 1, 1, 1, 1, 2, 3, 3, 4, 4, 4, 4, 4]
        self.assertEqual(pk(**metric_kwargs),
                         Decimal('0.2727272727272727272727272727'))

    def test_parts(self):
        '''
        Test parts.
        '''

        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        b = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3]
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

    def test_window_size_specified(self):
        '''
        Test when window size is specified.
        '''
        value = pk([2, 3, 6], [2, 2, 7], window_size=2)
        self.assertAlmostEqual(Decimal('0.2222222'), value)

    def test_boundary_format_nltk(self):
        '''
        Test the nltk boundary format.
        '''
        value = pk(
            '0100100000',
            '0101000000',
            window_size=2,
            boundary_format=BoundaryFormat.nltk)
        self.assertAlmostEqual(Decimal('0.2222222'), value)

    def test_nltk(self):
        '''
        Runs Pk tests from https://github.com/nltk/nltk/blob/master/nltk/test/segmentation.doctest
        '''
        # Originally 0.0
        self.assertAlmostEqual(
            pk('1000100', '1000100', window_size=3,
               boundary_format=BoundaryFormat.nltk),
            Decimal('0.0'))
        # Originally 0.5
        self.assertAlmostEqual(
            pk('010', '100', window_size=2,
               boundary_format=BoundaryFormat.nltk),
            Decimal('0.5'))
        # Originally 0.64
        self.assertAlmostEqual(
            pk('111111', '100100', window_size=2,
               boundary_format=BoundaryFormat.nltk),
            Decimal('0.4'))
        # Originally 0.04
        self.assertAlmostEqual(
            pk('000000', '100100', window_size=2,
               boundary_format=BoundaryFormat.nltk),
            Decimal('0.6'))
        # Originally 0.25
        self.assertAlmostEqual(
            pk('111111', '100100', window_size=3,
               boundary_format=BoundaryFormat.nltk),
            Decimal('0'))
        # Originally 0.25
        self.assertAlmostEqual(
            pk('000000', '100100', window_size=3,
               boundary_format=BoundaryFormat.nltk),
            Decimal('1'))

    def test_long_format(self):
        hypothesis = (
            2,
            31,
            4,
            1,
            1,
            3,
            11,
            5,
            21,
            4,
            2,
            1,
            17,
            26,
            16,
            1,
            17,
            4,
            3,
            7,
            7,
            6,
            12,
            1,
            6,
            25,
            2,
            4,
            3,
            16,
            8)
        reference = (
            2,
            36,
            1,
            3,
            10,
            1,
            5,
            21,
            4,
            3,
            59,
            8,
            10,
            4,
            3,
            7,
            13,
            12,
            7,
            27,
            4,
            3,
            24)
        self.assertAlmostEqual(
            pk(hypothesis, reference),
            Decimal('0.1532567049808429118773946360'))


class TestPairwisePkMeasure(TestCase):

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

    def test_pk_datasets(self):
        '''
        Test pk upon two datasets.
        '''
        hypothesis = HYPOTHESIS_STARGAZER
        reference = HEARST_1997_STARGAZER
        value = pk(hypothesis, reference)
        self.assertAlmostEquals(float(value['stargazer,h1,1']), 0.26315789)
        self.assertAlmostEquals(float(value['stargazer,h2,1']), 0.36842105)
        self.assertAlmostEquals(float(value['stargazer,h1,2']), 0.42105263)
        self.assertAlmostEquals(float(value['stargazer,h2,2']), 0.42105263)
