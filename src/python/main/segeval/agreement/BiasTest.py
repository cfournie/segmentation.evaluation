'''
Tests the segmentation version of Arstein and Poesio's bias.

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
from .Bias import artstein_poesio_bias
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT


class TestBias(unittest.TestCase):
    '''
    Test Arstein and Poesio's (2008) annotator bias.
    '''
    # pylint: disable=R0904

    def test_bias_g5(self):
        '''
        Test bias upon Group 5 of Kazantseva (2012) data.
        '''
        bias = artstein_poesio_bias(KAZANTSEVA2012_G5)
        self.assertTrue(bias > 0)
        self.assertEqual(bias,
                         Decimal('0.00841453429829254475759269324'))

    def test_bias_g5_ch1(self):
        '''
        Test bias upon Group 5, Chapter 1, of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G5['ch1']
        data = {'ch1' : data}
        bias = artstein_poesio_bias(data)
        self.assertTrue(bias > 0)
        self.assertEqual(bias,
                         Decimal('0.00390625000000000000000000011'))

    def test_bias_g2(self):
        '''
        Test bias upon Group 2 of Kazantseva (2012) data.
        '''
        bias = artstein_poesio_bias(KAZANTSEVA2012_G2)
        self.assertTrue(bias > 0)
        self.assertEqual(bias,
                         Decimal('0.00821695210923559041105482425'))

    def test_bias_g2_ch2(self):
        '''
        Test bias upon Group 2, Chapter 2, of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G2['ch2']
        data = {'ch2' : data}
        bias = artstein_poesio_bias(data)
        self.assertTrue(bias > 0)
        self.assertEqual(bias,
                         Decimal('0.00090702947845804988662131528'))

    def test_bias_complete(self):
        '''
        Test bias upon a hypothetical dataset containing complete agreement.
        '''
        bias = artstein_poesio_bias(COMPLETE_AGREEMENT)
        self.assertTrue(bias >= 0)
        self.assertEqual(bias,
                         Decimal('0.01455229356727327645713789012'))

