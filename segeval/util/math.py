'''
Math utility functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division, absolute_import
from decimal import Decimal


def mean(values):
    '''
    Calculates the mean of a list of numeric values.

    :param values: List of numeric values.
    :type values: list

    :returns: Mean.
    :rtype: :class:`decimal.Decimal`
    '''
    summation = Decimal(0)
    for value in values:
        summation += value
    if len(values) > 0:
        return summation / len(values)
    else:
        return 0


def var(values):
    '''
    Calculates the population variance of a list of numeric values.

    :param values: List of numeric values.
    :type values: list

    :returns: Variance.
    :rtype: :class:`decimal.Decimal`
    '''
    mean_value = mean(values)
    summation = Decimal(0)
    for value in values:
        summation += (value - mean_value) ** 2
    return summation / len(values)


def std(values):
    '''
    Calculates the population standard deviation of a list of numeric values.

    :param values: List of numeric values.
    :type values: list

    :returns: Standard deviation.
    :rtype: :class:`decimal.Decimal`
    '''
    return var(values).sqrt()


def stderr(values):
    '''
    Calculates the population standard error of the mean of a list of numeric
    values.

    :param values: List of numeric values.
    :type values: list

    :returns: Standard error of the mean.
    :rtype: :class:`decimal.Decimal`
    '''
    return std(values) / Decimal(len(values)).sqrt()


__all__ = []
