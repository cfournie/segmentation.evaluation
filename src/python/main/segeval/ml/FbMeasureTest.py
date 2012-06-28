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
from .FbMeasure import f_b_measure, pairwise_ml_measure, \
    pairwise_ml_measure_micro, ml_fmeasure
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT
from .. import convert_positions_to_masses


class TestFbMeasure(unittest.TestCase):
    '''
    Test segmentation F-measure.
    '''
    # pylint: disable=R0904

    def test_identical(self):
        '''
        Test whether identical segmentations produce 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = convert_positions_to_masses([1,1,1,1,1,2,2,2,3,3,3,3,3])
        b = convert_positions_to_masses([1,1,1,1,1,2,2,2,3,3,3,3,3])
        self.assertEqual(f_b_measure(a, b), 1.0)

    def test_no_boundaries(self):
        '''
        Test whether no segments versus some segments produce 0.0.
        '''
        # pylint: disable=C0324,C0103
        a = convert_positions_to_masses([1,1,1,1,1,1,1,1,1,1,1,1,1])
        b = convert_positions_to_masses([1,1,1,1,2,2,2,2,3,3,3,3,3])
        self.assertEqual(f_b_measure(a,b), 0)
        self.assertEqual(f_b_measure(b,a), 0)

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 2/12, or 0.167.
        '''
        # pylint: disable=C0324,C0103
        a = convert_positions_to_masses([1,2,3,4,5,6,7,8,9,10,11,12,13])
        b = convert_positions_to_masses([1,1,1,1,2,2,2,2,3,3,3,3,3])
        self.assertEqual(f_b_measure(a,b),
                         Decimal('0.2857142857142857142857142857'))
        self.assertEqual(f_b_measure(b,a),
                         Decimal('0.2857142857142857142857142857'))

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 0.0.
        '''
        # pylint: disable=C0324,C0103
        a = convert_positions_to_masses([1,2,3,4,5,6,7,8,9,10,11,12,13])
        b = convert_positions_to_masses([1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.assertEqual(f_b_measure(a,b), 0)
        self.assertEqual(f_b_measure(b,a), 0)

    def test_translated_boundary(self):
        '''
        Test whether 2/3 total segments participate in mis-alignment produces
        0.5.
        '''
        # pylint: disable=C0324,C0103
        a = convert_positions_to_masses([1,1,1,1,1,2,2,2,3,3,3,3,3])
        b = convert_positions_to_masses([1,1,1,1,2,2,2,2,3,3,3,3,3])
        self.assertEqual(f_b_measure(a,b),
                         Decimal('0.5'))
        self.assertEqual(f_b_measure(b,a),
                         Decimal('0.5'))
    
    def test_extra_boundary(self):
        '''
        Test whether 1/3 segments that are non-existent produces 0.8.
        '''
        # pylint: disable=C0324,C0103
        a = convert_positions_to_masses([1,1,1,1,1,2,2,2,3,3,3,3,3])
        b = convert_positions_to_masses([1,1,1,1,1,2,3,3,4,4,4,4,4])
        self.assertEqual(f_b_measure(a,b),
                         Decimal('0.8'))
        self.assertEqual(f_b_measure(b,a),
                         Decimal('0.8'))
    
    def test_full_miss_and_misaligned(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        0.25. 
        '''
        # pylint: disable=C0324,C0103
        a = convert_positions_to_masses([1,1,1,1,2,2,2,2,3,3,3,3,3])
        b = convert_positions_to_masses([1,1,1,1,1,2,3,3,4,4,4,4,4])
        self.assertEqual(f_b_measure(a,b), Decimal('0.4'))
        self.assertEqual(f_b_measure(b,a), Decimal('0.4'))


class TestPairwiseFbMeasure(unittest.TestCase):
    # pylint: disable=R0904
    '''
    Test pairwise F_b_measure.
    '''

    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise percentage on Group 5 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_ml_measure(KAZANTSEVA2012_G5, f_b_measure),
                         (Decimal('0.2441586812212541867438777319'),
                          Decimal('0.2305169230001435997031211476'),
                          Decimal('0.05313805178945413332341442152'),
                          Decimal('0.03327225188672428552085603179'),
                          48))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise percentage on Group 2 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_ml_measure(KAZANTSEVA2012_G2, f_b_measure),
                         (Decimal('0.477741985110406163037741985'),
                          Decimal('0.2090943663384804017117580493'),
                          Decimal('0.04372045403449064611325971045'),
                          Decimal('0.01908761684847243358481821495'),
                          120))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing large disagreement.
        '''
        self.assertEqual(pairwise_ml_measure(LARGE_DISAGREEMENT, f_b_measure),
                         (0.0,
                          0.0,
                          0.0,
                          0.0,
                          8))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing complete agreement.
        '''
        self.assertEqual(pairwise_ml_measure(COMPLETE_AGREEMENT, f_b_measure),
                         (1.0,
                          0.0,
                          0.0,
                          0.0,
                          48))


class TestMicroPairwiseFbMeasure(unittest.TestCase):
    # pylint: disable=R0904
    '''
    Test pairwise F_b_measure.
    '''

    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise percentage on Group 5 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_ml_measure_micro(KAZANTSEVA2012_G5,
                                                   ml_fmeasure),
                         Decimal('0.3163841807909604519774011299'))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise percentage on Group 2 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_ml_measure_micro(KAZANTSEVA2012_G2,
                                                   ml_fmeasure),
                         Decimal('0.4776119402985074626865671642'))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing large disagreement.
        '''
        self.assertEqual(pairwise_ml_measure_micro(LARGE_DISAGREEMENT,
                                                   ml_fmeasure),
                         0.0)
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing complete agreement.
        '''
        self.assertEqual(pairwise_ml_measure_micro(COMPLETE_AGREEMENT,
                                                   ml_fmeasure),
                         1.0)

