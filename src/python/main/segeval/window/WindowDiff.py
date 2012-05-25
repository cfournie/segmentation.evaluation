'''
Implementation of the WindowDiff segmentation evaluation metric described in:



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
from . import compute_window_size
from ..Math import mean, std, var
from .. import SegmentationMetricError
from .. import convert_masses_to_positions


def window_diff(ref_segments, hyp_segments, window_size=None, one_minus=False,
                fixed=True, lamprier_et_al_2007_fix=False):
    '''
    Calculates the WindowDiff segmentation evaluation metric score for a
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
    one_minus    -- Calculates 1-WD, turning WD into a reward metric (instead of
                    a penalty metric).
    fixed        -- Enables a fix, which deviates from the official method, but
                    allows for the implementation to range form [0,1] as
                    intended.
    
    '''
    # pylint: disable=C0103
    if len(ref_segments) != len(hyp_segments):
        raise SegmentationMetricError(
                    'Reference and hypothesis segmentations differ in length.')
    # Compute window size to use if unspecified
    if window_size is None:
        window_size = compute_window_size(ref_segments)
    # Create a set of pairs of units from each segmentation to go over using a
    # window
    sum_differences = 0
    units_ref_hyp = None
    phantom_size = window_size - 1
    if lamprier_et_al_2007_fix == False:
        units_ref_hyp = zip(ref_segments, hyp_segments)
    else:
        phantom = [0] * phantom_size
        units_ref_hyp = zip(phantom + ref_segments + phantom,
                            phantom + hyp_segments + phantom)
    # Slide window over and sum the number of varying windows
    for i in xrange(0, len(units_ref_hyp) - window_size + 1):
        window = units_ref_hyp[i:i+window_size]
        ref_boundaries = 0
        hyp_boundaries = 0
        # For pair in window
        for j in xrange(0, len(window)-1):
            ref_part, hyp_part = zip(*window[j:j+2])
            # Boundary exists in the reference segmentation
            if ref_part[0] != ref_part[1]:
                ref_boundaries += 1
            # Boundary exists in the hypothesis segmentation
            if hyp_part[0] != hyp_part[1]:
                hyp_boundaries += 1
        # If the number of boundaries per segmentation in the window differs
        if ref_boundaries != hyp_boundaries:
            sum_differences += 1
    # Perform final division
    n = len(ref_segments)
    if fixed:
        n += 1
    if lamprier_et_al_2007_fix:
        n += phantom_size
    win_diff = Decimal(sum_differences) / (n - window_size)
    if not one_minus:
        return win_diff
    else:
        return Decimal('1.0') - win_diff


def pairwise_windiff(segs_dict_all, groups=False, one_minus=False,
                     window_size=None, permute=True, fixed=True):
    # pylint: disable=C0103
    values = list()
    # Define fnc per group
    def per_group(group, values):
        for coder_segs in group.values():
            coders = coder_segs.keys()
            for m in range(0, len(coders)):
                for n in range(m+1, len(coders)):
                    segs_m = convert_masses_to_positions(
                                coder_segs[coders[m]])
                    segs_n = convert_masses_to_positions(
                                coder_segs[coders[n]])
                    values.append(Decimal(window_diff(segs_m, segs_n,
                                                    one_minus=one_minus,
                                                    window_size=window_size,
                                                    fixed=fixed)))
                    if permute:
                        values.append(Decimal(window_diff(segs_n, segs_m,
                                                        one_minus=one_minus,
                                                        window_size=\
                                                            window_size,
                                                        fixed=fixed)))
    # Parse by groups, or not
    if groups:
        for segs_dict_all_g in segs_dict_all.values():
            per_group(segs_dict_all_g, values)
    else:
        per_group(segs_dict_all, values)
    return mean(values), std(values), var(values)

