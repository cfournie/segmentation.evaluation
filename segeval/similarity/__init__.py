'''
Similarity utility functions based upon boundary edit distance.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division
from decimal import Decimal
from .distance.multipleboundary import boundary_edit_distance
from ..ml import ConfusionMatrix as cm


DEFAULT_N_T = 2
DEFAULT_BOUNDARY_TYPES = set([1])
DEFAULT_CONVERT_TO_BOUNDARY_STRINGS = True


def boundary_string_from_masses(masses):
    '''
    Creates a "boundary string", or sequence of boundary type sets.
    
    :param masses: Segmentation masses.
    :type masses:  list
    :returns: A sequence of boundary type sets
    :rtype: :func:`list` of :func:`set` objects containing :func:`int` values.
    '''
    string = [set() for _ in xrange(0, sum(masses) - 1)]
    # Iterate over each position
    pos = 0
    for mass in masses:
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
    matches = list()
    full_misses = list()
    boundaries_all = 0
    for set_a, set_b in zip(bs_a, bs_b):
        matches.extend(set_a.intersection(set_b))
        full_misses.extend(set_a.symmetric_difference(set_b))
        boundaries_all += len(set_a) + len(set_b)
    return {'count_edits' : count_edits, 'additions' : additions,
            'substitutions' : substitutions, 'transpositions' : transpositions, 
            'full_misses' : full_misses, 'boundaries_all' : boundaries_all, 
            'matches' : matches, 'pbs' : pbs}


def confusion_matrix(hypothesis, reference,
                     boundary_types=DEFAULT_BOUNDARY_TYPES,
                     n_t=DEFAULT_N_T, weight=DEFAULT_WEIGHT,
                     convert_to_boundary_strings=\
                        DEFAULT_CONVERT_TO_BOUNDARY_STRINGS):
    '''
    Create a confusion matrix using boundary edit distance.
    '''
    # pylint: disable=C0103,R0913,R0914
    statistics = descriptive_statistics(\
                           hypothesis, reference,
                           boundary_types=boundary_types,
                           n_t=n_t, weight=weight,
                           convert_to_boundary_strings=\
                            convert_to_boundary_strings)
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
        else:
            hyp = boundary_type
            ref = None
        matrix[hyp][ref] += 1
    return matrix

