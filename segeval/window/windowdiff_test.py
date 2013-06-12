'''
Tests the WindowDiff evaluation metric.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from decimal import Decimal
from .windowdiff import window_diff
from ..data.samples import (KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, 
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT)
from ..compute import summarize
from ..format import BoundaryFormat
from ..util import SegmentationMetricError
from ..util.test import TestCase


class TestWindowDiffPositions(TestCase):
    '''
    Test WindowDiff.
    '''
    # pylint: disable=R0904,C0324
    kwargs = {'boundary_format' : BoundaryFormat.position,
              'lamprier_et_al_2007_fix' : False}

    def test_identical(self):
        '''
        Test whether identical segmentations produce 0.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertEqual(window_diff(a, b, **self.kwargs), 0.0)

    def test_no_boundaries(self):
        '''
        Test whether no segments versus some segments produce 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertAlmostEqual(window_diff(a, b, **self.kwargs),
                         Decimal('0.3636363636363636363636363636'))
        self.assertAlmostEqual(window_diff(b, a, **self.kwargs),
                         Decimal('1'))

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 0.833
        erroneous windows.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertAlmostEqual(window_diff(a, b, **self.kwargs),
                         Decimal('1.0'))
        self.assertAlmostEqual(window_diff(b, a, **self.kwargs),
                         Decimal('1.0'))

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.assertAlmostEqual(window_diff(a, b, **self.kwargs), Decimal('1'))
        self.assertAlmostEqual(window_diff(b, a, **self.kwargs), Decimal('1'))

    def test_translated_boundary(self):
        '''
        Test mis-alignment.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertAlmostEqual(window_diff(a, b, **self.kwargs), # k = 2
                               Decimal(2.0/11.0))
        self.assertAlmostEqual(window_diff(b, a, **self.kwargs),
                               Decimal(2.0/11.0))
    
    def test_extra_boundary(self):
        '''
        Test extra boundary.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertAlmostEqual(window_diff(a, b, **self.kwargs),
                               Decimal(2.0/11.0))
        self.assertAlmostEqual(window_diff(b, a, **self.kwargs),
                               Decimal(2.0/11.0))
    
    def test_full_miss_and_misaligned(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        0.25. 
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertAlmostEqual(window_diff(a, b, **self.kwargs),
                         Decimal('0.2727272727272727272727272727'))
        self.assertAlmostEqual(window_diff(b, a, **self.kwargs),
                         Decimal('0.2727272727272727272727272727'))
    
    def test_fn_vs_fp(self):
        '''
        Test the difference between FP and FN.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertAlmostEqual(window_diff(a, b, **self.kwargs),
                         Decimal('0.1818181818181818181818181818'))
        self.assertAlmostEqual(window_diff(b, a, **self.kwargs),
                         Decimal('0.1818181818181818181818181818'))
        a = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertAlmostEqual(window_diff(a, b, **self.kwargs),
                         Decimal('0.1818181818181818181818181818'))
        self.assertAlmostEqual(window_diff(b, a, **self.kwargs),
                         Decimal('0.1818181818181818181818181818'))
    
    def test_parts(self):
        '''
        Test parts.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        metric_kwargs = dict(self.kwargs)
        metric_kwargs['return_parts'] = True
        self.assertEqual(window_diff(a, b, **metric_kwargs),
                         (11, 11))
    
    def test_format_exception(self):
        '''
        Test format exception.
        '''
        a = [2, 3, 6]
        b = [2, 2, 7]
        self.assertRaises(SegmentationMetricError, window_diff,
                          a, b, boundary_format=BoundaryFormat.sets)

    def test_mass_exception(self):
        '''
        Test length mismatch exception.
        '''
        a = [2, 2, 7]
        b = [2, 2, 8]
        self.assertRaises(SegmentationMetricError, window_diff, a, b)

    def test_one_minus(self):
        '''
        Test whether no segments versus some segments produce 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        metric_kwargs = dict(self.kwargs)
        metric_kwargs['one_minus'] = True
        self.assertAlmostEqual(window_diff(a, b, **metric_kwargs),
                         Decimal('0.6363636363636363636363636364'))
        self.assertAlmostEqual(window_diff(b, a, **metric_kwargs),
                         Decimal('0'))


class TestWindowDiffMasses(TestCase):
    '''
    Test WindowDiff.
    '''
    # pylint: disable=R0904,C0324
    kwargs = {'boundary_format' : BoundaryFormat.mass,
              'lamprier_et_al_2007_fix' : False}

    def test_thesis_all_and_none(self):
        '''
        Test paper example A vs B
        '''
        reference = [11]
        hypothesis = [1,1,1,1,1,1,1,1,1,1,1]
        # Test normal
        actual = window_diff(hypothesis, reference, **self.kwargs)
        self.assertAlmostEqual(1.0, float(actual))
    
    def test_scaiano_paper_b(self):
        '''
        Test paper example A vs B
        '''
        reference = [6,6]
        hypothesis = [12]
        # Test normal
        actual = window_diff(hypothesis, reference, **self.kwargs)
        self.assertAlmostEqual(3.0/9.0, float(actual))
    
    def test_scaiano_paper_c(self):
        '''
        Test paper example A vs C
        '''
        reference = [6,6]
        hypothesis = [5,7]
        # Test normal
        actual = window_diff(hypothesis, reference, **self.kwargs)
        self.assertAlmostEquals(2.0/9.0, float(actual))
    
    def test_scaiano_paper_d(self):
        '''
        Test paper example A vs D
        '''
        reference = [6,6]
        hypothesis = [1,5,6]
        # Test normal
        actual = window_diff(hypothesis, reference, **self.kwargs)
        self.assertAlmostEquals(1.0/9.0, float(actual))
    
    def test_scaiano_paper_e(self):
        '''
        Test paper example A vs E
        '''
        reference = [6,6]
        hypothesis = [5,1,1,5]
        # Test normal
        actual = window_diff(hypothesis, reference, **self.kwargs)
        self.assertAlmostEquals(5.0/9.0, float(actual))


class TestPairwiseWindowDiff(TestCase):
    # pylint: disable=R0904,E1101,W0232
    '''
    Test pairwise WindowDiff.
    '''
    
    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise WindowDiff on Group 5 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertAlmostEquals(summarize(window_diff(KAZANTSEVA2012_G5,
                                              lamprier_et_al_2007_fix=False)),
                         (Decimal('0.42514977232721135'),
                          Decimal('0.14960495739111837'),
                          Decimal('0.02238164327599834'),
                          Decimal('0.02159361560546617'),
                          48))
        self.assertAlmostEquals(summarize(window_diff(KAZANTSEVA2012_G5,
                                              lamprier_et_al_2007_fix=True)),
                         (Decimal('0.3981624488837195'),
                          Decimal('0.1499358110615409'),
                          Decimal('0.022480747438682093'),
                          Decimal('0.021641370219386377'),
                          48))
    def test_pair_g5(self):
        '''
        Test a comparison that is troublesome when using lamprier_et_al_2007_fix 
        '''
        # pylint: disable=C0103
        wd = window_diff(KAZANTSEVA2012_G5['ch4']['an2'],
                         KAZANTSEVA2012_G5['ch4']['an1'],
                         lamprier_et_al_2007_fix=True)
        self.assertAlmostEqual(0.76363636, float(wd))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise WindowDiff on Group 2 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertAlmostEquals(summarize(window_diff(KAZANTSEVA2012_G2,
                                              lamprier_et_al_2007_fix=False)),
                         (Decimal('0.3257163091933661553914718469'),
                          Decimal('0.1586420969856167116081811670'),
                          Decimal('0.02516731493599381893573908435'),
                          Decimal('0.01448197584815743151147537110'),
                          120))
        self.assertAlmostEquals(summarize(window_diff(KAZANTSEVA2012_G2,
                                              lamprier_et_al_2007_fix=True)),
                         (Decimal('0.2745037663246318112728760428'),
                          Decimal('0.1093940158628282748721971010'),
                          Decimal('0.01196705070659672423205913742'),
                          Decimal('0.009986261690691502298962284136'),
                          120))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise WindowDiff on a theoretical dataset
        containing large disagreement.
        '''
        val = summarize(window_diff(LARGE_DISAGREEMENT,
                                    lamprier_et_al_2007_fix=False))
        self.assertAlmostEquals(val,
                        (Decimal('1'),
                         Decimal('0'),
                         Decimal('0'),
                         Decimal('0'),
                         8))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise WindowDiff on a theoretical dataset
        containing complete agreement.
        '''
        self.assertAlmostEquals(summarize(window_diff(COMPLETE_AGREEMENT,
                                                lamprier_et_al_2007_fix=False)),
                         (0.0,
                          0.0,
                          0.0,
                          0.0,
                          48))
        self.assertAlmostEquals(summarize(window_diff(COMPLETE_AGREEMENT,
                                                lamprier_et_al_2007_fix=True)),
                          (0.0,
                           0.0,
                           0.0,
                           0.0,
                           48))
