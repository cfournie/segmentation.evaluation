

from . import compute_window_size, WINDOW_METRIC_DEFAULTS
from ..util.test import TestCase


class TestWindow(TestCase):
    '''
    Test window metric fncs.
    '''
    # pylint: disable=R0904,C0324

    def test_compute_window_size(self):
        fnc_round = WINDOW_METRIC_DEFAULTS['fnc_round']
        boundary_format = WINDOW_METRIC_DEFAULTS['boundary_format']
        reference = [1, 2, 3]
        self.assertEqual(2, compute_window_size(reference, fnc_round,
                                                boundary_format))
