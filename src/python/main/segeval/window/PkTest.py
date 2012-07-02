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
from ..window.Pk import pk, pairwise_pk
from ..data.Samples import KAZANTSEVA2012_G5, KAZANTSEVA2012_G2, \
    COMPLETE_AGREEMENT, LARGE_DISAGREEMENT


class TestPk(unittest.TestCase):
    '''
    Test Pk.
    '''
    # pylint: disable=R0904

    def test_identical(self):
        '''
        Test whether identical segmentations produce 0.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        self.assertEqual(pk(a, b), 0.0)
        self.assertEqual(pk(a, b, one_minus=True), 1.0)

    def test_no_boundaries(self):
        '''
        Test whether no segments versus some segments produce 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(pk(b, a),
                         Decimal('1.0'))
        self.assertEqual(pk(a, b),
                         Decimal('0.3636363636363636363636363636'))

    def test_all_boundaries(self):
        '''
        Test whether all segments versus some segments produces 7/11 = 0.636
        erroneous windows.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(pk(a, b),
                         Decimal('0.6363636363636363636363636364'))
        self.assertEqual(pk(b, a),
                         Decimal('0.6363636363636363636363636364'))

    def test_all_and_no_boundaries(self):
        '''
        Test whether all segments versus no segments produces 1.0.
        '''
        # pylint: disable=C0324,C0103
        a = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        b = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.assertEqual(pk(a, b), 1.0)
        self.assertEqual(pk(b, a), 1.0)

    def test_translated_boundary(self):
        '''
        Test whether 2/3 total segments participate in mis-alignment produces
        0.182.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        self.assertEqual(pk(a, b),
                         Decimal('0.1818181818181818181818181818'))
        self.assertEqual(pk(b, a),
                         Decimal('0.1818181818181818181818181818'))
    
    def test_extra_boundary(self):
        '''
        Test whether 1/3 segments that are non-existent produces 0.091.
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,1,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(pk(a, b),
                         Decimal('0.09090909090909090909090909091'))
        self.assertEqual(pk(b, a),
                         Decimal('0.09090909090909090909090909091'))
    
    def test_full_miss_and_misaligned(self):
        '''
        Test whether a full miss and a translated boundary out of 4 produces
        0.273. 
        '''
        # pylint: disable=C0324,C0103
        a = [1,1,1,1,2,2,2,2,3,3,3,3,3]
        b = [1,1,1,1,1,2,3,3,4,4,4,4,4]
        self.assertEqual(pk(a, b),
                         Decimal('0.2727272727272727272727272727'))
        self.assertEqual(pk(b, a),
                         Decimal('0.2727272727272727272727272727'))


class TestPairwisePkMeasure(unittest.TestCase):
    # pylint: disable=R0904
    '''
    Test pairwise Pk.
    '''
    
    def test_kazantseva2012_g5(self):
        '''
        Calculate permuted pairwise Pk on Group 5 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_pk(KAZANTSEVA2012_G5,
                                     convert_from_masses=True),
                         (Decimal('0.3553005828239669303205984460'),
                          Decimal('0.1100176084609921563234047476'),
                          Decimal('0.01210387417147617290343989768'),
                          Decimal('0.01587967396513816764352290376'),
                          48))
    
    def test_kazantseva2012_g2(self):
        '''
        Calculate mean permuted pairwise Pk on Group 2 from the dataset
        collected in [KazantsevaSzpakowicz2012]_.
        '''
        self.assertEqual(pairwise_pk(KAZANTSEVA2012_G2,
                                     convert_from_masses=True),
                         (Decimal('0.2882256923776327507173609771'),
                          Decimal('0.1454395656787966169084191445'),
                          Decimal('0.02115266726483699483402909754'),
                          Decimal('0.01327675514600517730547602481'),
                          120))
    
    def test_large_disagreement(self):
        '''
        Calculate mean permuted pairwise Pk on a theoretical dataset
        containing large disagreement.
        '''
        self.assertEqual(pairwise_pk(LARGE_DISAGREEMENT,
                                     convert_from_masses=True),
                         (1.0,
                          0.0,
                          0.0,
                          0.0,
                          8))
    
    def test_complete_agreement(self):
        '''
        Calculate mean permuted pairwise Pk on a theoretical dataset
        containing complete agreement.
        '''
        self.assertEqual(pairwise_pk(COMPLETE_AGREEMENT,
                                     convert_from_masses=True),
                         (0.0,
                          0.0,
                          0.0,
                          0.0,
                          48))

