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

.. codeauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal
from .Pi import fleiss_pi_linear
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
        self.assertEqual(fleiss_pi_linear(KAZANTSEVA2012_G5),
                         Decimal('0.2307643892167668335086819753'))


    def test_fliess_pi_g5_ch1(self):
        '''
        Test Pi upon Group 5, Chapter 1, of Kazantseva (2012) data.
        '''
        if TestPi.SKIP:
            return
        data = {'ch1' : KAZANTSEVA2012_G5['ch1']}
        self.assertEqual(fleiss_pi_linear(data),
                         Decimal('0.1906323185011709601873536298'))


    def test_fleiss_pi_g2(self):
        '''
        Test Pi upon Group 2 of Kazantseva (2012) data.
        '''
        if TestPi.SKIP:
            return
        # Test
        self.assertEqual(fleiss_pi_linear(KAZANTSEVA2012_G2),
                         Decimal('0.4018239928733601859131343866'))


    def test_fleiss_pi_g2_ch2(self):
        '''
        Test Pi upon Group 2, Chapter 2, of Kazantseva (2012) data.
        '''
        if TestPi.SKIP:
            return
        data = {'ch2' : KAZANTSEVA2012_G2['ch2']}
        # Test
        self.assertEqual(fleiss_pi_linear(data),
                         Decimal('0.5192587209302325581395348837'))
        

    def test_fleiss_pi_large_disagree(self):
        '''
        Test Pi upon a hypothetical dataset containing large disagreement.
        '''
        if TestPi.SKIP:
            return
        data = LARGE_DISAGREEMENT
        self.assertEqual(fleiss_pi_linear(data),
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
        pi1  = fleiss_pi_linear(data1)
        pi1f = fleiss_pi_linear(data1)
        self.assertEqual(pi1,
                         Decimal('0.7090909090909090909090909091'))
        self.assertEqual(pi1,pi1f)
        data2 = {'i1': {'c1' : [2, 8, 2, 1],
                        'c2' : [11, 2]}}
        pi2  = fleiss_pi_linear(data2)
        pi2f = fleiss_pi_linear(data2)
        self.assertEqual(pi2,
                         Decimal('0.1111111111111111111111111111'))
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
        pi = fleiss_pi_linear(data_complete)
        self.assertEqual(pi, 1.0)
    
    
    def test_fleiss_pi_complete(self):
        '''
        Test Pi upon a hypothetical dataset containing complete agreement.
        '''
        # pylint: disable=C0103
        if TestPi.SKIP:
            return
        data_complete = COMPLETE_AGREEMENT
        pi = fleiss_pi_linear(data_complete)
        self.assertEqual(pi, 1.0)

