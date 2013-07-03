'''
Weighting functions for edit operations produced by boundary edit distance.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from decimal import Decimal


def weight_a(additions):
    '''
    Default unweighted weighting function for addition edit operations.
    '''
    return len(additions)


def weight_s(substitutions, max_s, min_s=1):
    '''
    Unweighted weighting function for substitution edit operations.
    '''

    return len(substitutions)


def weight_s_scale(substitutions, max_s, min_s=1):
    '''
    Default weighting function for substitution edit operations by the distance between ordinal boundary types.
    '''

    return weight_t_scale(substitutions, max_s - min_s + 1)


def weight_t(transpositions, max_n):
    '''
    Unweighted weighting function for transposition edit operations.
    '''

    return len(transpositions)


def weight_t_scale(transpositions, max_n):
    '''
    Default weighting function for transposition edit operations by the distance that transpositions span.
    '''
    numerator = 0
    for transposition in transpositions:
        numerator += abs(transposition[0] - transposition[1])
    return Decimal(numerator) / max_n
