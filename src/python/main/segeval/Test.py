'''
Tests some general segeval utility functions.

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
from decimal import Decimal
from . import convert_positions_to_masses, convert_masses_to_positions, \
    compute_pairwise
from .data.Samples import KAZANTSEVA2012_G5
from .ml.FbMeasure import f_b_measure


class TestSegeval(unittest.TestCase):
    '''
    segeval utility function tests.
    '''
    #pylint: disable=R0904,C0103
    
    def test_convert_positions_to_masses(self):
        '''
        Test segment position sequence conversion to masses.
        '''
        #pylint: disable=C0324
        self.assertEqual([5,3,5],
                         convert_positions_to_masses(
                            [1,1,1,1,1,2,2,2,3,3,3,3,3]))
        
      
    def test_convert_masses_to_positions(self):
        '''
        Test segment position sequence conversion to masses.
        '''
        #pylint: disable=C0324
        self.assertEqual([1,1,1,1,1,2,2,2,3,3,3,3,3],
                         convert_masses_to_positions([5,3,5]))
    
    
    def test_compute_pairwise(self):
        '''
        Tests computing pairwise values from dicts.  Ensures that dicts of
        arbitrary size can still be used.
        '''
        expected = (Decimal('0.2441586812212541867438777318'),
                    Decimal('0.2305169230001435997031211478'),
                    Decimal('0.05313805178945413332341442158'),
                    Decimal('0.04705406986889928477977431108'),
                    24)
        
        self.assertEqual(compute_pairwise(KAZANTSEVA2012_G5,
                                          f_b_measure),
                         expected)
        
        