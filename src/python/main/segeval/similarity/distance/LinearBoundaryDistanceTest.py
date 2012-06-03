'''
Tests linear boundary edit distance.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2012, Chris Fournier
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


class TestLinearBoundaryDistance(unittest.TestCase):
    '''
    Tests linear boundary edit distance.
    '''
    # pylint: disable=R0904,C0324,C0103
    
    SKIP = False

    def test_nested_transp_case_linear(self):
        '''
        Test the linear transposition case.
        '''
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [1,1,7]
        mass_b = [5,1,3]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     7)
        self.assertEqual((d,len(t),len(s)), (1,1,0))
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     5)
        
        self.assertEqual((d,len(t),len(s)), (3,1,2))


    def test_suboptimal_transp(self):
        '''
        Test a decision to use substitutions instead of a transposition.
        '''
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [1,3,2]
        mass_b = [2,3,1]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     4)
        self.assertEqual((d,len(t),len(s)), (2,2,0))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     2)
        self.assertEqual((d,len(t),len(s)), (2,2,0))


    def test_n2_transp(self):
        '''
        Test transpositions with n=2
        '''
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [5,5]
        mass_b = [6,4]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     1)
        self.assertEqual((d,len(t),len(s)), (2,0,2))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     2)
        self.assertEqual((d,len(t),len(s)), (1,1,0))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     3)
        self.assertEqual((d,len(t),len(s)), (1,1,0))


    def test_n3_transp(self):
        '''
        Test transpositions with n=3
        '''
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [5,5]
        mass_b = [7,3]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     1)
        self.assertEqual((d,len(t),len(s)), (2,0,2))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     2)
        self.assertEqual((d,len(t),len(s)), (2,0,2))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     3)
        self.assertEqual((d,len(t),len(s)), (1,1,0))
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     4)
        self.assertEqual((d,len(t),len(s)), (1,1,0))

    
    def test_complex_case(self):
        '''
        Test a combination of substitutions and transpositions
        '''
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [1,2,2,4]
        mass_b = [2,2,5]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     4)
        self.assertEqual((d,len(t),len(s)), (3,2,1))
        
    def test_distance_1(self):
        '''
        Test a distance of one.
        '''
        if TestLinearBoundaryDistance.SKIP:
            return
        
        mass_a = [1,4,4]
        mass_b = [1,2,6]
        
        d,t,s = linear_edit_distance(mass_a,
                                     mass_b,
                                     5)
                                     
        self.assertEqual((d,len(t),len(s)), (1,1,0))
        
        
        
        
        
        