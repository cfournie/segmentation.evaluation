'''
Created on May 12, 2013

@author: cfournie
'''
from decimal import Decimal


def weight_a(additions):
    '''
    Default weighting function for addition edit operations.
    '''
    return len(additions)


def weight_s(substitutions, max_s, min_s=1):
    '''
    Potential weighting function for substitution edit operations.
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
    Potential weighting function for transposition edit operations.
    '''
    # pylint: disable=W0613,C0103
    return len(transpositions)


def weight_t_scale(transpositions, max_n):
    '''
    Default weighting function for transposition edit operations.
    '''
    numerator = 0
    if isinstance(transpositions, list):
        for transposition in transpositions:
            numerator += abs(transposition[0] - transposition[1])
        return Decimal(numerator) / max_n

