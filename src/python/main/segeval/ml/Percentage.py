'''
Percentage metric functions.

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
from .. import compute_pairwise


def find_boundary_position_freqs(segs_set):
    '''
    Converts a list of segmentation mass sets into a dict of boundary positions,
    and the frequency of the whether boundaries were chosen at that location or,
    or not,
    
    Arguments:
    segs_set -- List of segmentation mass sets
    
    Returns:
    Dict of boundary positions and their frequencies.
    '''
    seg_positions = dict()
    for segs_i in segs_set:
        # Iterate over boundary positions that precede the index, excluding the
        # first position so that the start is not counted as a boundary
        for i in xrange(1, len(segs_i)):
            position = sum(segs_i[0:i])
            try:
                seg_positions[position] += 1
            except KeyError:
                seg_positions[position] = 1
    return seg_positions


def percentage(segs_hypothesis, segs_reference):
    '''
    Calculates the percentage agreement between a hypothesis, and reference
    segmentation.
    
    Arguments:
    segs_hypothesis -- Hypothesis segmentation masses
    segs_reference  -- Reference segmentation masses
    
    Returns:
    Percentage.
    '''
    positions_hyp = find_boundary_position_freqs([segs_hypothesis])
    positions_ref = find_boundary_position_freqs([segs_reference])
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

