'''
Window-based segmentation evaluation metrics package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division, absolute_import
from decimal import Decimal
from segeval.metric import METRIC_DEFAULTS
from segeval.format import BoundaryFormat, convert_positions_to_masses
from segeval.util import SegmentationMetricError
from segeval.util.math import mean


WINDOW_METRIC_DEFAULTS = dict(METRIC_DEFAULTS)
WINDOW_METRIC_DEFAULTS.update({
    'window_size': None,
    'fnc_round': round,
    'permuted': True
})


def __compute_window_size__(reference, fnc_round, boundary_format):
    '''
    Compute a window size from a dict of segment masses.

    :param masses: A dict of segment masses.
    :type masses: dict
    '''
    all_masses = list()
    # Define fnc

    def __list_coder_masses__(inner_coder_masses):
        '''
        Recursively collect all masses.

        :param inner_coder_masses: Either a dict of dicts, or dict of a list of
            masses.
        :type inner_coder_masses: dict or list
        '''
        if hasattr(inner_coder_masses, 'items'):
            for cur_inner_coder_masses in inner_coder_masses.values():
                __list_coder_masses__(cur_inner_coder_masses)
        elif hasattr(inner_coder_masses, '__iter__') and not isinstance(inner_coder_masses, str):
            all_masses.extend(inner_coder_masses)
        else:
            raise SegmentationMetricError('Expected either a dict-like \
collection of segmentations or a segmentation as a list-like object')
    if boundary_format == BoundaryFormat.position:
        reference = convert_positions_to_masses(reference)
    # Recurse and list all masses
    __list_coder_masses__(reference)
    # Convert to floats
    all_masses = [Decimal(mass) for mass in all_masses]
    # Calculate
    avg = mean(all_masses) / Decimal('2')
    window_size = int(fnc_round(avg))
    return window_size if window_size > 1 else 2


def compute_window_size(reference, **kwargs):
    metric_kwargs = dict(WINDOW_METRIC_DEFAULTS)
    metric_kwargs.update(kwargs)
    del metric_kwargs['one_minus']
    del metric_kwargs['permuted']
    del metric_kwargs['window_size']
    del metric_kwargs['return_parts']
    return __compute_window_size__(reference, **metric_kwargs)
