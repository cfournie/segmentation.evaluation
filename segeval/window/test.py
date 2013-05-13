

from . import compute_window_size, WINDOW_METRIC_DEFAULTS
from ..util.test import TestCase
from ..data.samples import KAZANTSEVA2012_G5


class TestWindow(TestCase):
    '''
    Test window metric fncs.
    '''
    # pylint: disable=R0904,C0324

    def test_window_size(self):
        fnc_round = WINDOW_METRIC_DEFAULTS['fnc_round']
        boundary_format = WINDOW_METRIC_DEFAULTS['boundary_format']
        reference = [1, 2, 3]
        self.assertEqual(2, compute_window_size(reference, fnc_round,
                                                boundary_format))
    
    def test_window_size_dataset(self):
        fnc_round = WINDOW_METRIC_DEFAULTS['fnc_round']
        boundary_format = WINDOW_METRIC_DEFAULTS['boundary_format']
        self.assertEqual(3, compute_window_size(KAZANTSEVA2012_G5, fnc_round,
                                                boundary_format))

