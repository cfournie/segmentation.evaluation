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
from .WindowDiff import window_diff,pairwise_windiff
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT


class TestWindowDiff(unittest.TestCase):
    # pylint: disable=R0904,C0324

    def test_identical(self):
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertEqual(window_diff(a,b), 0.0)

    def test_no_boundaries(self):
        a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(window_diff(a,b),
                         Decimal('1.0'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.1666666666666666666666666667'))

    def test_all_boundaries(self):
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.8333333333333333333333333333'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.8333333333333333333333333333'))

    def test_all_and_no_boundaries(self):
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.assertEqual(window_diff(a,b), 1.0)
        self.assertEqual(window_diff(b,a), 1.0)

    def test_translated_boundary(self):
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.1666666666666666666666666667'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.1666666666666666666666666667'))
    
    def test_extra_boundary(self):
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.08333333333333333333333333333'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.08333333333333333333333333333'))
    
    def test_full_miss_and_misaligned(self):
        a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(window_diff(a,b),
                         Decimal('0.25'))
        self.assertEqual(window_diff(b,a),
                         Decimal('0.25'))
    
    def test_fn_vs_fp(self):
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
        
    
    def test_Kazantseva2012_g5(self):
        self.assertEqual(pairwise_windiff(KAZANTSEVA2012_G5),
                         (0.36045062372598652,
                          0.16741031890126951,
                          0.028026214874624755))
    
    def test_Kazantseva2012_g2(self):
        self.assertEqual(pairwise_windiff(KAZANTSEVA2012_G2),
                         (0.25455124234555987,
                          0.12277644444889446,
                          0.015074055311512468))
    
    def test_large_disagreement(self):
        self.assertEqual(pairwise_windiff(LARGE_DISAGREEMENT),
                         (1.0,
                          0.0,
                          0.0))
    
    def test_complete_agreement(self):
        self.assertEqual(pairwise_windiff(COMPLETE_AGREEMENT),
                         (0.0,
                          0.0,
                          0.0))

