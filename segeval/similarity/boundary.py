'''
Created on Sep 4, 2012

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division
from . import (descriptive_statistics, DEFAULT_N_T, DEFAULT_WEIGHT, 
    DEFAULT_BOUNDARY_TYPES, DEFAULT_CONVERT_TO_BOUNDARY_STRINGS)


def boundary_similarity(segs_a, segs_b,
                        boundary_types=DEFAULT_BOUNDARY_TYPES,
                        n_t=DEFAULT_N_T, weight=DEFAULT_WEIGHT,
                        convert_to_boundary_strings=\
                        DEFAULT_CONVERT_TO_BOUNDARY_STRINGS,
                        return_parts=False):
    '''
    Boundary Similarity.
    '''
    # pylint: disable=C0103,R0913,R0914
    statistics = descriptive_statistics(segs_a, segs_b,
                                        boundary_types=boundary_types, n_t=n_t,
                                        weight=weight,
                                        convert_to_boundary_strings=\
                                            convert_to_boundary_strings)
    additions = statistics['additions']
    substitutions = statistics['substitutions']
    transpositions = statistics['transpositions']
    count_unweighted = len(additions) + len(substitutions) + len(transpositions)
    # Fraction
    denominator = count_unweighted + len(statistics['matches'])
    numerator   = denominator - statistics['count_edits']
    if return_parts:
        return numerator, denominator, additions, substitutions, transpositions
    else:
        return numerator / denominator if denominator > 0 else 1

