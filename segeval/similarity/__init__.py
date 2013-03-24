'''
Similarity utility functions based upon boundary edit distance.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from decimal import Decimal
from .distance.multipleboundary import boundary_edit_distance


DEFAULT_N_T = 2
DEFAULT_BOUNDARY_TYPES = set([1])
DEFAULT_CONVERT_TO_BOUNDARY_STRINGS = True


def load_tests(loader, tests, pattern):
    '''
    A load_tests functions utilizing the default loader.
    '''
    #pylint: disable=W0613
    from ..utils import default_load_tests
    return default_load_tests(__file__, loader, tests)


def boundary_string_from_masses(segment_masses):
    '''
    Creates a "boundary string", or sequence of boundary type sets.
    
    :param segment_masses: Segmentation masses.
    :type segment_masses:  list
    :returns: A sequence of boundary type sets
    :rtype: :func:`list` of :func:`set` objects containing :func:`int` values.
    '''
    string = [set() for _ in xrange(0, sum(segment_masses) - 1)]
    # Iterate over each position
    pos = 0
    for mass in segment_masses:
        cur_pos = pos + mass - 1
        if cur_pos < len(string):
            string[cur_pos].add(1)
        pos += mass
    # Return
    return [set(pb) for pb in string]


def weight_a(additions):
    '''
    Default weighting function for addition edit operations.
    '''
    return len(additions)


def weight_s(substitutions, max_s, min_s=1):
    '''
    Default weighting function for substitution edit operations.
    '''
    # pylint: disable=W0613,C0103
    return len(substitutions)


def weight_s_scale(substitutions, max_s, min_s=1):
    '''
    Default weighting function for substitution edit operations.
    '''
    # pylint: disable=W0613,C0103
    return weight_t_scale(substitutions, max_s - min_s + 1)


def weight_t(transpositions, max_n):
    '''
    Default weighting function for transposition edit operations.
    '''
    # pylint: disable=W0613,C0103
    return len(transpositions)


def weight_t_scale(transpositions, max_n):
    '''
    Default weighting function for transposition edit operations.
    '''
    numerator   = 0
    if isinstance(transpositions, list):
        for transposition in transpositions:
            numerator += abs(transposition[0] - transposition[1])
        return Decimal(numerator) / max_n
    else:
        return Decimal(abs(transpositions[0] - transpositions[1])) / max_n



DEFAULT_WEIGHT = (weight_a, weight_s_scale, weight_t_scale)


def descriptive_statistics(segs_a, segs_b,
                           boundary_types=DEFAULT_BOUNDARY_TYPES,
                           n_t=DEFAULT_N_T, weight=DEFAULT_WEIGHT,
                           convert_to_boundary_strings=\
                            DEFAULT_CONVERT_TO_BOUNDARY_STRINGS):
    '''
    Compute boundary similarity applying the weighting functions specified.
    '''
    # pylint: disable=C0103,R0913,R0914
    # Count boundaries
    bs_a = segs_a
    bs_b = segs_b
    if convert_to_boundary_strings:
        bs_a = boundary_string_from_masses(segs_a)
        bs_b = boundary_string_from_masses(segs_b)
    # Calculate the total pbs
    pbs = len(bs_b) * len(boundary_types)
    # Compute edits
    additions, substitutions, transpositions = \
        boundary_edit_distance(bs_a, bs_b, n_t=n_t)
    # Apply weighting functions
    fnc_weight_a, fnc_weight_s, fnc_weight_t = weight
    count_additions      = fnc_weight_a(additions)
    count_substitutions  = fnc_weight_s(substitutions,
                                        max(boundary_types),
                                        min(boundary_types))
    count_transpositions = fnc_weight_t(transpositions, n_t)
    count_edits = count_additions + count_substitutions + count_transpositions
    # Compute
    full_misses = 0
    boundaries_all = 0
    matches = 0
    for set_a, set_b in zip(bs_a, bs_b):
        matches += len(set_a.intersection(set_b))
        full_misses += len(set_a.symmetric_difference(set_b))
        boundaries_all += len(set_a) + len(set_b)
    return count_edits, additions, substitutions, transpositions, full_misses, \
        boundaries_all, matches, pbs


def confusion_matrix(segs_a, segs_b,
                     boundary_types=DEFAULT_BOUNDARY_TYPES,
                     n_t=DEFAULT_N_T, weight=DEFAULT_WEIGHT,
                     convert_to_boundary_strings=\
                        DEFAULT_CONVERT_TO_BOUNDARY_STRINGS):
    '''
    Create a confusion matrix using boundary edit distance.
    '''
    # pylint: disable=C0103,R0913,R0914
    # Count boundaries
    bs_a = segs_a
    bs_b = segs_b
    if convert_to_boundary_strings:
        bs_a = boundary_string_from_masses(segs_a)
        bs_b = boundary_string_from_masses(segs_b)
    # Compute edits
    additions, substitutions, transpositions = \
        boundary_edit_distance(bs_a, bs_b, n_t=n_t)
    # Apply weighting functions
    fnc_weight_a, fnc_weight_s, fnc_weight_t = weight
    count_additions      = fnc_weight_a(additions)
    count_substitutions  = fnc_weight_s(substitutions,
                                        max(boundary_types),
                                        min(boundary_types))
    count_transpositions = fnc_weight_t(transpositions, n_t)
    count_edits = count_additions + count_substitutions + count_transpositions
    # Compute
    full_misses = 0
    boundaries_all = 0
    matches = 0
    for set_a, set_b in zip(bs_a, bs_b):
        matches += len(set_a.intersection(set_b))
        full_misses += len(set_a.symmetric_difference(set_b))
        boundaries_all += len(set_a) + len(set_b)
    return count_edits, additions, substitutions, transpositions, \
            full_misses, boundaries_all, matches
    

