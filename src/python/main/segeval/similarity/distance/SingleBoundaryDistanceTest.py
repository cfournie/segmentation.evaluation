'''
Tests the boundary distance and string methods functionality.

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
from .SingleBoundaryDistance import linear_edit_distance


class TestBoundaryDistance(unittest.TestCase):
    '''
    Test single boundary type edit distance.
    '''
    # pylint: disable=R0904,C0324,C0103
    
    SKIP = False
    
    def test_st_2_basic_cases(self):
        '''
        Substitution and transpsition (n=2) basic cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        # Transposition
        mass_a = [2,2]
        mass_b = [3,1]
        d,t,s = linear_edit_distance(mass_a, mass_b, 2)[0:3]
        self.assertEqual((d,len(t),len(s)), (1,1,0))
        
        d,t,s = linear_edit_distance(mass_a, mass_b, 2)[0:3]
        self.assertEqual((d,len(t),len(s)), (1,1,0))
        
        # Add/sub/del
        mass_a = [4,1]
        mass_b = [1,4]
        d,t,s = linear_edit_distance(mass_a, mass_b, 2)[0:3]
        self.assertEqual((d,len(t),len(s)), (2,0,2))
        
        mass_a = [4]
        mass_b = [4]
        d,t,s = linear_edit_distance(mass_a, mass_b, 2)[0:3]
        self.assertEqual((d,len(t),len(s)), (0,0,0))


    def test_st_2_edge_cases(self):
        '''
        Substitution and transpsition (n=2) edge cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        d,t,s = linear_edit_distance([], [], 2)[0:3]
        self.assertEqual((d,len(t),len(s)), (0,0,0))


    def test_st_2_complex_cases(self):
        '''
        Substitution and transpsition (n=2) complex cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        mass_a = [1,2,2,4]
        mass_b = [2,2,5]
        # Combination of add/sub/del and transposition
        d,t,s = linear_edit_distance(mass_a, mass_b, 2)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,2,1))


    def test_nested_transp_case(self):
        '''
        Nested transpsition case.
        '''
        if TestBoundaryDistance.SKIP:
            return
        mass_a = [1,1,7]
        mass_b = [5,1,3]
        d,t,s = linear_edit_distance(mass_a, mass_b, 7)[0:3]
        self.assertEqual((d,len(t),len(s)), (1,1,0))
        d,t,s = linear_edit_distance(mass_a, mass_b, 5)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,1,2))
    
    
    def test_st_1_basic_cases(self):
        '''
        Substitution and transpsition (n=1) basic cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        # Transposition
        d,t,s = linear_edit_distance([2,2],
                                     [3,1], 1)[0:3]
        self.assertEqual((d,len(t),len(s)), (2,0,2))
        d,t,s = linear_edit_distance([3,1],
                                     [2,2], 1)[0:3]
        self.assertEqual((d,len(t),len(s)), (2,0,2))
        # Add/sub/del
        d,t,s = linear_edit_distance([5,1],
                                     [1,5], 1)[0:3]
        self.assertEqual((d,len(t),len(s)), (2,0,2))
        d,t,s = linear_edit_distance([4],
                                     [4], 1)[0:3]
        self.assertEqual((d,len(t),len(s)), (0,0,0))


    def test_st_1_edge_cases(self):
        '''
        Substitution and transpsition (n=1) edge cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        d,t,s = linear_edit_distance([],
                                     [], 1)[0:3]
        self.assertEqual((d,len(t),len(s)), (0,0,0))


    def test_st_1_complex_cases(self):
        '''
        Substitution and transpsition (n=1) complex cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        # Combination of add/sub/del and transposition
        d,t,s = linear_edit_distance([1,2,2,4],
                                     [2,2,5], 1)[0:3]
        self.assertEqual((d,len(t),len(s)), (5,0,5))
    
    
    def test_st_3_basic_cases(self):
        '''
        Substitution and transpsition (n=3) basic cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        # Transposition
        d,t,s = linear_edit_distance([1,3],
                                     [3,1], 3)[0:3]
        self.assertEqual((d,len(t),len(s)), (1,1,0))
        # Transposition
        d,t,s = linear_edit_distance([2,2],
                                     [3,1], 3)[0:3]
        self.assertEqual((d,len(t),len(s)), (1,1,0))
        # Add/sub/del
        d,t,s = linear_edit_distance([5,1],
                                     [1,5], 3)[0:3]
        self.assertEqual((d,len(t),len(s)), (2,0,2))
        d,t,s = linear_edit_distance([4],
                                     [4], 3)[0:3]
        self.assertEqual((d,len(t),len(s)), (0,0,0))


    def test_st_3_complex_cases(self):
        '''
        Substitution and transpsition (n=3) complex cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        # Combination of add/sub/del and transposition
        d,t,s = linear_edit_distance([1,2,2,4],
                                     [2,2,5], 3)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,2,1))
        # Combination of add/sub/del and transposition
        d,t,s = linear_edit_distance([1,2,2,4],
                                     [2,2,3,2], 3)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
    
    
    def test_st_3_mixup_cases(self):
        '''
        Substitution and transpsition (n=3) mixup (tricky) cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        # Combination of add/sub/del and transposition
        d,t,s = linear_edit_distance([1,2,2,3],
                                     [2,2,2,2], 3)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,4],
                                     [2,2,3,2], 3)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,5],
                                     [2,2,4,2], 3)[0:3]
        self.assertEqual((d,len(t),len(s)), (4,2,2))
        
    def test_st_4_mixup_cases(self):
        '''
        Substitution and transpsition (n=4) mixup (tricky) cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        # Combination of add/sub/del and transposition
        d,t,s = linear_edit_distance([1,2,2,3],
                                     [2,2,2,2], 4)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,4],
                                     [2,2,3,2], 4)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,5],
                                     [2,2,4,2], 4)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,6],
                                     [2,2,5,2], 4)[0:3]
        self.assertEqual((d,len(t),len(s)), (4,2,2))
        
    def test_st_5_mixup_cases(self):
        '''
        Substitution and transpsition (n=5) mixup (tricky) cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        # Combination of add/sub/del and transposition
        d,t,s = linear_edit_distance([1,2,2,3],
                                     [2,2,2,2], 5)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,4],
                                     [2,2,3,2], 5)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,5],
                                     [2,2,4,2], 5)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,6],
                                     [2,2,5,2], 5)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,7],
                                     [2,2,6,2], 5)[0:3]
        self.assertEqual((d,len(t),len(s)), (4,2,2))
        
    def test_st_6_mixup_cases(self):
        '''
        Substitution and transpsition (n=6) mixup (tricky) cases.
        '''
        if TestBoundaryDistance.SKIP:
            return
        # Combination of add/sub/del and transposition
        d,t,s = linear_edit_distance([1,2,2,3],
                                     [2,2,2,2], 6)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,4],
                                     [2,2,3,2], 6)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,5],
                                     [2,2,4,2], 6)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,6],
                                     [2,2,5,2], 6)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,7],
                                     [2,2,6,2], 6)[0:3]
        self.assertEqual((d,len(t),len(s)), (3,3,0))
        d,t,s = linear_edit_distance([1,2,2,8],
                                     [2,2,7,2], 6)[0:3]
        self.assertEqual((d,len(t),len(s)), (4,2,2))

