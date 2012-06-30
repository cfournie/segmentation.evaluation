'''
Tests the segmentation versions of Cohen's and Fleiss' Kappa.

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
from .Kappa import cohen_kappa, fleiss_kappa
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT


class TestKappa(unittest.TestCase):
    '''
    Test segmentation versions of Cohen's Kappa and Fleiss' Multi-Kappa.
    '''
    # pylint: disable=R0904
    
    SKIP = False

    def test_fleiss_kappa_g5(self):
        '''
        Test Kappa upon Group 5 of Kazantseva (2012) data.
        '''
        if TestKappa.SKIP:
            return
        data = KAZANTSEVA2012_G5
        self.assertEqual(fleiss_kappa(data),
                         Decimal('0.8198449828922561273654074436'))


    def test_fleiss_kappa_g5_ch1(self):
        '''
        Test Kappa upon Group 5, Chapter 1, of Kazantseva (2012) data.
        '''
        if TestKappa.SKIP:
            return
        data = KAZANTSEVA2012_G5['ch1']
        data = {'ch1' : data}
        self.assertEqual(fleiss_kappa(data),
                         Decimal('0.7462686567164179104477611940'))


    def test_fleiss_kappa_g2(self):
        '''
        Test Kappa upon Group 2 of Kazantseva (2012) data.
        '''
        if TestKappa.SKIP:
            return
        data = KAZANTSEVA2012_G2
        self.assertEqual(fleiss_kappa(data),
                         Decimal('0.8865951832180913251160770952'))


    def test_fleiss_kappa_g2_ch2(self):
        '''
        Test Kappa upon Group 2, Chapter 2, of Kazantseva (2012) data.
        '''
        if TestKappa.SKIP:
            return
        data = KAZANTSEVA2012_G2['ch2']
        data = {'ch2' : data}
        self.assertEqual(fleiss_kappa(data),
                         Decimal('0.8840057636887608069164265130'))
        

    def test_fleiss_kappa_disagree(self):
        '''
        Test Kappa upon a hypothetical dataset containing large disagreement.
        '''
        if TestKappa.SKIP:
            return
        data = LARGE_DISAGREEMENT
        self.assertEqual(fleiss_kappa(data),
                         Decimal('-0.05952156715012243360331512524'))
    
    
    def test_cohen_kappa(self):
        '''
        Test Cohen's and Fleiss' Kappa.
        '''
        if TestKappa.SKIP:
            return
        data1 = {'i1' : {'c1' : [2, 8, 2, 1],
                         'c2' : [2, 1, 7, 2, 1]}}
        kappa1  = cohen_kappa(data1)
        kappa1f = fleiss_kappa(data1)
        self.assertEqual(kappa1,
                         Decimal('0.9032258064516129032258064517'))
        self.assertEqual(kappa1, kappa1f)
        data2 = {'i1' : {'c1' : [2, 8, 2, 1],
                         'c2' : [11, 2]}}
        kappa2  = cohen_kappa(data2)
        kappa2f = fleiss_kappa(data2)
        self.assertEqual(kappa2,
                         Decimal('0.7352941176470588235294117647'))
        self.assertEqual(kappa2, kappa2f)
        self.assertTrue(kappa2 < kappa1)
    
    
    def test_cohen_kappa_complete(self):
        '''
        Test Kappa upon a hypothetical dataset containing complete agreement.
        '''
        if TestKappa.SKIP:
            return
        # pylint: disable=C0324
        data_complete = {'i1' : {'c1' : [2,8,2,1],
                                 'c2' : [2,8,2,1]}}
        kappa = cohen_kappa(data_complete)
        self.assertEqual(kappa, 1.0)
    
    
    def test_fleiss_kappa_complete(self):
        '''
        Test Kappa upon a hypothetical dataset containing complete agreement.
        '''
        if TestKappa.SKIP:
            return
        data_complete = COMPLETE_AGREEMENT
        kappa = fleiss_kappa(data_complete)
        self.assertEqual(kappa, 1.0)

