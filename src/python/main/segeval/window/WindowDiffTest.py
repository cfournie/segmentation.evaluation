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
from ..Utils import AlmostTestCase


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
        self.assertAlmostEqual(window_diff(a,b),
                         Decimal('0.3636363636363636363636363636'))
        self.assertAlmostEqual(window_diff(b,a),
                         Decimal('0.8333333333333333333333333333'))

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 0.833
        erroneous windows.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertAlmostEqual(window_diff(a,b),
                         Decimal('0.9090909090909090909090909091'))
        self.assertAlmostEqual(window_diff(b,a),
                         Decimal('0.75'))

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.assertAlmostEqual(window_diff(a,b), Decimal('0.83333333333333333'))
        self.assertAlmostEqual(window_diff(b,a), Decimal('0.91666666666666666'))

    def test_translated_boundary(self):
        '''
        Test mis-alignment.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertAlmostEqual(window_diff(a,b), # k = 2
                               Decimal(2.0/11.0))
        self.assertAlmostEqual(window_diff(b,a),
                               Decimal(2.0/11.0))
    
    def test_extra_boundary(self):
        '''
        Test extra boundary.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertAlmostEqual(window_diff(a,b),
                               Decimal(2.0/11.0))
        self.assertAlmostEqual(window_diff(b,a),
                               Decimal(2.0/11.0))
    
    def test_full_miss_and_misaligned(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        0.25. 
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertAlmostEqual(window_diff(a,b),
                         Decimal('0.2727272727272727272727272727'))
        self.assertAlmostEqual(window_diff(b,a),
                         Decimal('0.2727272727272727272727272727'))
    
    def test_fn_vs_fp(self):
        '''
        Test the difference between FP and FN.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertAlmostEqual(window_diff(a,b),
                         Decimal('0.1818181818181818181818181818'))
        self.assertAlmostEqual(window_diff(b,a),
                         Decimal('0.1818181818181818181818181818'))
        a = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertAlmostEqual(window_diff(a,b),
                         Decimal('0.1818181818181818181818181818'))
        self.assertAlmostEqual(window_diff(b,a),
                         Decimal('0.1818181818181818181818181818'))
    
    def test_scaiano_paper_b(self):
        '''
        Test paper example A vs B
        '''
        reference = [6,6]
        hyp_b = [12]
        # Test normal
        actual = window_diff(hyp_b, reference, convert_from_masses=True,
                             lamprier_et_al_2007_fix=False)
        self.assertAlmostEqual(3.0/9.0, float(actual))
        # Test fix
        actual = window_diff(hyp_b, reference, convert_from_masses=True,
                             lamprier_et_al_2007_fix=True)
        self.assertAlmostEqual(3.0/9.0, float(actual))
    
    def test_scaiano_paper_c(self):
        '''
        Test paper example A vs C
        '''
        reference = [6,6]
        hyp_b = [5,7]
        # Test normal
        actual = window_diff(hyp_b, reference, convert_from_masses=True,
                             lamprier_et_al_2007_fix=False)
        self.assertAlmostEquals(2.0/9.0, float(actual))
        # Test fix
        actual = window_diff(hyp_b, reference, convert_from_masses=True,
                             lamprier_et_al_2007_fix=True)
        self.assertAlmostEquals(2.0/9.0, float(actual))
    
    def test_scaiano_paper_d(self):
        '''
        Test paper example A vs D
        '''
        reference = [6,6]
        hyp_b = [1,5,6]
        # Test normal
        actual = window_diff(hyp_b, reference, convert_from_masses=True,
                             lamprier_et_al_2007_fix=False)
        self.assertAlmostEquals(1.0/9.0, float(actual))
        # Test fix
        actual = window_diff(hyp_b, reference, convert_from_masses=True,
                             lamprier_et_al_2007_fix=True)
        self.assertAlmostEquals(3.0/9.0, float(actual))
    
    def test_scaiano_paper_e(self):
        '''
        Test paper example A vs E
        '''
        reference = [6,6]
        hyp_b = [5,1,1,5]
        # Test normal
        actual = window_diff(hyp_b, reference, convert_from_masses=True,
                             lamprier_et_al_2007_fix=False)
        self.assertAlmostEquals(5.0/9.0, float(actual))
        # Test fix
        actual = window_diff(hyp_b, reference, convert_from_masses=True,
                             lamprier_et_al_2007_fix=True)
        self.assertAlmostEquals(5.0/9.0, float(actual))


class TestPairwiseWindowDiff(AlmostTestCase):
    # pylint: disable=R0904,E1101,W0232
    '''
    Test pairwise WindowDiff.
    '''
    
    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise WindowDiff on Group 5 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertAlmostEquals(pairwise_window_diff(KAZANTSEVA2012_G5,
                                              lamprier_et_al_2007_fix=False),
                         (Decimal('0.39074292557364606400383060'),
                          Decimal('0.1532459549229588475788075613'),
                          Decimal('0.02348432270024953505176294415'),
                          Decimal('0.02211914833174788657143879197'),
                          48)

)
        self.assertAlmostEquals(pairwise_window_diff(KAZANTSEVA2012_G5,
                                              lamprier_et_al_2007_fix=True),
                         (Decimal('0.5050519674147423890139467544'),
                          Decimal('0.2083536565181746643262726936'),
                          Decimal('0.04341124618449350778640836788'),
                          Decimal('0.03007325991935274181082342604'),
                          48)
)
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise WindowDiff on Group 2 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertAlmostEquals(pairwise_window_diff(KAZANTSEVA2012_G2,
                                              lamprier_et_al_2007_fix=False),
                         (Decimal('0.3127768830224693'),
                          Decimal('0.1476337375818111'),
                          Decimal('0.02179572047237506'),
                          Decimal('0.013477054720392689'),
                          120))
        self.assertAlmostEquals(pairwise_window_diff(KAZANTSEVA2012_G2,
                                              lamprier_et_al_2007_fix=True),
                         (Decimal('0.3510380674724445543899241432'),
                          Decimal('0.1660721071574854077325131729'),
                          Decimal('0.02757994477572731599258676371'),
                          Decimal('0.01516023987709498502329933401'),
                          120))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise WindowDiff on a theoretical dataset
        containing large disagreement.
        '''
        self.assertAlmostEquals(pairwise_window_diff(LARGE_DISAGREEMENT,
                                              lamprier_et_al_2007_fix=False),
                        (Decimal('0.8459729214944234199689912141'),
                         Decimal('0.1476397871849968959886430556'),
                         Decimal('0.02179750676003117367307268181'),
                         Decimal('0.05219854734572502170997494041'),
                         8))
                         
        self.assertAlmostEquals(pairwise_window_diff(LARGE_DISAGREEMENT,
                                              lamprier_et_al_2007_fix=True),
                          (1.0,
                           0.0,
                           0.0,
                           0.0,
                           8))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise WindowDiff on a theoretical dataset
        containing complete agreement.
        '''
        self.assertAlmostEquals(pairwise_window_diff(COMPLETE_AGREEMENT,
                                                lamprier_et_al_2007_fix=False),
                         (0.0,
                          0.0,
                          0.0,
                          0.0,
                          48))
        self.assertAlmostEquals(pairwise_window_diff(COMPLETE_AGREEMENT,
                                                lamprier_et_al_2007_fix=True),
                          (0.0,
                           0.0,
                           0.0,
                           0.0,
                           48))

