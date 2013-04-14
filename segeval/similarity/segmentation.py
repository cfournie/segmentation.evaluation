'''
Similarity package

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division
from . import (descriptive_statistics, DEFAULT_N_T, DEFAULT_BOUNDARY_TYPES, 
    DEFAULT_WEIGHT, DEFAULT_CONVERT_TO_BOUNDARY_STRINGS)


def segmentation_similarity(segs_a, segs_b,
                            boundary_types=DEFAULT_BOUNDARY_TYPES,
                            n_t=DEFAULT_N_T, weight=DEFAULT_WEIGHT,
                            convert_to_boundary_strings=\
                            DEFAULT_CONVERT_TO_BOUNDARY_STRINGS,
                            return_parts=False):
    '''
    S
    '''
    # pylint: disable=C0103,R0913,R0914
    statistics = descriptive_statistics(segs_a, segs_b,
                                        boundary_types=boundary_types, n_t=n_t,
                                        weight=weight,
                                        convert_to_boundary_strings=\
                                            convert_to_boundary_strings)
    pbs = statistics['pbs'] * len(boundary_types)
    # Fraction
    denominator = pbs
    numerator   = pbs - statistics['count_edits']
    if return_parts:
        return numerator, denominator
    else:
        return numerator / denominator if denominator > 0 else 1

