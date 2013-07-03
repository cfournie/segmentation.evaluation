'''
Tests window-based segmentation metric utility functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from . import compute_window_size
from ..util import SegmentationMetricError
from ..util.test import TestCase
from ..data.samples import KAZANTSEVA2012_G5


class TestWindow(TestCase):

    '''
    Test window metric fncs.
    '''

    def test_window_size(self):
        reference = [1, 2, 3]
        self.assertEqual(2, compute_window_size(reference))

    def test_window_size_dataset(self):
        self.assertEqual(3, compute_window_size(KAZANTSEVA2012_G5))

    def test_window_size_exception(self):
        reference = 'incorrect type'
        self.assertRaises(SegmentationMetricError, compute_window_size, reference)
