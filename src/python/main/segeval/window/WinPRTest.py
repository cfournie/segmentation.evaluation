'''
Tests the WinPR evaluation metric.

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
from .WinPR import win_pr, pairwise_winpr
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT


class TestWinPR(unittest.TestCase):
    # pylint: disable=R0904,C0324

    def test_identical(self):
        segs_a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        segs_b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b),
                         (4, 0, 0, 22) )
        self.assertEqual(win_pr(segs_a, segs_b, return_fscore=True),
                         Decimal('1') )

    def test_no_boundaries(self):
        segs_a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        segs_b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b),
                         (12, 12, 0, 67) )
        self.assertEqual(win_pr(segs_a, segs_b, return_fscore=True),
                         Decimal('0.6666666666666666666666666667') )
        self.assertEqual(win_pr(segs_b, segs_a),
                         (2, 0, 2, 22) )
        self.assertEqual(win_pr(segs_b, segs_a, return_fscore=True),
                         Decimal('0.6666666666666666666666666667') )

    def test_all_boundaries(self):
        segs_a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        segs_b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b),
                         (4, 0, 10, 12) )
        self.assertEqual(win_pr(segs_a, segs_b, return_fscore=True),
                         Decimal('0.4444444444444444444444444444') )
        self.assertEqual(win_pr(segs_b, segs_a),
                         (4, 10, 0, 12) )
        self.assertEqual(win_pr(segs_b, segs_a, return_fscore=True),
                         Decimal('0.4444444444444444444444444444') )

    def test_all_and_no_boundaries(self):
        segs_a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        segs_b = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.assertEqual(win_pr(segs_a, segs_b),
                         (2, 0, 12, 12) )
        self.assertEqual(win_pr(segs_a, segs_b, return_fscore=True),
                         Decimal('0.25') )
        self.assertEqual(win_pr(segs_b, segs_a),
                         (12, 72, 0, 7) )
        self.assertEqual(win_pr(segs_b, segs_a, return_fscore=True),
                         Decimal('0.25') )

    def test_translated_boundary(self):
        segs_a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        segs_b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(win_pr(segs_a, segs_b),
                         (3, 1, 1, 21) )
        self.assertEqual(win_pr(segs_a, segs_b, return_fscore=True),
                         Decimal('0.75') )
        self.assertEqual(win_pr(segs_b, segs_a),
                         (3, 1, 1, 21) )
        self.assertEqual(win_pr(segs_b, segs_a, return_fscore=True),
                         Decimal('0.75') )
    
    def test_extra_boundary(self):
        segs_a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        segs_b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(win_pr(segs_a, segs_b),
                         (4, 1, 0, 21) )
        self.assertEqual(win_pr(segs_a, segs_b, return_fscore=True),
                         Decimal('0.8888888888888888888888888889') )
        self.assertEqual(win_pr(segs_b, segs_a),
                         (4, 0, 1, 21) )
        self.assertEqual(win_pr(segs_b, segs_a, return_fscore=True),
                         Decimal('0.8888888888888888888888888889') )
    
    def test_full_miss_and_misaligned(self):
        segs_a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        segs_b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(win_pr(segs_a, segs_b),
                         (3, 2, 1, 20) )
        self.assertEqual(win_pr(segs_a, segs_b, return_fscore=True),
                         Decimal('0.6666666666666666666666666667') )
        self.assertEqual(win_pr(segs_b, segs_a),
                         (3, 1, 2, 20) )
        self.assertEqual(win_pr(segs_b, segs_a, return_fscore=True),
                         Decimal('0.6666666666666666666666666667') )
    
    def test_kazantseva2012_g5(self):
        self.assertEqual(pairwise_winpr(KAZANTSEVA2012_G5),
                         (0.5666704244829246,
                          0.12888939175854155,
                          0.016612475307886801))
    
    def test_kazantseva2012_g2(self):
        self.assertEqual(pairwise_winpr(KAZANTSEVA2012_G2),
                         (0.69788839687219373,
                          0.10885799550018138,
                          0.01185006318431751))
    
    def test_large_disagreement(self):
        self.assertEqual(pairwise_winpr(LARGE_DISAGREEMENT),
                         (0.26666666666666666,
                          0.0,
                          0.0))
    
    def test_complete_agreement(self):
        self.assertEqual(pairwise_winpr(COMPLETE_AGREEMENT),
                         (1.0,
                          0.0,
                          0.0))

