'''
Provides a segmentation version of the  percentage agreement metric.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2011-2012, Chris Fournier
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
from . import find_boundary_position_freqs
from .. import compute_pairwise


def percentage(hypothesis_masses, reference_masses):
    '''
    Calculates the percentage agreement between a hypothesis, and reference
    segmentation.
    
    :param hypothesis_masses: Hypothesis segmentation masses.
    :param reference_masses: Reference segmentation masses.
    :param beta: Scales how precision and recall are averaged.
    :type hypothesis_masses: list
    :type reference_masses: list
    
    :returns: F-measure.
    :rtype: :class:`decimal.Decimal`
    '''
    positions_hyp = find_boundary_position_freqs([hypothesis_masses])
    positions_ref = find_boundary_position_freqs([reference_masses])
    agree    = Decimal('0')
    disagree = Decimal('0')
    for pos in positions_ref.keys():
        if pos in positions_hyp:
            agree += 1
        else:
            disagree += 1
    for pos in positions_hyp.keys():
        if pos not in positions_ref:
            disagree += 1
    return agree / (agree + disagree)


def pairwise_percentage(dataset_masses):
    '''
    Calculate mean pairwise segmentation percentage.
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :type dataset_masses: dict
    
    :returns: Mean, standard deviation, and variance of segmentation percentage.
    :rtype: :func:`float`, :func:`float`, :func:`float`
    '''
    return compute_pairwise(dataset_masses, percentage, permuted=False)

