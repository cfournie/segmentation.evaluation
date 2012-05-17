'''
Tests the segmentation versions of Scott's and Fleiss' Pi.

References:
    Chris Fournier and Diana Inkpen. 2012. Segmentation Similarity and
    Agreement. Submitted manuscript.
    
    Ron Artstein and Massimo Poesio. 2008. Inter-coder agreement for
    computational linguistics. Computational Linguistics, 34(4):555-596. MIT
    Press.

    Marti A. Hearst. 1997. TextTiling: Segmenting Text into Multi-paragraph
    Subtopic Passages. Computational Linguistics, 23(1):33-64.
    
    William A. Scott. 1955. Reliability of content analysis: The case of nominal
    scale coding. Public Opinion Quarterly, 19(3):321-325.
    
    Joseph L. Fleiss. 1971. Measuring nominal scale agreement among many raters.
    Psychological Bulletin, 76(5):378-382.

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
from .Pi import scotts_pi, fleiss_pi
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT


class TestPi(unittest.TestCase):
    '''
    Test segmentation versions of Scott's Pi and Fleiss' Multi-Pi.
    '''
    # pylint: disable=R0904
    
    SKIP = False

    def test_fliess_pi_g5(self):
        '''
        Test Pi upon Group 5 of Kazantseva (2012) data.
        '''
        if TestPi.SKIP:
            return
        # Test
        self.assertEqual(fleiss_pi(KAZANTSEVA2012_G5),
                         Decimal('0.8182766795508965420878677699'))


    def test_fliess_pi_g5_ch1(self):
        '''
        Test Pi upon Group 5, Chapter 1, of Kazantseva (2012) data.
        '''
        if TestPi.SKIP:
            return
        data = {'ch1' : KAZANTSEVA2012_G5['ch1']}
        self.assertEqual(fleiss_pi(data),
                         Decimal('0.7451990632318501170960187353'))


    def test_fleiss_pi_g2(self):
        '''
        Test Pi upon Group 2 of Kazantseva (2012) data.
        '''
        if TestPi.SKIP:
            return
        # Test
        self.assertEqual(fleiss_pi(KAZANTSEVA2012_G2),
                         Decimal('0.8856338452498481859738514723'))


    def test_fleiss_pi_g2_ch2(self):
        '''
        Test Pi upon Group 2, Chapter 2, of Kazantseva (2012) data.
        '''
        if TestPi.SKIP:
            return
        data = {'ch2' : KAZANTSEVA2012_G2['ch2']}
        # Test
        self.assertEqual(fleiss_pi(data),
                         Decimal('0.8838942307692307692307692308'))
        

    def test_fleiss_pi_large_disagree(self):
        '''
        Test Pi upon a hypothetical dataset containing large disagreement.
        '''
        if TestPi.SKIP:
            return
        data = LARGE_DISAGREEMENT
        self.assertEqual(fleiss_pi(data),
                         Decimal('-0.5757942099675148626179719687'))


    def test_scotts_pi(self):
        '''
        Test Scott's and Fleiss' Pi.
        '''
        # pylint: disable=C0324,C0103
        if TestPi.SKIP:
            return
        data1 = {'i1': {'c1' : [2,8,2,1],
                        'c2' : [2,1,7,2,1]}}
        pi1  = scotts_pi(data1)
        pi1f = fleiss_pi(data1)
        self.assertEqual(pi1,
                         Decimal('0.9030303030303030303030303031'))
        self.assertEqual(pi1,pi1f)
        data2 = {'i1': {'c1' : [2, 8, 2, 1],
                        'c2' : [11, 2]}}
        pi2  = scotts_pi(data2)
        pi2f = fleiss_pi(data2)
        self.assertEqual(pi2,
                         Decimal('0.7333333333333333333333333333'))
        self.assertEqual(pi2,pi2f)
        self.assertTrue(pi2 < pi1)
    
    
    def test_scotts_pi_complete(self):
        '''
        Test Pi upon a hypothetical dataset containing complete agreement.
        '''
        # pylint: disable=C0324,C0103
        if TestPi.SKIP:
            return
        data_complete = {'i1': {'c1' : [2,8,2,1],
                                'c2' : [2,8,2,1]}}
        pi = scotts_pi(data_complete)
        self.assertEqual(pi, 1.0)
    
    
    def test_fleiss_pi_complete(self):
        '''
        Test Pi upon a hypothetical dataset containing complete agreement.
        '''
        # pylint: disable=C0103
        if TestPi.SKIP:
            return
        data_complete = COMPLETE_AGREEMENT
        pi = fleiss_pi(data_complete)
        self.assertEqual(pi, 1.0)

