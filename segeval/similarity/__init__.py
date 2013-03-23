'''
Similarity package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import unittest
from decimal import Decimal


def load_tests(loader, tests, pattern):
    '''
    A load_tests functions utilizing the default loader.
    '''
    #pylint: disable=W0613
    from ..Utils import default_load_tests
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

