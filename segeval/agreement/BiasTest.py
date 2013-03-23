'''
Tests the segmentation version of Arstein and Poesio's bias.

.. codeauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal
from .Bias import artstein_poesio_bias_linear
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
        bias = artstein_poesio_bias_linear(KAZANTSEVA2012_G5)
        self.assertTrue(bias > 0)
        self.assertEqual(bias,
                         Decimal('0.00841453429829254475759269324'))

    def test_bias_g5_ch1(self):
        '''
        Test bias upon Group 5, Chapter 1, of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G5['ch1']
        data = {'ch1' : data}
        bias = artstein_poesio_bias_linear(data)
        self.assertTrue(bias > 0)
        self.assertEqual(bias,
                         Decimal('0.00390625000000000000000000011'))

    def test_bias_g2(self):
        '''
        Test bias upon Group 2 of Kazantseva (2012) data.
        '''
        bias = artstein_poesio_bias_linear(KAZANTSEVA2012_G2)
        self.assertTrue(bias > 0)
        self.assertEqual(bias,
                         Decimal('0.00821695210923559041105482425'))

    def test_bias_g2_ch2(self):
        '''
        Test bias upon Group 2, Chapter 2, of Kazantseva (2012) data.
        '''
        data = KAZANTSEVA2012_G2['ch2']
        data = {'ch2' : data}
        bias = artstein_poesio_bias_linear(data)
        self.assertTrue(bias > 0)
        self.assertEqual(bias,
                         Decimal('0.00090702947845804988662131528'))

    def test_bias_complete(self):
        '''
        Test bias upon a hypothetical dataset containing complete agreement.
        '''
        bias = artstein_poesio_bias_linear(COMPLETE_AGREEMENT)
        self.assertTrue(bias >= 0)
        self.assertEqual(bias,
                         Decimal('0.01455229356727327645713789012'))

