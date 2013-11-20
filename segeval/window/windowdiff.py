'''
Implementation of the WindowDiff segmentation evaluation metric described in
[PevznerHearst2002]_ with an optional modification to fix incorrect error
counting at the beginning and end of segmentations provided by
[LamprierEtAl2007]_.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division, absolute_import
from decimal import Decimal
from segeval.window import __compute_window_size__, WINDOW_METRIC_DEFAULTS
from segeval.format import (BoundaryFormat, convert_masses_to_positions,
                            convert_positions_to_masses, convert_nltk_to_masses)
from segeval.util import __fnc_metric__, SegmentationMetricError


WINDOWDIFF_METRIC_DEFAULTS = dict(WINDOW_METRIC_DEFAULTS)
WINDOWDIFF_METRIC_DEFAULTS.update({
    'lamprier_et_al_2007_fix': False
})


def __create_paired_window__(hypothesis, reference, window_size,
                             lamprier_et_al_2007_fix):
    '''
    Create a set of pairs of units from each segmentation to go over using a
    window.
    '''
    phantom_size = 0
    if lamprier_et_al_2007_fix is False:
        units_ref_hyp = zip(reference, hypothesis)
    else:
        phantom_size = window_size
        phantom_size = 1 if phantom_size <= 0 else phantom_size
        phantom = tuple([0] * phantom_size)
        units_ref_hyp = zip(phantom + reference + phantom,
                            phantom + hypothesis + phantom)
    return list(units_ref_hyp), phantom_size


def __window_diff__(hypothesis, reference, window_size, one_minus,
                    boundary_format, return_parts, fnc_round,
                    lamprier_et_al_2007_fix):
    '''
    Calculates the WindowDiff segmentation evaluation metric score for a
    hypothetical segmentation against a reference segmentation for a given
    window size.  The standard method of calculating the window size
    is performed a window size is not specified.

    :param hypothesis:     Hypothesis segmentation section labels
                                        sequence.
    :param reference:      Reference segmentation section labels
                                        sequence.
    :param window_size:              The size of the window that is slid over \
                                        the two segmentations used to count \
                                        mismatches (default is None and will \
                                        use the average window size)
    :param one_minus:                Return 1-WindowDiff to make it no longer \
                                         a penalty-metric.
    :param lamprier_et_al_2007_fix:  Apply a fix for improperly counted errors \
                                        at the beginning and end of \
                                        segmentations, provided by \
                                        _[LamprierEtAl2007].
    :param convert_from_masses:      Convert the segmentations provided from \
                                        masses into positions.
    :type hypothesis: list
    :type reference: list
    :type window_size: int
    :type one_minus: bool
    :type lamprier_et_al_2007_fix: bool
    :type convert_from_masses: bool

    .. note:: See :func:`segeval.convert_masses_to_positions` for an example of
              the input format.
    '''
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
            'Reference and hypothesis segmentations differ in position \
length (%(ref)i is not %(hyp)i).' % {'ref': len(reference),
                                     'hyp': len(hypothesis)})
    # Compute window size to use if unspecified
    if window_size is None:
        window_size = __compute_window_size__(reference, fnc_round,
                                              BoundaryFormat.position)
    # Create a set of pairs of units from each segmentation to go over using a
    # window
    units_ref_hyp = __create_paired_window__(hypothesis, reference,
                                             window_size,
                                             lamprier_et_al_2007_fix)[0]
    # Slide window over and sum the number of varying windows
    sum_differences = 0
    measurements = len(units_ref_hyp) - window_size
    for i in range(0, measurements):
        window = units_ref_hyp[i: i + window_size + 1]
        ref_boundaries = 0
        hyp_boundaries = 0
        # Check that the number of loops is correct
        assert len(window) is window_size + 1
        # For pair in window
        for j in range(0, len(window) - 1):
            ref_part, hyp_part = zip(*window[j:j + 2])
            # Boundary exists in the reference segmentation
            if ref_part[0] is not ref_part[1]:
                ref_boundaries += 1
            # Boundary exists in the hypothesis segmentation
            if hyp_part[0] is not hyp_part[1]:
                hyp_boundaries += 1
        # If the number of boundaries per segmentation in the window differs
        if ref_boundaries is not hyp_boundaries:
            sum_differences += 1
    # Perform final division
    n = sum(convert_positions_to_masses(reference))
    denominator = n - window_size
    if lamprier_et_al_2007_fix:
        denominator = measurements + 1
    win_diff = Decimal(sum_differences) / denominator
    # Check normalization
    assert denominator == measurements or lamprier_et_al_2007_fix
    # Check value
    assert win_diff <= 1
    if not one_minus:
        if return_parts:
            return sum_differences, denominator
        else:
            return win_diff
    else:
        return Decimal('1.0') - win_diff


def window_diff(*args, **kwargs):

    return __fnc_metric__(__window_diff__, args, kwargs,
                          WINDOWDIFF_METRIC_DEFAULTS)
