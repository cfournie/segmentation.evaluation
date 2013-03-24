'''
Tests the WinPR evaluation metric.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal
from .winpr import pairwise_win_pr, win_pr, win_pr_f
from ..data.samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT
from ..utils import AlmostTestCase


class TestWinPR(unittest.TestCase):
    '''
    Test WinPR.
    '''
    # pylint: disable=R0904,C0324

    def test_identical(self):
        '''
        Test whether identical segmentations produce 1.0.
        '''
        segs_a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        segs_b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 0, 'tn': 14, 'fn': 0, 'tp': 4} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('1') )

    def test_no_boundaries(self):
        '''
        Test whether no segments versus some segments produce 0.6667.
        '''
        segs_a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        segs_b = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 14, 'tn': 14, 'fn': 0, 'tp': 0} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 0, 'tn': 14, 'fn': 4, 'tp': 0} )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0') )

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 0.4444.
        '''
        segs_a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        segs_b = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                          {'fp': 0, 'tn': -2, 'fn': 10, 'tp': 2} )
        self.assertAlmostEqual(
                        win_pr_f(segs_a, segs_b, convert_from_masses=False),
                        Decimal('0.2857142857142857142857142857') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 20, 'tn': -6, 'fn': 0, 'tp': 4} )
        self.assertAlmostEqual(
                        win_pr_f(segs_b, segs_a, convert_from_masses=False),
                        Decimal('0.2857142857142857142857142857') )

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 0.25.
        '''
        segs_a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        segs_b = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 0, 'tn': -2, 'fn': 12, 'tp': 0} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 84, 'tn': -56, 'fn': 0, 'tp': 0} )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0') )

    def test_translated_boundary(self):
        '''
        Test whether 2/3 total segments participate in mis-alignment produces
        0.75.
        '''
        segs_a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        segs_b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 1, 'tn': 13, 'fn': 1, 'tp': 3} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0.75') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 1, 'tn': 13, 'fn': 1, 'tp': 3} )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0.75') )
    
    def test_extra_boundary(self):
        '''
        Test whether 1/3 segments that are non-existent produces 0.889.
        '''
        segs_a = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        segs_b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 2, 'tn': 12, 'fn': 0, 'tp': 4} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0.8') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 0, 'tn': 12, 'fn': 2, 'tp': 4} )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0.8') )
    
    def test_full_miss_and_misaligned(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        '0.6667. 
        '''
        segs_a = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        segs_b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 3, 'tn': 11, 'fn': 1, 'tp': 3} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0.6') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 1, 'tn': 11, 'fn': 3, 'tp': 3}  )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0.6') )
    
    def test_paper_b(self):
        '''
        Test paper example A vs B
        '''
        reference = [6,6]
        hyp_b = [12]
        self.assertEqual(win_pr(hyp_b, reference, convert_from_masses=True),
                         {'fp': 0, 'tn': 18, 'fn': 3, 'tp': 0} )
    
    def test_paper_c(self):
        '''
        Test paper example A vs B
        '''
        reference = [6,6]
        hyp_b = [5, 7]
        self.assertEqual(win_pr(hyp_b, reference, convert_from_masses=True),
                         {'fp': 1, 'tn': 17, 'fn': 1, 'tp': 2} )
    
    def test_paper_d(self):
        '''
        Test paper example A vs B
        '''
        reference = [6,6]
        hyp_b = [1, 5, 6]
        self.assertEqual(win_pr(hyp_b, reference, convert_from_masses=True),
                         {'fp': 3, 'tn': 15, 'fn': 0, 'tp': 3} )
    
    def test_paper_e(self):
        '''
        Test paper example A vs B
        '''
        reference = [6,6]
        hyp_b = [5, 1, 1, 5]
        self.assertEqual(win_pr(hyp_b, reference, convert_from_masses=True),
                         {'fp': 6, 'tn': 12, 'fn': 0, 'tp': 3} )
    
    def test_paper_b_variant(self):
        '''
        Test paper example A vs B
        '''
        reference = [6,7]
        hyp_b = [13]
        self.assertEqual(win_pr(hyp_b, reference, convert_from_masses=True),
                         {'fp': 0, 'tn': 21, 'fn': 3, 'tp': 0} )
    

class TestPairwiseWinPR(AlmostTestCase):
    # pylint: disable=R0904,E1101,W0232
    '''
    Test pairwise WinPR.
    '''
    
    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise percentage on Group 5 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertAlmostEquals(pairwise_win_pr(KAZANTSEVA2012_G5),
                         (Decimal('0.428415257642714534961510445'),
                          Decimal('0.1826269902482006217397900299'),
                          Decimal('0.03335261756711636499053638142'),
                          Decimal('0.03727857828069424298430979826'),
                          24))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise percentage on Group 2 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertAlmostEquals(pairwise_win_pr(KAZANTSEVA2012_G2),
                         (Decimal('0.6225356510043595404055377518'),
                          Decimal('0.1362766639153026527641337870'),
                          Decimal('0.01857132912788435214526670332'),
                          Decimal('0.01759324166068908032856815646'),
                          60))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing large disagreement.
        '''
        self.assertAlmostEquals(pairwise_win_pr(LARGE_DISAGREEMENT),
                         (Decimal('0'),
                          Decimal('0'),
                          Decimal('0'),
                          Decimal('0'),
                          4))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing complete agreement.
        '''
        self.assertAlmostEquals(pairwise_win_pr(COMPLETE_AGREEMENT),
                         (1.0,
                          0.0,
                          0.0,
                          0.0,
                          24))

