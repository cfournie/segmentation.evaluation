'''
Implementation of the WinPR segmentation evaluation metric described in:

Scaiano, M., & Inkpen, D. (n.d.). Revisiting Evaluation Measure for
Segmentation Evaluation.

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
from numpy import mean, std, var
from .WindowDiff import compute_window_size
from ..ml import fscore
from .. import SegmentationMetricError
from .. import convert_masses_to_segments


def win_pr(ref_segments, hyp_segments, window_size=None, return_fscore=False,
           beta=1.0):
    '''
    Calculates the WinPR segmentation evaluation metric confusion matrix for a
    hypothetical segmentation against a reference segmentation for a given
    window size.  The standard WindowDiff method of calculating the window size
    is performed a window size is not specified.
    
    Arguments:
    ref_segments  -- An ordered sequence of which section each unit belongs to,
                     e.g.: [1,1,1,1,1,2,2,2,3,3,3,3,3], for 13 units (e.g.
                     sentences, paragraphs).  This is the reference segmentation
                     used to compare a hypothetical segmentation against.
    hyp_segments  -- An ordered sequence of which section each unit belongs to.
                     This is the hypothetical segmentation that is compared
                     against the reference ca.chrisfournier.nlp.methods.segmentation.
    window_size   -- The size of the window that is slid over the two
                     segmentations used to count mismatches.
    return_fscore -- If True, specifies that an F-score is to be returned.
    '''
    if len(ref_segments) != len(hyp_segments):
        raise SegmentationMetricError(
                    'Reference and hypothesis segmentations differ in length.')
    # Compute window size to use if unspecified
    if window_size is None:
        window_size = compute_window_size(ref_segments)
    # Create a set of pairs of units from each segmentation to go over using a
    # window
    tp,fp,fn = [0]*3
    tn = (-1 * window_size) * (window_size - 1)
    # Create and append phantom boundaries at the beginning and end of the
    # segmentation to properly count boundaries at the beginning and end
    phantom = [0]*(window_size-1)
    units_ref_hyp = zip(phantom+ref_segments+phantom,
                        phantom+hyp_segments+phantom)
    # Slide window over and calculate TP, TN, FP, FN
    for i in xrange(0,len(units_ref_hyp) - window_size + 1):
        window = units_ref_hyp[i:i+window_size]
        ref_boundaries = 0
        hyp_boundaries = 0
        # For pair in window
        for j in xrange(0,len(window)-1):
            ref_part,hyp_part = zip(*window[j:j+2])
            # Boundary exists in the reference segmentation
            if ref_part[0] != ref_part[1]:
                ref_boundaries += 1
            # Boundary exists in the hypothesis segmentation
            if hyp_part[0] != hyp_part[1]:
                hyp_boundaries += 1
        # If the number of boundaries per segmentation in the window differs
        tp += min(ref_boundaries,hyp_boundaries)
        fp += max(0, hyp_boundaries - ref_boundaries)
        fn += max(0, ref_boundaries - hyp_boundaries)
        tn += (window_size - max(ref_boundaries,hyp_boundaries))
    # Return the constituent statistics
    if not return_fscore:
        return tp,fp,fn,tn
    else:
        return fscore(tp,fp,fn, beta)


def pairwise_winpr(segs_dict_all, groups=False):
    values = list()
    # Define fnc per group
    def per_group(group, values):
        for coder_segs in group.values():
            coders = coder_segs.keys()
            for m in range(0,len(coders)):
                for n in range(m+1,len(coders)):
                    segs_m = convert_masses_to_segments(coder_segs[coders[m]])
                    segs_n = convert_masses_to_segments(coder_segs[coders[n]])
                    tp,fp,fn = win_pr(segs_m,segs_n)[0:3]
                    f_1mn = fscore(tp,fp,fn)
                    tp,fp,fn = win_pr(segs_n,segs_m)[0:3]
                    f_1nm = fscore(tp,fp,fn)
                    values.append(float(f_1mn))
                    values.append(float(f_1nm))
    # Parse by groups, or not
    if groups:
        for segs_dict_all_g in segs_dict_all.values():
            per_group(segs_dict_all_g, values)
    else:
        per_group(segs_dict_all, values)
    # Return mean, std dev, and variance
    return mean(values),std(values),var(values)

