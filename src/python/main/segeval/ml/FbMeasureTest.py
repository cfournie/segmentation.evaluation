'''
Tests the WindowDiff evaluation metric.

@author: Chris Fournier
@contact: chris.m.fournier@gmail.com
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
from .FbMeasure import f_b_measure, pairwise_f_b_measure
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT
from .. import convert_segments_to_masses


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
        a = convert_segments_to_masses([1,1,1,1,1,2,2,2,3,3,3,3,3])
        b = convert_segments_to_masses([1,1,1,1,1,2,2,2,3,3,3,3,3])
        self.assertEqual(f_b_measure(a, b), 1.0)

    def test_no_boundaries(self):
        '''
        Test whether no segments versus some segments produce 0.0.
        '''
        # pylint: disable=C0324,C0103
        a = convert_segments_to_masses([1,1,1,1,1,1,1,1,1,1,1,1,1])
        b = convert_segments_to_masses([1,1,1,1,2,2,2,2,3,3,3,3,3])
        self.assertEqual(f_b_measure(a,b), 0)
        self.assertEqual(f_b_measure(b,a), 0)

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 2/12, or 0.167.
        '''
        # pylint: disable=C0324,C0103
        a = convert_segments_to_masses([1,2,3,4,5,6,7,8,9,10,11,12,13])
        b = convert_segments_to_masses([1,1,1,1,2,2,2,2,3,3,3,3,3])
        self.assertEqual(f_b_measure(a,b),
                         Decimal('0.2857142857142857142857142857'))
        self.assertEqual(f_b_measure(b,a),
                         Decimal('0.2857142857142857142857142857'))

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 0.0.
        '''
        # pylint: disable=C0324,C0103
        a = convert_segments_to_masses([1,2,3,4,5,6,7,8,9,10,11,12,13])
        b = convert_segments_to_masses([1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.assertEqual(f_b_measure(a,b), 0)
        self.assertEqual(f_b_measure(b,a), 0)

    def test_translated_boundary(self):
        '''
        Test whether 2/3 total segments participate in  mis-alignment produces
        0.33.
        '''
        # pylint: disable=C0324,C0103
        a = convert_segments_to_masses([1,1,1,1,1,2,2,2,3,3,3,3,3])
        b = convert_segments_to_masses([1,1,1,1,2,2,2,2,3,3,3,3,3])
        self.assertEqual(f_b_measure(a,b),
                         Decimal('0.5'))
        self.assertEqual(f_b_measure(b,a),
                         Decimal('0.5'))
    
    def test_extra_boundary(self):
        '''
        Test whether 1/3 segments that are non-existent produces 0.66.
        '''
        # pylint: disable=C0324,C0103
        a = convert_segments_to_masses([1,1,1,1,1,2,2,2,3,3,3,3,3])
        b = convert_segments_to_masses([1,1,1,1,1,2,3,3,4,4,4,4,4])
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
        a = convert_segments_to_masses([1,1,1,1,2,2,2,2,3,3,3,3,3])
        b = convert_segments_to_masses([1,1,1,1,1,2,3,3,4,4,4,4,4])
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
        collected in Kazantseva (2012).
        '''
        self.assertEqual(pairwise_f_b_measure(KAZANTSEVA2012_G5),
                         (0.24415868122125425,
                          0.23051692300014356,
                          0.053138051789454119))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise percentage on Group 2 from the dataset
        collected in Kazantseva (2012).
        '''
        self.assertEqual(pairwise_f_b_measure(KAZANTSEVA2012_G2),
                         (0.47774198511040616,
                          0.20909436633848039,
                          0.043720454034490645))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing large disagreement.
        '''
        self.assertEqual(pairwise_f_b_measure(LARGE_DISAGREEMENT),
                         (0.0,
                          0.0,
                          0.0))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing complete agreement.
        '''
        self.assertEqual(pairwise_f_b_measure(COMPLETE_AGREEMENT),
                         (1.0,
                          0.0,
                          0.0))

