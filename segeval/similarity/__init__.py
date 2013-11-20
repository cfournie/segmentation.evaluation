'''
Similarity utility functions based upon boundary edit distance.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import, division
from segeval.similarity.distance import identify_types
from segeval.similarity.distance.multipleboundary import boundary_edit_distance
from segeval.similarity.weight import weight_a, weight_s_scale, weight_t_scale
from segeval.metric import METRIC_DEFAULTS
from segeval.ml import ConfusionMatrix as cm
from segeval.format import (BoundaryFormat, boundary_string_from_masses,
                            convert_positions_to_masses, convert_nltk_to_masses)
from segeval.util import __fnc_metric__, SegmentationMetricError


SIMILARITY_METRIC_DEFAULTS = dict(METRIC_DEFAULTS)
SIMILARITY_METRIC_DEFAULTS.update({
    'n_t': 2,
    'boundary_types': None,
    'weight': (weight_a, weight_s_scale, weight_t_scale)
})


def __boundary_statistics__(
        segs_a, segs_b, boundary_types, boundary_format, n_t, weight):
    '''
    Compute boundary similarity applying the weighting functions specified.
    '''

    # Convert from NLTK types
    if boundary_format == BoundaryFormat.nltk:
        segs_a = convert_nltk_to_masses(segs_a)
        segs_b = convert_nltk_to_masses(segs_b)
        boundary_format = BoundaryFormat.mass
    # Check format
    if boundary_format == BoundaryFormat.sets:
        pass  # Correct boundary format
    elif boundary_format == BoundaryFormat.mass:
        segs_a = boundary_string_from_masses(segs_a)
        segs_b = boundary_string_from_masses(segs_b)
    elif boundary_format == BoundaryFormat.position:
        segs_a = convert_positions_to_masses(segs_a)
        segs_b = convert_positions_to_masses(segs_b)
        segs_a = boundary_string_from_masses(segs_a)
        segs_b = boundary_string_from_masses(segs_b)
    else:
        raise SegmentationMetricError('Unsupported boundary format')
    # Check length
    if len(segs_a) != len(segs_b):
        raise SegmentationMetricError(
            'Segmentations differ in length ({0} != {1})'.format(
                len(segs_a), len(segs_b)))
    # Determine the boundary types
    boundary_types = identify_types(segs_a, segs_b)
    # Calculate the total pbs
    pbs = len(segs_b) * len(boundary_types)
    # Compute edits
    additions, substitutions, transpositions = \
        boundary_edit_distance(segs_a, segs_b, n_t=n_t)
    # Apply weighting functions
    fnc_weight_a, fnc_weight_s, fnc_weight_t = weight
    count_additions = fnc_weight_a(additions)
    count_substitutions = fnc_weight_s(substitutions,
                                       max(boundary_types),
                                       min(boundary_types))
    count_transpositions = fnc_weight_t(transpositions, n_t)
    count_edits = count_additions + count_substitutions + count_transpositions
    # Compute
    matches = list()
    full_misses = list()
    boundaries_all = 0
    for set_a, set_b in zip(segs_a, segs_b):
        matches.extend(set_a.intersection(set_b))
        full_misses.extend(set_a.symmetric_difference(set_b))
        boundaries_all += len(set_a) + len(set_b)
    return {'count_edits': count_edits, 'additions': additions,
            'substitutions': substitutions, 'transpositions': transpositions,
            'full_misses': full_misses, 'boundaries_all': boundaries_all,
            'matches': matches, 'pbs': pbs, 'boundary_types': boundary_types}


def __boundary_confusion_matrix__(*args, **kwargs):
    '''
    Create a confusion matrix using boundary edit distance.
    '''

    # Trim kwargs
    metric_kwargs = dict(kwargs)
    del metric_kwargs['return_parts']
    del metric_kwargs['one_minus']
    # Obtain statistics
    statistics = __boundary_statistics__(*args, **metric_kwargs)
    # Get parameters
    n_t = kwargs['n_t']
    weight = kwargs['weight']
    # Initialize
    matrix = cm()
    fnc_weight_t = weight[2]
    # Add matches
    for match in statistics['matches']:
        matrix[match][match] += 1
    # Add weighted near misses
    for transposition in statistics['transpositions']:
        match = transposition[2]
        matrix[match][match] += fnc_weight_t([transposition], n_t)
    # Add confusion errors
    for substitution in statistics['substitutions']:
        hyp, ref = substitution
        matrix[hyp][ref] += 1
    # Add full misses
    for addition in statistics['additions']:
        hyp, ref = None, None
        boundary_type, side = addition
        if side == 'a':
            hyp = None
            ref = boundary_type
        else:  # side == 'b'
            hyp = boundary_type
            ref = None
        assert side == 'a' or side == 'b'
        matrix[hyp][ref] += 1
    return matrix


def boundary_confusion_matrix(*args, **kwargs):

    return __fnc_metric__(__boundary_confusion_matrix__, args, kwargs,
                          SIMILARITY_METRIC_DEFAULTS)


def boundary_statistics(*args, **kwargs):

    default_kwargs = dict(SIMILARITY_METRIC_DEFAULTS)
    del default_kwargs['one_minus']
    del default_kwargs['return_parts']
    return __fnc_metric__(__boundary_statistics__, args, kwargs,
                          default_kwargs)
