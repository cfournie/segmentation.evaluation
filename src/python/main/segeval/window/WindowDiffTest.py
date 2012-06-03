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
                         (Decimal('0.3346808778477464646756666835'),
                          Decimal('0.1548359646350644285479295987'),
                          Decimal('0.02397417594447092239596242763'),
                          Decimal('0.03160575893229410229605643339')))
        self.assertEqual(pairwise_window_diff(KAZANTSEVA2012_G5,
                                              lamprier_et_al_2007_fix=True),
                         (Decimal('0.3132488451884422284933124958'),
                          Decimal('0.1504970340183621608256398094'),
                          Decimal('0.02264935724832405748451673388'),
                          Decimal('0.03072007842893909445584931717')))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise WindowDiff on Group 2 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_window_diff(KAZANTSEVA2012_G2,
                                              lamprier_et_al_2007_fix=False),
                         (Decimal('0.2320175115879447163831997425'),
                          Decimal('0.1120117646913460670148287930'),
                          Decimal('0.01254663542926948147954575889'),
                          Decimal('0.01538599916689114871263558635')))
        self.assertEqual(pairwise_window_diff(KAZANTSEVA2012_G2,
                                              lamprier_et_al_2007_fix=True),
                         (Decimal('0.2177394026283560619148130360'),
                          Decimal('0.1025027049723129189687548044'),
                          Decimal('0.01050680452664102360225293032'),
                          Decimal('0.01407982936126299309751920047')))
    
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
                          0.0))
        self.assertEqual(pairwise_window_diff(LARGE_DISAGREEMENT,
                                              lamprier_et_al_2007_fix=True),
                          (Decimal('0.8738537684261691328366719325'),
                           Decimal('0.09697786067530433386741553343'),
                           Decimal('0.009404705461158738750410907665'),
                           Decimal('0.04848893033765216693370776672')))
    
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
                          0.0))
        self.assertEqual(pairwise_window_diff(LARGE_DISAGREEMENT,
                                              lamprier_et_al_2007_fix=True),
                         (Decimal('0.8738537684261691328366719325'),
                          Decimal('0.09697786067530433386741553343'),
                          Decimal('0.009404705461158738750410907665'),
                          Decimal('0.04848893033765216693370776672')))

