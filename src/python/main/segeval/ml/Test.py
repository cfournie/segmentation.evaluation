'''
Tests the machine learning (ML) statistics functions, and ml package.

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
from . import precision, recall, fscore, confusionmatrix, prfcf


class TestML(unittest.TestCase):
    '''
    Machine-learning metric tests.
    '''
    # pylint: disable=R0904,C0103
    
    def test_precision(self):
        '''
        Test precision.
        '''
        tp = 1
        fp = 1
        self.assertEqual(precision(tp, fp), Decimal('0.5'))
        tp = 1
        fp = 3
        self.assertEqual(precision(tp, fp), Decimal('0.25'))
        tp = 6
        fp = 2
        self.assertEqual(precision(tp, fp), Decimal('0.75'))
        tp = 0
        fp = 2
        self.assertEqual(precision(tp, fp), Decimal('0'))
        tp = 2
        fp = 0
        self.assertEqual(precision(tp, fp), Decimal('1'))
        tp = 0
        fp = 0
        self.assertEqual(precision(tp, fp), Decimal('0'))
        
    def test_recall(self):
        '''
        Test recall.
        '''
        tp = 1
        fn = 1
        self.assertEqual(recall(tp, fn), Decimal('0.5'))
        tp = 1
        fn = 3
        self.assertEqual(recall(tp, fn), Decimal('0.25'))
        tp = 6
        fn = 2
        self.assertEqual(recall(tp, fn), Decimal('0.75'))
        tp = 0
        fn = 2
        self.assertEqual(recall(tp, fn), Decimal('0'))
        tp = 2
        fn = 0
        self.assertEqual(recall(tp, fn), Decimal('1'))
        tp = 0
        fn = 0
        self.assertEqual(recall(tp, fn), Decimal('0'))
        
    def test_f1(self):
        '''
        Test F-Score with a beta of 1.0, 0.5, or 2.0.
        '''
        tp = 2
        fp = 1
        fn = 1
        beta = 1.0
        self.assertEqual(fscore(tp, fp, fn, beta), Decimal('4') / Decimal('6'))
        tp = 1
        fp = 3
        fn = 1
        beta = 1.0
        self.assertEqual(fscore(tp, fp, fn, beta), Decimal('1') / Decimal('3'))
        beta = 0.5
        self.assertAlmostEqual(fscore(tp, fp, fn, beta), Decimal('0.277777777'))
        beta = 2.0
        self.assertAlmostEqual(fscore(tp, fp, fn, beta), Decimal('0.416666666'))
        tp = 0
        fp = 0
        fn = 0
        beta = 1.0
        self.assertEqual(fscore(tp, fp, fn, beta), Decimal('0'))
        
    def test_confusion_matrix(self):
        '''
        Tests confusion matrix calculation.
        '''
        tp = 1
        fp = 2
        fn = 3
        tn = None
        
        cf = ( (tp, fp), (fn, tn) )
        self.assertEqual(confusionmatrix(tp, fp, fn, tn), cf)
    
    def test_prfcf(self):
        '''
        Tests precision, recall, F1, and CF calculation.
        '''
        tp = 2
        fp = 4
        fn = 8
        tn = None
        
        p = Decimal('1') / Decimal('3')
        r = Decimal('0.2')
        f = Decimal('0.25')
        
        cf = ( (tp, fp), (fn, tn) )
        self.assertEqual(prfcf(tp, fp, fn, tn), (p, r, f, cf))

