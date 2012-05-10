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
from .Percentage import percentage, pairwise_percentage, find_seg_positions
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT
from .. import convert_segment_pos_to_masses



class TestPercentage(unittest.TestCase):
    '''
    Test segmentation percentage.
    '''
    # pylint: disable=R0904

    def test_identical(self):
        '''
        Test whether identical segmentations produce 1.0.
        '''
        # pylint: disable=C0324
        segs_a = convert_segment_pos_to_masses(
                                        [1,1,1,1,1,2,2,2,3,3,3,3,3])
        segs_b = convert_segment_pos_to_masses(
                                        [1,1,1,1,1,2,2,2,3,3,3,3,3])
        self.assertEqual(percentage(segs_a, segs_b),1.0)

    def test_no_boundaries(self):
        '''
        Test whether no segments versus some segments produce 0.0.
        '''
        # pylint: disable=C0324
        segs_a = convert_segment_pos_to_masses(
                                        [1,1,1,1,1,1,1,1,1,1,1,1,1])
        segs_b = convert_segment_pos_to_masses(
                                        [1,1,1,1,2,2,2,2,3,3,3,3,3])
        self.assertEqual(percentage(segs_a, segs_b),0)
        self.assertEqual(percentage(segs_b, segs_a),0)

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 2/12, or 0.167.
        '''
        # pylint: disable=C0324
        segs_a = convert_segment_pos_to_masses(
                                    [1,2,3,4,5,6,7,8,9,10,11,12,13])
        segs_b = convert_segment_pos_to_masses(
                                    [1,1,1,1,2,2,2,2,3,3,3,3,3])
        self.assertEqual(percentage(segs_a, segs_b),
                         Decimal('0.1666666666666666666666666667'))
        self.assertEqual(percentage(segs_b, segs_a),
                         Decimal('0.1666666666666666666666666667'))

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 0.0.
        '''
        # pylint: disable=C0324
        segs_a = convert_segment_pos_to_masses(
                                    [1,2,3,4,5,6,7,8,9,10,11,12,13])
        segs_b = convert_segment_pos_to_masses(
                                    [1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.assertEqual(percentage(segs_a, segs_b),0)
        self.assertEqual(percentage(segs_b, segs_a),0)

    def test_translated_boundary(self):
        '''
        Test whether 2/3 total segments participate in  mis-alignment produces
        0.33.
        '''
        # pylint: disable=C0324
        segs_a = convert_segment_pos_to_masses(
                                        [1,1,1,1,1,2,2,2,3,3,3,3,3])
        segs_b = convert_segment_pos_to_masses(
                                        [1,1,1,1,2,2,2,2,3,3,3,3,3])
        self.assertEqual(percentage(segs_a, segs_b),
                         Decimal('0.3333333333333333333333333333'))
        self.assertEqual(percentage(segs_b, segs_a),
                         Decimal('0.3333333333333333333333333333'))
    
    def test_extra_boundary(self):
        '''
        Test whether 1/3 segments that are non-existent produces 0.66.
        '''
        # pylint: disable=C0324
        segs_a = convert_segment_pos_to_masses(
                                        [1,1,1,1,1,2,2,2,3,3,3,3,3])
        segs_b = convert_segment_pos_to_masses(
                                        [1,1,1,1,1,2,3,3,4,4,4,4,4])
        self.assertEqual(percentage(segs_a, segs_b),
                         Decimal('0.6666666666666666666666666667'))
        self.assertEqual(percentage(segs_b, segs_a),
                         Decimal('0.6666666666666666666666666667'))
    
    def test_full_miss_and_misaligned(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        0.25. 
        '''
        # pylint: disable=C0324
        segs_a = convert_segment_pos_to_masses(
                                        [1,1,1,1,2,2,2,2,3,3,3,3,3])
        segs_b = convert_segment_pos_to_masses(
                                        [1,1,1,1,1,2,3,3,4,4,4,4,4])
        self.assertEqual(percentage(segs_a, segs_b), Decimal('0.25'))
        self.assertEqual(percentage(segs_b, segs_a), Decimal('0.25'))


class TestPairwisePercentage(unittest.TestCase):
    # pylint: disable=R0904
    '''
    Test permuted pairwise percentage.
    '''
    
    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise percentage on Group 5 from the dataset
        collected in Kazantseva (2012).
        '''
        self.assertEqual(pairwise_percentage(KAZANTSEVA2012_G5),
                         (0.16212636352438983,
                          0.17884097818862088,
                          0.031984095479462765))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise percentage on Group 2 from the dataset
        collected in Kazantseva (2012).
        '''
        self.assertEqual(pairwise_percentage(KAZANTSEVA2012_G2),
                         (0.33980878326466551,
                          0.1948481072924021,
                          0.037965784915431441))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing large disagreement.
        '''
        self.assertEqual(pairwise_percentage(LARGE_DISAGREEMENT),
                         (0.0,
                          0.0,
                          0.0))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise percentage on a theoretical dataset
        containing complete agreement.
        '''
        self.assertEqual(pairwise_percentage(COMPLETE_AGREEMENT),
                         (1.0,
                          0.0,
                          0.0))


class TestPercentageUtils(unittest.TestCase):
    # pylint: disable=R0904
    '''
    Test utility functions used to calculate percentage.
    '''
    
    def test_find_seg_positions(self):
        '''
        Test segmentation position frequency counting.
        '''
        # pylint: disable=C0324
        seg_positions = find_seg_positions([[1,2,3,3,2,1],
                                            [1,2,2,4,2,1]])
        self.assertEqual(seg_positions, { 1: 2,
                                          3: 2,
                                          5: 1,
                                          6: 1,
                                          9: 2,
                                         11: 2})
