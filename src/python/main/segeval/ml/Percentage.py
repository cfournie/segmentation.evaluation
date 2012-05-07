'''
Percentage metric functions.

@author: Chris Fournier
@contact: chris.m.fournier@gmail.com
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
from numpy import mean, std, var


def find_seg_positions(segs_set):
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
    positions_hyp = find_seg_positions([segs_hypothesis])
    positions_ref = find_seg_positions([segs_reference])
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


def pairwise_percentage(segs_dict_all, groups=False):
    '''
    Calculate mean permuted pairwise percentage.
    
    Arguments:
    segs_dict_all -- Dict of groups containing coders and segmentations (or just
                     the group contents)
    groups        -- True if segs_dict_all is split into groups, false if not
    
    Returns:
    Mean, standard deviation, and variance of percentages.
    '''
    values = list()
    # Define fnc per group
    def per_group(group, values):
        '''
        Calculate pairwise percentages for each group and append to output.
        
        Arguments:
        group  -- Dict of coders and segmentation masses
        values -- list of output percentages
        '''
        # pylint: disable=C0103
        for coder_segs in group.values():
            coders = coder_segs.keys()
            for m in range(0, len(coders)):
                for n in range(m+1, len(coders)):
                    segs_m = coder_segs[coders[m]]
                    segs_n = coder_segs[coders[n]]
                    values.append(float(percentage(segs_m, segs_n)))
    # Parse by groups, or not
    if groups:
        for segs_dict_all_g in segs_dict_all.values():
            per_group(segs_dict_all_g, values)
    else:
        per_group(segs_dict_all, values)
    # Return mean, std dev, and variance
    return mean(values), std(values), var(values)

