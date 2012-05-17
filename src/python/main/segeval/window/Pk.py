'''
Implementation of the Pk segmentation evaluation metric described in:

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
from . import compute_window_size
from .. import SegmentationMetricError
from .. import convert_masses_to_positions


def pk(ref_segments, hyp_segments, window_size=None, one_minus=False):
    '''
    Calculates the Pk segmentation evaluation metric score for a
    hypothetical segmentation against a reference segmentation for a given
    window size.  The standard method of calculating the window size
    is performed a window size is not specified.
    
    Arguments:
    ref_segments -- An ordered sequence of which section each unit belongs to,
                    e.g.: [1,1,1,1,1,2,2,2,3,3,3,3,3], for 13 units (e.g.
                    sentences, paragraphs).  This is the reference segmentation
                    used to compare a hypothetical segmentation against.
    hyp_segments -- An ordered sequence of which section each unit belongs to.
                    This is the hypothetical segmentation that is compared
                    against the reference segmentation.
    window_size  -- The size of the window that is slid over the two
                    segmentations used to count mismatches.
    
    '''
    if len(ref_segments) != len(hyp_segments):
        raise SegmentationMetricError(
                    'Reference and hypothesis segmentations differ in length.')
    # Compute window size to use if unspecified
    if window_size is None:
        window_size = compute_window_size(ref_segments)
    # Create a set of pairs of units from each segmentation to go over using a
    # window
    sum_differences = 0
    # Slide window over and sum the number of varying windows
    measurements = 0
    for i in xrange(0,len(ref_segments) - (window_size)):
        # Create probe windows with k boundaries inside
        window_ref = ref_segments[i:i+window_size+1]
        window_hyp = hyp_segments[i:i+window_size+1]
        # Probe agreement
        agree_ref = window_ref[0] == window_ref[-1]
        agree_hyp = window_hyp[0] == window_hyp[-1]
        # If the windows agreements agree
        if agree_ref != agree_hyp:
            sum_differences += 1
        measurements += 1
    # Perform final division
    p_k = Decimal(sum_differences) / measurements
    if not one_minus:
        return p_k
    else:
        return Decimal('1.0') - p_k


def pairwise_pk(segs_dict_all, groups=False, one_minus=False):
    values = list()
    # Define fnc per group
    def per_group(group, values):
        for coder_segs in group.values():
            coders = coder_segs.keys()
            for m in range(0,len(coders)):
                for n in range(m+1,len(coders)):
                    segs_m = convert_masses_to_positions(
                                coder_segs[coders[m]])
                    segs_n = convert_masses_to_positions(
                                coder_segs[coders[n]])
                    values.append(float(pk(segs_m,segs_n,
                                           one_minus=one_minus)))
                    values.append(float(pk(segs_n,segs_m,
                                           one_minus=one_minus)))
    # Parse by groups, or not
    if groups:
        for segs_dict_all_g in segs_dict_all.values():
            per_group(segs_dict_all_g, values)
    else:
        per_group(segs_dict_all, values)
    return mean(values),std(values),var(values)

