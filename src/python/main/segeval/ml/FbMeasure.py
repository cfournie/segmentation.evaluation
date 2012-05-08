'''
F-Measure metric functions.

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
from .Percentage import find_seg_positions
from . import fscore


def f_b_measure(segs_hypothesis, segs_reference):
    '''
    Calculates the F-Measure between a hypothesis, and reference segmentation.
    
    .. math::
        \text{F}_{\beta}\text{-measure}
    
    Arguments:
    segs_hypothesis -- Hypothesis segmentation masses
    segs_reference  -- Reference segmentation masses
    
    Returns:
    F-Measure.
    '''
    # pylint: disable=C0103
    positions_hyp = find_seg_positions([segs_hypothesis])
    positions_ref = find_seg_positions([segs_reference])
    tp = Decimal('0')
    fp = Decimal('0')
    fn = Decimal('0')
    for pos in positions_ref.keys():
        if pos in positions_hyp:
            tp += 1
        else:
            fn += 1
    for pos in positions_hyp.keys():
        if pos not in positions_ref:
            fp += 1
    return fscore(tp, fp, fn, beta=1.0)


def pairwise_f_b_measure(segs_dict_all, groups=False):
    '''
    Calculate mean pairwise segmentation F-Measure.
    
    Arguments:
    segs_dict_all -- Dict of groups containing coders and segmentations (or just
                     the group contents)
    groups        -- True if segs_dict_all is split into groups, false if not
    
    Returns:
    Mean, standard deviation, and variance of segmentation F-Measure.
    '''
    # pylint: disable=C0103
    values = list()
    # Define fnc per group
    def per_group(group, values):
        '''
        Calculate pairwise segmentation F-Measure for each group and append to
        output.
        
        Arguments:
        group  -- Dict of coders and segmentation masses
        values -- list of output segmentation F-Measures
        '''
        for coder_segs in group.values():
            coders = coder_segs.keys()
            for m in range(0, len(coders)):
                for n in range(m+1, len(coders)):
                    segs_m = coder_segs[coders[m]]
                    segs_n = coder_segs[coders[n]]
                    values.append(float(f_b_measure(segs_m, segs_n)))
    # Parse by groups, or not
    if groups:
        for segs_dict_all_g in segs_dict_all.values():
            per_group(segs_dict_all_g, values)
    else:
        per_group(segs_dict_all, values)
    # Return mean, std dev, and variance
    return mean(values), std(values), var(values)

