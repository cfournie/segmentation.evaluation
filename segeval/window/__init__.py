'''
Window based evaluation metricks package.  Provides window based segmentation
evaluation metrics including:

* Pk 
* WindowDiff and
* WinPR

.. warning:: These are provided for comparison, but are not recommended for \
    segmentation evaluation.  Instead, use  the segmentation similarity
    metric [FournierInkpen2012]_ implemented in
    :func:`segeval.similarity.SegmentationSimilarity.similarity` and the
    associated inter-coder agreement coefficients in
    :mod:`segeval.agreement`.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division
from decimal import Decimal
from .. import METRIC_DEFAULTS
from ..format import BoundaryFormat, convert_positions_to_masses
from ..util.math import mean


WINDOW_METRIC_DEFAULTS = dict(METRIC_DEFAULTS)
WINDOW_METRIC_DEFAULTS.update({
    'window_size' : None,
    'fnc_round' : round,
    'permuted' : True
})


def compute_window_size(reference, fnc_round, boundary_format):
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
        if isinstance(inner_coder_masses, list):
            all_masses.extend(inner_coder_masses)
        elif isinstance(inner_coder_masses, dict):
            for cur_inner_coder_masses in inner_coder_masses.values():
                __list_coder_masses__(cur_inner_coder_masses)
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

    