'''
Segmentation Similarity (S) package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division
from . import __boundary_statistics__, SIMILARITY_METRIC_DEFAULTS
from ..util import __fnc_metric__
from decimal import Decimal


def __segmentation_similarity__(*args, **kwargs):
    '''
    Segmentation Similarity (S).
    '''

    metric_kwargs = dict(kwargs)
    del metric_kwargs['return_parts']
    del metric_kwargs['one_minus']
    # Arguments
    boundary_types = kwargs['boundary_types']
    return_parts = kwargs['return_parts']
    one_minus = kwargs['one_minus']
    # Compute
    statistics = __boundary_statistics__(*args, **metric_kwargs)
    # Process
    pbs = statistics['pbs'] * len(boundary_types)
    # Fraction
    denominator = pbs
    numerator = pbs - statistics['count_edits']
    if return_parts:
        return numerator, denominator
    else:
        value = numerator / denominator if denominator > 0 else 1
        if one_minus:
            return Decimal('1') - value
        else:
            return value


def segmentation_similarity(*args, **kwargs):
    '''
    Segmentation Similarity (S).
    '''
    return __fnc_metric__(__segmentation_similarity__, args, kwargs,
                          SIMILARITY_METRIC_DEFAULTS)
