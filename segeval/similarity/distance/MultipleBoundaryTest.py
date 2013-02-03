'''
Tests multiple-boundary edit distance.

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
from .MultipleBoundary import boundary_edit_distance, \
    __additions_substitutions__, __additions_substitutions_sets__


class TestMultipleBoundaries(unittest.TestCase):
    '''
    Test items.
    '''
    # pylint: disable=R0904,C0324,C0103,C0301
    
    SKIP = False
    
    
    def test_additions_substitutions(self):
        '''
        Test the expected functionality of __additions_substitutions__
        '''
        a_i = set([1, 2, 3, 4])
        b_i = set([1, 6])
        
        a = a_i - b_i
        b = b_i - a_i
        d = a_i ^ b_i
        
        self.assertEqual((2, 1),
                         __additions_substitutions__(d, a, b))
    
    
    def test_additions_substitutions_sets(self):
        '''
        Test the expected functionality of __additions_substitutions_sets__
        '''
        a_i = set([1, 2, 3, 4])
        b_i = set([1, 6])
        
        a = a_i - b_i
        b = b_i - a_i
        d = a_i ^ b_i
        
        self.assertEqual((set([2, 3]), set([(4, 6)])), 
                         __additions_substitutions_sets__(d, a, b))
    
    
    def test_edit_distance_identity(self):
        '''
        Test a mixed example of additions, substitutions and transpositions.
        '''
        a = [set(), set([1]), set(), set(), set([1]), set(), set(), set(), set(), set()]
        b = a
        
        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([], [], []),
                         (additions, substitutions, transpositions))
    
    
    def test_edit_distance_compliment(self):
        '''
        Test a mixed example of additions, substitutions and transpositions.
        '''
        a = [set(   ), set(   ), set(   ), set(   ), set(   ), set(   ), set(   ), set(   ), set(   ), set(   )]
        b = [set([1]), set([1]), set([1]), set([1]), set([1]), set([1]), set([1]), set([1]), set([1]), set([1])]
        
        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [], []),
                         (additions, substitutions, transpositions))
    
    
    def test_edit_distance(self):
        '''
        Test a mixed example of additions, substitutions and transpositions.
        '''
        a = [set(), set([1   ]), set(), set(), set([1]), set(   ), set(), set(), set(   ), set()]
        b = [set(), set([2, 3]), set(), set(), set(   ), set([1]), set(), set(), set([3]), set()]
        
        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([3, 3], [(1, 2)], [(4, 5, 1)]),
                         (additions, substitutions, transpositions))
    
    
    def test_edit_distance_two_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([2]), set(), set(   ), set([2]), set(), set(), set()]
        b = [set(), set(), set(), set(   ), set(), set([2]), set(   ), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([2], [], [(5, 6, 2)]),
                         (additions, substitutions, transpositions))
    
    
    def test_edit_distance_no_two_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set([2]), set(), set(), set([2]), set([2]), set(), set(), set()]
        b = [set(), set(), set(   ), set(), set(), set([2]), set([2]), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([2], [], []),
                         (additions, substitutions, transpositions))
    
    
    def test_edit_distance_two_transpositions_equal(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set(), set([2]), set(   ), set([2]), set(), set(), set()]
        b = [set(), set(), set(), set(), set(   ), set([2]), set(   ), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b)
        self.assertEqual(([2], [], [(4, 5, 2)]),
                         (additions, substitutions, transpositions))
    
    
    def test_edit_distance_two_substitutions_into_two_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([2]), set(), set([1]), set(), set(), set(), set()]
        b = [set(), set(), set(), set([1]), set(), set([2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b, n=3)
        self.assertEqual(([], [(2, 1), (1, 2)], []),
                         (additions, substitutions, transpositions))
    
    
    def test_edit_distance_two_substitutions_into_no_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([2]), set(), set([3]), set(), set(), set(), set()]
        b = [set(), set(), set(), set([1]), set(), set([2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b, n=3)
        self.assertEqual(([], [(2,1), (3,2)], []),
                         (additions, substitutions, transpositions))
    
    
    def test_edit_distance_two_substitutions_one_ad_into_one_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([2,4]), set(), set([3]), set(), set(), set(), set()]
        b = [set(), set(), set(), set([1]), set(), set([2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b, n=3)
        self.assertEqual(([4], [(2, 1), (3, 2)], []),
                         (additions, substitutions, transpositions))
    
    
    def test_edit_distance_two_substitutions_one_ad_into_no_transpositions(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([2]), set(), set([3]), set(), set(), set(), set()]
        b = [set(), set(), set(), set([1,4]), set(), set([2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b, n=3)
        self.assertEqual(([4], [(2,1), (3,2)], []),
                         (additions, substitutions, transpositions))
    
    
    def test_edit_distance_three_transpositions_overlapping(self):
        '''
        Test two transpositions
        '''
        a = [set(), set(), set(), set([1,2,3]), set(),    set(     ), set(), set(), set(), set()]
        b = [set(), set(), set(), set(       ), set([3]), set([1,2]), set(), set(), set(), set()]
        additions, substitutions, transpositions = boundary_edit_distance(a, b, n=3)
        self.assertEqual(([], [], [(3,4,3),(3,5,1),(3,5,2)]),
                         (additions, substitutions, transpositions))
    
    
