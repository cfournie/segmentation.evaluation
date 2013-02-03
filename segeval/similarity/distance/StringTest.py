'''
Tests the application of string edit distance algorithms upon string
representations of segmentaions.

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
from .String import levenshtein, damerau_levenshtein, jaro


class TestEditDistance(unittest.TestCase):
    '''
    Tests a variety of string edit distances as the could be used upon
    strings that represent segmentations.
    '''
    # pylint: disable=C0103,R0904
    
    skip = False
    
    def test_damerau_levenshtein_basic_cases(self):
        '''
        Test basic/simple cases.
        '''
        if TestEditDistance.skip:
            return
        # Transposition
        distance = damerau_levenshtein('--|--',
                                       '---|-')
        self.assertEqual(distance, 1)
        distance = damerau_levenshtein('---|-',
                                       '--|--')
        self.assertEqual(distance, 1)
        # Add/sub/del
        distance = damerau_levenshtein('-X---|-',
                                       '-|---X-')
        self.assertEqual(distance, 2)
        distance = damerau_levenshtein('----',
                                       '----')
        self.assertEqual(distance, 0)


    def test_damerau_levenshtein_edge_cases(self):
        '''
        Test empty strings.
        '''
        if TestEditDistance.skip:
            return
        distance = damerau_levenshtein('',
                                       '')
        self.assertEqual(distance, 0)


    def test_damerau_levenshtein_complex_cases(self):
        '''
        Test cases that have difficult interpretations.
        '''
        if TestEditDistance.skip:
            return
        # Combination of add/sub/del and transposition
        distance = damerau_levenshtein('-|--|--|----',
                                       '--|--|-X----')
        self.assertEqual(distance, 3)
        
    
    def test_levenshtein_basic_cases(self):
        '''
        Test basic/simple cases.
        '''
        if TestEditDistance.skip:
            return
        # Transposition
        distance = levenshtein('--|--',
                               '---|-')
        self.assertEqual(distance, 2)
        distance = levenshtein('---|-',
                               '--|--')
        self.assertEqual(distance, 2)
        # Add/sub/del
        distance = levenshtein('-----|-',
                               '-|-----')
        self.assertEqual(distance, 2)
        distance = levenshtein('----',
                               '----')
        self.assertEqual(distance, 0)


    def test_levenshtein_edge_cases(self):
        '''
        Test empty strings.
        '''
        if TestEditDistance.skip:
            return
        distance = levenshtein('',
                               '')
        self.assertEqual(distance, 0)


    def test_levenshtein_complex_cases(self):
        '''
        Test cases that have difficult interpretations.
        '''
        if TestEditDistance.skip:
            return
        # Combination of add/sub/del and transposition
        distance = levenshtein('-|--|--|----',
                               '--|--|-X----')
        self.assertEqual(distance, 3)
        
    
    def test_jaro_basic_cases(self):
        '''
        Test basic/simple cases.
        '''
        if TestEditDistance.skip:
            return
        # Transposition
        distance = jaro('--|--',
                        '---|-')
        self.assertEqual(distance, Decimal('0.9333333333333333333333333332'))
        distance = jaro('---|-',
                        '--|--')
        self.assertEqual(distance, Decimal('0.9333333333333333333333333332'))
        # Add/sub/del
        distance = jaro('-----|-',
                        '-|-----')
        self.assertEqual(distance, Decimal('0.9047619047619047619047619046'))
        distance = jaro('----',
                        '----')
        self.assertEqual(distance, Decimal('0.8333333333333333333333333332'))


    def test_jaro_edge_cases(self):
        '''
        Test empty strings.
        '''
        if TestEditDistance.skip:
            return
        distance = jaro('',
                        '')
        self.assertEqual(distance, 0)


    def test_jaro_complex_cases(self):
        '''
        Test cases that have difficult interpretations.
        '''
        if TestEditDistance.skip:
            return
        # Combination of add/sub/del and transposition
        distance = jaro('-|--|--|----',
                        '--|--|-X----')
        self.assertEqual(distance, Decimal('0.9999999999999999999999999999'))

