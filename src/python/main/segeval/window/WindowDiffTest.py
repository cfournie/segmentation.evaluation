'''
Tests the WindowDiff evaluation metric.

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
from .WindowDiff import window_diff, pairwise_window_diff
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT


class TestWindowDiff(unittest.TestCase):
    '''
    Test WindowDiff.
    '''
    # pylint: disable=R0904,C0324

    def test_identical(self):
        '''
        Test whether identical segmentations produce 0.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertEqual(window_diff(a,b), 0.0)

    def test_no_boundaries(self):
        '''
        Test whether no segments versus some segments produce 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.1666666666666666666666666667'))
        self.assertEqual(window_diff(b,a),
                         Decimal('1.0'))

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 0.833
        erroneous windows.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.8333333333333333333333333333'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.8333333333333333333333333333'))

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.assertEqual(window_diff(a,b), 1.0)
        self.assertEqual(window_diff(b,a), 1.0)

    def test_translated_boundary(self):
        '''
        Test whether 2/3 total segments participate in mis-alignment produces
        0.167.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.1666666666666666666666666667'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.1666666666666666666666666667'))
    
    def test_extra_boundary(self):
        '''
        Test whether 1/3 segments that are non-existent produces 0.083.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.08333333333333333333333333333'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.08333333333333333333333333333'))
    
    def test_full_miss_and_misaligned(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        0.25. 
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.25'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.25'))
    
    def test_fn_vs_fp(self):
        '''
        Test the difference between FP and FN.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.08333333333333333333333333333'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.08333333333333333333333333333'))
        a = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.08333333333333333333333333333'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.08333333333333333333333333333'))


class TestPairwiseWindowDiff(unittest.TestCase):
    # pylint: disable=R0904
    '''
    Test pairwise WindowDiff.
    '''
        
    
    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise WindowDiff on Group 5 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_window_diff(KAZANTSEVA2012_G5,
                                              lamprier_et_al_2007_fix=False),
                         (Decimal('0.3604506237259865251208907681'),
                          Decimal('0.1674103189012695088955568781'),
                          Decimal('0.02802621487462475498810473917'),
                          Decimal('0.02416359817069226127768032185'),
                          48))
        self.assertEqual(pairwise_window_diff(KAZANTSEVA2012_G5,
                                              lamprier_et_al_2007_fix=True),
                         (Decimal('0.3389327650117214732278073269'),
                          Decimal('0.1644218164415795205498766706'),
                          Decimal('0.02703453372194846954943255448'),
                          Decimal('0.02373224499579829290476994224'),
                          48))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise WindowDiff on Group 2 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_window_diff(KAZANTSEVA2012_G2,
                                              lamprier_et_al_2007_fix=False),
                         (Decimal('0.2545512423455600226641754512'),
                          Decimal('0.1227764444488944596833784807'),
                          Decimal('0.01507405531151246718395938746'),
                          Decimal('0.01120790469248990475787117305'),
                          120))
        self.assertEqual(pairwise_window_diff(KAZANTSEVA2012_G2,
                                              lamprier_et_al_2007_fix=True),
                         (Decimal('0.2282101219734164495559781365'),
                          Decimal('0.09824964933538713480770055133'),
                          Decimal('0.009652993594526537660429053525'),
                          Decimal('0.008968924867993997594174187067'),
                          120))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise WindowDiff on a theoretical dataset
        containing large disagreement.
        '''
        self.assertEqual(pairwise_window_diff(LARGE_DISAGREEMENT,
                                              lamprier_et_al_2007_fix=False),
                         (1.0,
                          0.0,
                          0.0,
                          0.0,
                          8))
        self.assertEqual(pairwise_window_diff(LARGE_DISAGREEMENT,
                                              lamprier_et_al_2007_fix=True),
                          (Decimal('0.8583107329225146711972779546'),
                           Decimal('0.1040894435363239488284336823'),
                           Decimal('0.01083461225570157148986770720'),
                           Decimal('0.03680117568723445601862258284'),
                           8))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise WindowDiff on a theoretical dataset
        containing complete agreement.
        '''
        self.assertEqual(pairwise_window_diff(COMPLETE_AGREEMENT,
                                              lamprier_et_al_2007_fix=False),
                         (0.0,
                          0.0,
                          0.0,
                          0.0,
                          48))
        self.assertEqual(pairwise_window_diff(LARGE_DISAGREEMENT,
                                              lamprier_et_al_2007_fix=True),
                          (Decimal('0.8583107329225146711972779546'),
                           Decimal('0.1040894435363239488284336823'),
                           Decimal('0.01083461225570157148986770720'),
                           Decimal('0.03680117568723445601862258284'),
                           8))

