'''
Tests the WinPR evaluation metric.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2011-2012, Chris Fournier
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#       
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================
import unittest
from decimal import Decimal
from .WinPR import pairwise_win_pr, win_pr, win_pr_f
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT


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
                         {'fp': 0, 'tn': 22, 'fn': 0, 'tp': 4} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('1') )

    def test_no_boundaries(self):
        '''
        Test whether no segments versus some segments produce 0.6667.
        '''
        segs_a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        segs_b = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 12, 'tn': 67, 'fn': 0, 'tp': 12} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0.6666666666666666666666666667') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 0, 'tn': 22, 'fn': 2, 'tp': 2} )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0.6666666666666666666666666667') )

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 0.4444.
        '''
        segs_a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        segs_b = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                          {'fp': 0, 'tn': 12, 'fn': 10, 'tp': 4} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0.4444444444444444444444444444') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 10, 'tn': 12, 'fn': 0, 'tp': 4} )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0.4444444444444444444444444444') )

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 0.25.
        '''
        segs_a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        segs_b = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 0, 'tn': 12, 'fn': 12, 'tp': 2} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0.25') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 72, 'tn': 7, 'fn': 0, 'tp': 12} )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0.25') )

    def test_translated_boundary(self):
        '''
        Test whether 2/3 total segments participate in mis-alignment produces
        0.75.
        '''
        segs_a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        segs_b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 1, 'tn': 21, 'fn': 1, 'tp': 3} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0.75') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 1, 'tn': 21, 'fn': 1, 'tp': 3} )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0.75') )
    
    def test_extra_boundary(self):
        '''
        Test whether 1/3 segments that are non-existent produces 0.889.
        '''
        segs_a = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        segs_b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 1, 'tn': 21, 'fn': 0, 'tp': 4} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0.8888888888888888888888888889') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 0, 'tn': 21, 'fn': 1, 'tp': 4} )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0.8888888888888888888888888889') )
    
    def test_full_miss_and_misaligned(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        '0.6667. 
        '''
        segs_a = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        segs_b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b, convert_from_masses=False),
                         {'fp': 2, 'tn': 20, 'fn': 1, 'tp': 3} )
        self.assertEqual(win_pr_f(segs_a, segs_b, convert_from_masses=False),
                         Decimal('0.6666666666666666666666666667') )
        self.assertEqual(win_pr(segs_b, segs_a, convert_from_masses=False),
                         {'fp': 1, 'tn': 20, 'fn': 2, 'tp': 3}  )
        self.assertEqual(win_pr_f(segs_b, segs_a, convert_from_masses=False),
                         Decimal('0.6666666666666666666666666667') )
    

class TestPairwiseWinPR(unittest.TestCase):
    # pylint: disable=R0904
    '''
    Test pairwise WinPR.
    '''
    
    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise percentage on Group 5 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_win_pr(KAZANTSEVA2012_G5, ),
                         (Decimal('0.5868367743367743367743367746'),
                          Decimal('0.1198711646320202975515773835'),
                          Decimal('0.01436909611023691387771751852'),
                          Decimal('0.02446859901846728286113130960'),
                          24))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise percentage on Group 2 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_win_pr(KAZANTSEVA2012_G2),
                         (Decimal('0.6980631577775708883529586183'),
                          Decimal('0.1121769660131793859585435576'),
                          Decimal('0.01258367170392200306131853235'),
                          Decimal('0.01448198403990397250690864769'),
                          60))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing large disagreement.
        '''
        self.assertEqual(pairwise_win_pr(LARGE_DISAGREEMENT),
                         (Decimal('0.2573671497584541062801932368'),
                          Decimal('0.1535469743040559128336768347'),
                          Decimal('0.02357667331793040677728768466'),
                          Decimal('0.07677348715202795641683841735'),
                          4))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing complete agreement.
        '''
        self.assertEqual(pairwise_win_pr(COMPLETE_AGREEMENT),
                         (1.0,
                          0.0,
                          0.0,
                          0.0,
                          24))

