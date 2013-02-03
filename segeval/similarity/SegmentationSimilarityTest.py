'''
Tests the similarity evaluation metric functions.

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
from .SegmentationSimilarity import similarity, pairwise_similarity, \
    pairwise_similarity_micro
from .. import SegmentationMetricError
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT


class TestSegmentationSimilarity(unittest.TestCase):
    '''
    Tests the Segmentation Similarity metric.
    '''
    # pylint: disable=R0904,C0324
    
    N                    = 2
    WEIGHT               = (1,1)
    SCALE_TRANSPOSITIONS = True
    
    REF_A = [1,2,2,4,2,1]
    REF_B = [1,2,3,3,2,1]
    REF_C = [2,1,3,3,2,1]
    REF_D = [2,1,6,2,1]
    REF_E = [3,6,2,1]
    REF_F = [2,2,5,2,1]
    
    NO_REF_SEG  = [12]
    ALL_REF_SEG = [1,1,1,1,1,1,1,1,1,1,1,1]
    
    TOTAL_REFS_MASS = 12
    ALL_REFS = [REF_A,REF_B,REF_C,REF_D,REF_E,REF_F,NO_REF_SEG,ALL_REF_SEG]
    
    REF_TRANS_A = [2,2,2]
    REF_TRANS_B = [1,2,3]
    REF_TRANS_C = [3,2,1]
    REF_TRANS_D = [2,2,2]
    
    SKIP = False
    
    
    def test_verify_total_mass(self):
        '''
        Tests to ensure that all of the cases of the same hypothetical problem
        sum to the same mass.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        # Check for TOTAL_MASS
        for ref in TestSegmentationSimilarity.ALL_REFS:
            self.assertTrue(TestSegmentationSimilarity.TOTAL_REFS_MASS,
                            sum(ref))
    
    
    def test_empty_set(self):
        '''
        In this case the method is expected to produce a similarity of 1.0.
        '''
        # pylint: disable=C0103
        if TestSegmentationSimilarity.SKIP:
            return
        # Two empty sets
        sim = similarity([], [],
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, 1.0)
        u,t = similarity([], [],
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS,
                         return_parts=True)
        self.assertEqual((u,t), (0,0))
        
    
    def test_exception_on_mismatch(self):
        '''
        Test that mismatched mass totals raise an exception.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        self.assertRaises(SegmentationMetricError, similarity, [1], [])
        self.assertRaises(SegmentationMetricError, similarity, [], [1])
        self.assertRaises(SegmentationMetricError, similarity,
                          TestSegmentationSimilarity.REF_A,
                          [1] + TestSegmentationSimilarity.REF_A)
    
    
    def test_exception_on_zero(self):
        '''
        Test that otherwise conforming masses that contain zeros raise an
        exception.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        self.assertRaises(SegmentationMetricError, similarity, [0], [0])
        self.assertRaises(SegmentationMetricError, similarity,
                          [1,2,3],
                          [1,0,5])
        self.assertRaises(SegmentationMetricError, similarity,
                          [1,0,5],
                          [1,2,3])
    
    
    def test_reflexivity_and_full_match(self):
        '''
        Test the reflexive property, and the value.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        for ref in TestSegmentationSimilarity.ALL_REFS:
            self.assertEqual(similarity(ref,ref), similarity(ref,ref))
            self.assertEqual(similarity(ref,ref), 1.0)
        sim = similarity(TestSegmentationSimilarity.NO_REF_SEG,
                         TestSegmentationSimilarity.NO_REF_SEG,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, 1.0)
        sim = similarity(TestSegmentationSimilarity.ALL_REF_SEG,
                         TestSegmentationSimilarity.ALL_REF_SEG,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, 1.0)
    
    
    def test_symmetry_property(self):
        '''
        Test the symmetry property.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        refs = TestSegmentationSimilarity.ALL_REFS
        for i,ref in enumerate(refs):
            not_refs = [ref for j, ref in enumerate(refs) if j != i]
            for not_ref in not_refs:
                self.assertEqual(
                    similarity(ref,not_ref,
                               TestSegmentationSimilarity.N,
                               TestSegmentationSimilarity.WEIGHT,
                               TestSegmentationSimilarity.SCALE_TRANSPOSITIONS),
                    similarity(not_ref,ref,
                               TestSegmentationSimilarity.N,
                               TestSegmentationSimilarity.WEIGHT,
                               TestSegmentationSimilarity.SCALE_TRANSPOSITIONS))
    
    
    def test_with_no_segmentation(self):
        '''
        Test cases compared to a single segment (i.e. no segmentation).
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        sim = similarity(TestSegmentationSimilarity.REF_A,
                         TestSegmentationSimilarity.NO_REF_SEG,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.5454545454545454545454545455'))
        sim = similarity(TestSegmentationSimilarity.REF_B,
                         TestSegmentationSimilarity.NO_REF_SEG,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.5454545454545454545454545455'))
        sim = similarity(TestSegmentationSimilarity.REF_C,
                         TestSegmentationSimilarity.NO_REF_SEG,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.5454545454545454545454545455'))
        sim = similarity(TestSegmentationSimilarity.REF_E,
                         TestSegmentationSimilarity.NO_REF_SEG,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.7272727272727272727272727273'))
    
     
    def test_with_maximal_segmentation(self):
        '''
        Test cases compared to a fully segmented case (each segment is one unit
        long).
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        sim = similarity(TestSegmentationSimilarity.REF_A,
                         TestSegmentationSimilarity.ALL_REF_SEG,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.4545454545454545454545454545'))
        sim = similarity(TestSegmentationSimilarity.REF_D,
                         TestSegmentationSimilarity.ALL_REF_SEG,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.3636363636363636363636363636'))
        sim = similarity(TestSegmentationSimilarity.REF_E,
                         TestSegmentationSimilarity.ALL_REF_SEG,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.2727272727272727272727272727'))
    
    
    def test_maximal_and_no_segments(self):
        '''
        Test a case of one segment against a completely segmented case).
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        sim = similarity(TestSegmentationSimilarity.NO_REF_SEG,
                         TestSegmentationSimilarity.ALL_REF_SEG,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, 0.0)
        sim = similarity([10],
                         [1,1,1,1,1,1,1,1,1,1],
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, 0.0)
    
    
    def test_simple_translation(self):
        '''
        Test a case where segment boundaries are shifted once in one direction.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        sim_ab = similarity(TestSegmentationSimilarity.REF_TRANS_A,
                            TestSegmentationSimilarity.REF_TRANS_B,
                            TestSegmentationSimilarity.N,
                            TestSegmentationSimilarity.WEIGHT,
                            TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        sim_cd = similarity(TestSegmentationSimilarity.REF_TRANS_C,
                            TestSegmentationSimilarity.REF_TRANS_D,
                            TestSegmentationSimilarity.N,
                            TestSegmentationSimilarity.WEIGHT,
                            TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim_ab, sim_cd)
        self.assertEqual(sim_ab, Decimal('0.6'))
    
    
    def test_erratic_translation(self):
        '''
        Test a case where segment boundaries are shifted erratically.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        # AB
        sim = similarity(TestSegmentationSimilarity.REF_A,
                         TestSegmentationSimilarity.REF_B,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.9090909090909090909090909091'))
        # AC
        sim = similarity(TestSegmentationSimilarity.REF_A,
                         TestSegmentationSimilarity.REF_C,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.8181818181818181818181818182'))
        # AD
        sim = similarity(TestSegmentationSimilarity.REF_A,
                         TestSegmentationSimilarity.REF_D,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.8181818181818181818181818182'))
    
    
    def test_differing_num_of_segments(self):
        '''
        Test a case where the number of segments differs.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        # AE
        sim = similarity(TestSegmentationSimilarity.REF_A,
                         TestSegmentationSimilarity.REF_E,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.8181818181818181818181818182'))
        # AF
        sim = similarity(TestSegmentationSimilarity.REF_A,
                         TestSegmentationSimilarity.REF_F,
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.7272727272727272727272727273'))
        # Whiteboard example
        sim = similarity([2,1,2,2], [4,2,1],
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.5'))


class TestSegmentationSimilarityFigures(unittest.TestCase):
    '''
    Tests the Segmentation Similarity metric figures.
    '''
    # pylint: disable=R0904,C0324
    
    def test_figure_walkthrough(self):
        '''
        Tests the case in the Figure in the paper's walkthrough.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        sim = similarity([1,2,2,3,3,1,2],
                         [1,2,1,2,6,2],
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.6923076923076923076923076923'))
    
    
    def test_figure_insert_delete(self):
        '''
        Tests the case in the paper's insertion/deletion Figure.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        sim = similarity([1,2,2,4,2,1],
                         [1,2,6,2,1],
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.9090909090909090909090909091'))
    
    
    def test_figure_complex_ins_del(self):
        '''
        Tests the case in the paper's complex insertion/deletion Figure.
        '''
        if TestSegmentationSimilarity.SKIP:
            return
        sim = similarity([1,1,3,1,2,2,1,1],
                         [2,1,4,2,1,2],
                         TestSegmentationSimilarity.N,
                         TestSegmentationSimilarity.WEIGHT,
                         TestSegmentationSimilarity.SCALE_TRANSPOSITIONS)
        self.assertEqual(sim, Decimal('0.4545454545454545454545454545'))
        
    
    def test_scaled_transposition(self):
        '''
        Tests the case in the Figure in the paper's walkthrough.
        '''
        #if TestSegmentationSimilarity.SKIP:
        #    return
        sim = similarity([1,4,4],
                         [1,2,6],
                         5,
                         TestSegmentationSimilarity.WEIGHT,
                         True)
        self.assertEqual(sim, Decimal('0.8125'))
        
    
    def test_figure_walkthrough_and_F(self):
        '''
        Tests the case in the Figure in the paper's walkthrough.
        '''
        # pylint: disable=C0103
        if TestSegmentationSimilarity.SKIP:
            return
        a   = [1,2,2,3,3,1,2]
        f_a = [sum(a)]#[1] * sum(a)
        b   = [1,2,1,2,6,2]
        f_b = [sum(a)]#[1] * sum(a)
        sim_ab_u = \
            similarity(a,
                       b,
                       TestSegmentationSimilarity.N,
                       TestSegmentationSimilarity.WEIGHT,
                       TestSegmentationSimilarity.SCALE_TRANSPOSITIONS,
                       return_parts=True)[0]
        sim_afb_u = \
            similarity(a,
                       f_b,
                       TestSegmentationSimilarity.N,
                       TestSegmentationSimilarity.WEIGHT,
                       TestSegmentationSimilarity.SCALE_TRANSPOSITIONS,
                       return_parts=True)[0]
        sim_fab_u = \
            similarity(f_a,
                       b,
                       TestSegmentationSimilarity.N,
                       TestSegmentationSimilarity.WEIGHT,
                       TestSegmentationSimilarity.SCALE_TRANSPOSITIONS,
                       return_parts=True)[0]
        self.assertEqual(sim_ab_u,  Decimal('9'))
        self.assertEqual(sim_afb_u, Decimal('7'))
        self.assertEqual(sim_fab_u, Decimal('8'))
        




class TestPairwiseS(unittest.TestCase):
    # pylint: disable=R0904
    '''
    Test permuted pairwise percentage.
    '''
    
    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise S on Group 5 from the dataset
        collected in Kazantseva (2012).
        '''
        self.assertEqual(pairwise_similarity(KAZANTSEVA2012_G5),
                         (Decimal('0.8160882473382473382473382471'),
                          Decimal('0.06720030843553828301879219481'),
                          Decimal('0.004515881453831477719001606533'),
                          Decimal('0.01371720551872640852180333777'),
                          24))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise S on Group 2 from the dataset
        collected in Kazantseva (2012).
        '''
        self.assertEqual(pairwise_similarity(KAZANTSEVA2012_G2),
                         (Decimal('0.8838086068830613118161256798'),
                          Decimal('0.04672823593290891559792690999'),
                          Decimal('0.002183528033401599953629233128'),
                          Decimal('0.006032589318860240953093878222'),
                          60))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise S on a theoretical dataset
        containing large disagreement.
        '''
        self.assertEqual(pairwise_similarity(LARGE_DISAGREEMENT),
                         (0.0,
                          0.0,
                          0.0,
                          0.0,
                          4))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise S on a theoretical dataset
        containing complete agreement.
        '''
        self.assertEqual(pairwise_similarity(COMPLETE_AGREEMENT),
                         (1.0,
                          0.0,
                          0.0,
                          0.0,
                          24))


class TestMicroPairwiseS(unittest.TestCase):
    # pylint: disable=R0904
    '''
    Test permuted pairwise S.
    '''
    
    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise S on Group 5 from the dataset
        collected in Kazantseva (2012).
        '''
        self.assertEqual(pairwise_similarity_micro(KAZANTSEVA2012_G5),
                         Decimal('0.8243464052287581699346405229'))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise S on Group 2 from the dataset
        collected in Kazantseva (2012).
        '''
        self.assertEqual(pairwise_similarity_micro(KAZANTSEVA2012_G2),
                         Decimal('0.8891428571428571428571428571'))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise S on a theoretical dataset
        containing large disagreement.
        '''
        self.assertEqual(pairwise_similarity_micro(LARGE_DISAGREEMENT),
                         0.0)
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise S on a theoretical dataset
        containing complete agreement.
        '''
        self.assertEqual(pairwise_similarity_micro(COMPLETE_AGREEMENT),
                         1.0)

    