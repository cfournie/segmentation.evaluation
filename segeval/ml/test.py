'''
Tests the machine learning (ML) statistics functions, and ml package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import unittest
from decimal import Decimal
from segeval.ml import (
    __precision__, precision, __recall__, recall, __fmeasure__,
    fmeasure, ConfusionMatrix as cm, Average)
from segeval.util import SegmentationMetricError


class TestConfusionMatrix(unittest.TestCase):

    '''
    Confusion matrix tests.
    '''

    def test_matrix_set_add(self):
        '''
        Test matrix.
        '''
        matrix = cm()
        matrix['p']['p'] += 2
        matrix['p']['n'] = 3
        self.assertEqual(matrix['p']['p'], 2)
        self.assertEqual(matrix['p']['n'], 3)
        self.assertEqual(matrix['p']['f'], 0)
        self.assertEqual(matrix['a']['b'], 0)

    def test_setitem(self):
        '''
        Ensure that __setitem__ raises an AttributeError
        '''
        exception = False
        matrix = cm()
        try:
            matrix['a'] = 0
        except AttributeError:
            exception = True
        self.assertTrue(exception, 'AttributeError not raised')

    def test_matrix_classes(self):
        '''
        Test matrix.
        '''
        matrix = cm()
        matrix['p']['p'] += 2
        matrix['p']['n'] = 3
        self.assertEqual(matrix['p']['p'], 2)
        self.assertEqual(matrix['p']['n'], 3)
        self.assertEqual(matrix['p']['f'], 0)
        self.assertEqual(matrix['a']['b'], 0)

        self.assertEqual(matrix.classes(), set(['p', 'n', 'a', 'b', 'f']))


class TestML(unittest.TestCase):

    '''
    Machine-learning metric tests.
    '''

    def test_precision(self):
        '''
        Test precision.
        '''
        matrix = cm()
        matrix['p']['p'] += 1
        matrix['p']['f'] += 1
        self.assertEqual(__precision__(matrix, 'p'), Decimal('0.5'))
        self.assertEqual(__precision__(matrix, 'f'), Decimal('0'))
        self.assertEqual(
            precision(matrix, version=Average.micro), Decimal('0.5'))
        self.assertEqual(
            precision(matrix, version=Average.macro), Decimal('0.25'))
        matrix = cm()
        matrix['p']['p'] += 1
        matrix['p']['f'] += 3
        matrix['f']['p'] += 1
        self.assertEqual(
            precision(matrix, version=Average.micro), Decimal('0.2'))
        self.assertEqual(
            precision(matrix, version=Average.macro), Decimal('0.125'))
        self.assertEqual(__precision__(matrix, 'p'), Decimal('0.25'))
        self.assertEqual(__precision__(matrix, 'f'), Decimal('0'))
        matrix = cm()
        matrix['p']['p'] += 5
        matrix['p']['f'] += 2
        matrix['f']['p'] += 1
        matrix['f']['f'] += 2
        self.assertEqual(
            precision(matrix, version=Average.micro), Decimal('0.7'))
        self.assertAlmostEqual(precision(matrix, version=Average.macro),
                               Decimal('0.69047'), 4)
        self.assertAlmostEqual(__precision__(matrix, 'p'),
                               Decimal('0.71428'), 4)
        self.assertAlmostEqual(__precision__(matrix, 'f'),
                               Decimal('0.66666'), 4)
        matrix = cm()
        matrix['p']['f'] += 2
        self.assertEqual(precision(matrix), Decimal('0'))
        self.assertEqual(__precision__(matrix, 'p'), Decimal('0'))
        self.assertEqual(__precision__(matrix, 'f'), Decimal('0'))
        matrix = cm()
        matrix['p']['p'] += 2
        self.assertEqual(precision(matrix), Decimal('1'))
        self.assertEqual(__precision__(matrix, 'p'), Decimal('1'))
        self.assertEqual(__precision__(matrix, 'f'), Decimal('0'))
        matrix = cm()
        self.assertEqual(precision(matrix), Decimal('0'))
        self.assertEqual(__precision__(matrix, 'p'), Decimal('0'))
        self.assertEqual(__precision__(matrix, 'f'), Decimal('0'))

    def test_recall(self):
        '''
        Test recall.
        '''
        matrix = cm()
        matrix['p']['p'] += 1
        matrix['p']['f'] += 1
        self.assertEqual(__recall__(matrix, 'p'), Decimal('1.0'))
        self.assertEqual(__recall__(matrix, 'f'), Decimal('0'))
        self.assertEqual(recall(matrix, version=Average.micro), Decimal('0.5'))
        self.assertEqual(recall(matrix, version=Average.macro), Decimal('0.5'))
        matrix = cm()
        matrix['p']['p'] += 1
        matrix['p']['f'] += 3
        matrix['f']['p'] += 1
        self.assertEqual(recall(matrix, version=Average.micro), Decimal('0.2'))
        self.assertEqual(
            recall(matrix, version=Average.macro), Decimal('0.25'))
        self.assertEqual(__recall__(matrix, 'p'), Decimal('0.5'))
        self.assertEqual(__recall__(matrix, 'f'), Decimal('0'))
        matrix = cm()
        matrix['p']['p'] += 5
        matrix['p']['f'] += 2
        matrix['f']['p'] += 1
        matrix['f']['f'] += 2
        self.assertEqual(recall(matrix, version=Average.micro), Decimal('0.7'))
        self.assertAlmostEqual(recall(matrix, version=Average.macro),
                               Decimal('0.66666'), 4)
        self.assertAlmostEqual(__recall__(matrix, 'p'),
                               Decimal('0.83333'), 4)
        self.assertAlmostEqual(__recall__(matrix, 'f'),
                               Decimal('0.5'), 4)
        matrix = cm()
        matrix['p']['f'] += 2
        self.assertEqual(recall(matrix), Decimal('0'))
        self.assertEqual(__recall__(matrix, 'p'), Decimal('0'))
        self.assertEqual(__recall__(matrix, 'f'), Decimal('0'))
        matrix = cm()
        matrix['p']['p'] += 2
        self.assertEqual(recall(matrix), Decimal('1'))
        self.assertEqual(__recall__(matrix, 'p'), Decimal('1'))
        self.assertEqual(__recall__(matrix, 'f'), Decimal('0'))
        matrix = cm()
        self.assertEqual(recall(matrix), Decimal('0'))
        self.assertEqual(__recall__(matrix, 'p'), Decimal('0'))
        self.assertEqual(__recall__(matrix, 'f'), Decimal('0'))

    def test_fmeasure(self):
        '''
        Test FMeasure.
        '''
        matrix = cm()
        matrix['p']['p'] += 1
        matrix['p']['f'] += 1
        self.assertAlmostEqual(
            __fmeasure__(matrix, 'p'), Decimal('0.66666'), 4)
        self.assertEqual(__fmeasure__(matrix, 'f'), Decimal('0'))
        self.assertAlmostEqual(fmeasure(matrix, version=Average.micro),
                               Decimal('0.66666'), 4)
        self.assertAlmostEqual(fmeasure(matrix, version=Average.macro),
                               Decimal('0.33333'), 4)
        self.assertAlmostEqual(fmeasure(matrix, classification='p'),
                               Decimal('0.66666'), 4)
        matrix = cm()
        matrix['p']['p'] += 1
        matrix['p']['f'] += 3
        matrix['f']['p'] += 1
        self.assertAlmostEqual(fmeasure(matrix, version=Average.micro),
                               Decimal('0.33333'), 4)
        self.assertAlmostEqual(fmeasure(matrix, version=Average.macro),
                               Decimal('0.16666'), 4)
        self.assertAlmostEqual(__fmeasure__(matrix, 'p'),
                               Decimal('0.33333'), 4)
        self.assertAlmostEqual(fmeasure(matrix, classification='p'),
                               Decimal('0.33333'), 4)
        self.assertEqual(__fmeasure__(matrix, 'f'), Decimal('0'))
        matrix = cm()
        matrix['p']['p'] += 5
        matrix['p']['f'] += 2
        matrix['f']['p'] += 1
        matrix['f']['f'] += 2
        self.assertAlmostEqual(fmeasure(matrix, version=Average.micro),
                               Decimal('0.68421'), 4)
        self.assertAlmostEqual(fmeasure(matrix, version=Average.macro),
                               Decimal('0.67032'), 4)
        self.assertAlmostEqual(__fmeasure__(matrix, 'p'),
                               Decimal('0.76923'), 4)
        self.assertAlmostEqual(__fmeasure__(matrix, 'f'),
                               Decimal('0.57142'), 4)
        matrix = cm()
        matrix['p']['f'] += 2
        self.assertEqual(fmeasure(matrix), Decimal('0'))
        self.assertEqual(__fmeasure__(matrix, 'p'), Decimal('0'))
        self.assertEqual(__fmeasure__(matrix, 'f'), Decimal('0'))
        matrix = cm()
        matrix['p']['p'] += 2
        self.assertEqual(fmeasure(matrix), Decimal('1'))
        self.assertEqual(__fmeasure__(matrix, 'p'), Decimal('1'))
        self.assertEqual(__fmeasure__(matrix, 'f'), Decimal('0'))
        matrix = cm()
        self.assertEqual(fmeasure(matrix), Decimal('0'))
        self.assertEqual(__fmeasure__(matrix, 'p'), Decimal('0'))
        self.assertEqual(__fmeasure__(matrix, 'f'), Decimal('0'))

    def test_exception_on_incorrect_average(self):
        '''
        Test exception on incorrect average.
        '''
        matrix = cm()
        matrix['p']['p'] += 1
        matrix['p']['f'] += 1
        self.assertRaises(
            SegmentationMetricError, fmeasure, matrix, version='incorrect')
