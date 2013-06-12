'''
Tests window-based segmentation metric utility functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''

from . import compute_window_size
from ..util.test import TestCase
from ..data.samples import KAZANTSEVA2012_G5


class TestWindow(TestCase):
    '''
    Test window metric fncs.
    '''
    # pylint: disable=R0904,C0324

    def test_window_size(self):
        reference = [1, 2, 3]
        self.assertEqual(2, compute_window_size(reference))
    
    def test_window_size_dataset(self):
        self.assertEqual(3, compute_window_size(KAZANTSEVA2012_G5))

