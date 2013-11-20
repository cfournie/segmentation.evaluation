'''
Implementation of the Pk segmentation evaluation metric described in
[BeefermanBerger1999]_.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division, absolute_import
from decimal import Decimal
from segeval.window import __compute_window_size__, WINDOW_METRIC_DEFAULTS
from segeval.util import __fnc_metric__, SegmentationMetricError
from segeval.format import (
    BoundaryFormat,
    convert_masses_to_positions,
    convert_nltk_to_masses)


def __pk__(hypothesis, reference, window_size, one_minus, boundary_format,
           return_parts, fnc_round):

    # Convert from NLTK types
    if boundary_format == BoundaryFormat.nltk:
        reference = convert_nltk_to_masses(reference)
        hypothesis = convert_nltk_to_masses(hypothesis)
        boundary_format = BoundaryFormat.mass
    # Convert from masses into positions
    if boundary_format == BoundaryFormat.mass:
        reference = convert_masses_to_positions(reference)
        hypothesis = convert_masses_to_positions(hypothesis)
    elif boundary_format != BoundaryFormat.position:
        raise SegmentationMetricError('Unsupported boundary format')
    # Check for input errors
    if len(reference) != len(hypothesis):
        raise SegmentationMetricError(
            'Reference and hypothesis segmentations differ in position length ({0} is not {1}).'.format(len(reference), len(hypothesis)))
    # Compute window size to use if unspecified
    if window_size is None:
        window_size = __compute_window_size__(reference, fnc_round,
                                              BoundaryFormat.position)
    # Create a set of pairs of units from each segmentation to go over using a
    # window
    sum_differences = 0
    # Slide window over and sum the number of varying windows
    measurements = 0
    for i in range(0, len(reference) - (window_size)):
        # Create probe windows with k boundaries inside
        window_ref = reference[i:i + window_size + 1]
        window_hyp = hypothesis[i:i + window_size + 1]
        # Probe agreement
        agree_ref = window_ref[0] is window_ref[-1]
        agree_hyp = window_hyp[0] is window_hyp[-1]
        # If the windows agreements agree
        if agree_ref is not agree_hyp:
            sum_differences += 1
        measurements += 1
    # Perform final division
    value = Decimal(sum_differences) / measurements if measurements > 0 else 0
    if return_parts:
        return sum_differences, measurements
    else:
        if one_minus:
            return Decimal('1.0') - value
        else:
            return value


def pk(*args, **kwargs):

    return __fnc_metric__(__pk__, args, kwargs, WINDOW_METRIC_DEFAULTS)
