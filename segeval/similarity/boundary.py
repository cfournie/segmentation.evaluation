'''
Boundary Similarity (B) package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import, division
from segeval.similarity import __boundary_statistics__, SIMILARITY_METRIC_DEFAULTS
from segeval.util import __fnc_metric__
from decimal import Decimal


def __boundary_similarity__(*args, **kwargs):

    metric_kwargs = dict(kwargs)
    del metric_kwargs['return_parts']
    del metric_kwargs['one_minus']
    # Arguments
    return_parts = kwargs['return_parts']
    one_minus = kwargs['one_minus']
    # Compute
    statistics = __boundary_statistics__(*args, **metric_kwargs)
    additions = statistics['additions']
    substitutions = statistics['substitutions']
    transpositions = statistics['transpositions']
    count_unweighted = len(additions) + len(substitutions) + len(transpositions)
    # Fraction
    denominator = count_unweighted + len(statistics['matches'])
    numerator = denominator - statistics['count_edits']
    if return_parts:
        return numerator, denominator, additions, substitutions, transpositions
    else:
        value = numerator / denominator if denominator > 0 else 1
        if one_minus:
            return Decimal('1') - value
        else:
            return value


def boundary_similarity(*args, **kwargs):
    '''
    Boundary Similarity (B).
    '''

    return __fnc_metric__(__boundary_similarity__, args, kwargs,
                          SIMILARITY_METRIC_DEFAULTS)
