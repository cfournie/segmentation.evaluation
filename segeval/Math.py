'''
Math utility functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2012, Chris Fournier
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#       
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================
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
    return summation / len(values)
    
    
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

