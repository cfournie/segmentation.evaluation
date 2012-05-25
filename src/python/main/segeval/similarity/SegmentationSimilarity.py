'''
Segmentation similarity evaluation metric functions.

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
from .distance.SingleBoundaryDistance import linear_edit_distance
from .. import SegmentationMetricError
from ..Math import mean, std, var


def similarity(segs_a, segs_b, n=2, weight=(1, 1), scale_transpositions=True,
               return_parts=False):
    # pylint: disable=C0103,R0913,R0914
    '''
    Calculates similarity between two sequences of segment masses where complete
    similarity is 1.0 (identical), 50% of min number of transformations required
    to change the mass of one to another is 0.5, and 100% of the min number of
    transformations required to change the mass of one to another results in 0.
    
    When evaluating segmentation, use this chart as a rule of thumb:
    
    1.0               --  Complete similarity  
    1.0 >  sim > 0.9  --  High similarity
    0.9 >= sim > 0.7  --  Moderate similarity
    0.7 >= sim > 0.6  --  Poor similarity
    0.6 >= sim > 0.4  --  Very Poor similarity
    0.4 >= sim > 0.3  --  Poor dissimilarity
    0.3 >= sim > 0.2  --  Moderate dissimilarity
    0.2 >= sim > 0.0  --  High dissimilarity
    0.0 == sim        --  Complete dissimilarity
    
    Arguments:
    segment_a            -- mass segment sequence (e.g. [1,2,3,3,2,1])
    segment_b            -- mass segment sequence (e.g. [1,2,2,4,2,1])
    n                    -- The maximum window size in which to consider 
                            transpositions (n=1 means no transpositions)
    weight               -- Weighting factor to multiple by:
                            (substitutions, transpositions)
    scale_transpositions -- If true, scales transpositions by their size and the
                            number of boundaires (see trp(n,b) in the paper)
    return_parts         -- If true, return the numerator and denominator of
                            what would constitute the similarity, else specifies
                            that the similarity is to be returned (default:
                            False)
    
    Returns:
    if return_parts is False:
        Similarity, where 0.0 >= sim >= 1.0.
    else:
        The mass unmoved, and the total mass
    '''
    # Total number of segments to be evaluated
    if len(segs_a) == 0 and len(segs_b) == 0:
        if return_parts:
            return 0, 0
        else:
            return Decimal('1.0')
    elif sum(segs_a) != sum(segs_b):
        raise SegmentationMetricError('Unequal segmentation masses (%i != %i)' \
                                      % (sum(segs_a), sum(segs_b)))
    elif 0 in segs_a or 0 in segs_b:
        raise SegmentationMetricError('Non-plausable mass 0 present')
    else:
        # Compute total pbs
        pbs_total = sum(segs_a) - 1
        
        # Compute edit distance
        set_transpositions, set_errors, set_transpositions_details = \
            linear_edit_distance(segs_a, segs_b, n)[1:4]
        
        # Scale transpositions
        if scale_transpositions:
            set_transpositions = Decimal(0)
            for transposition in set_transpositions_details:
                set_transpositions += transposition.te()
        
        # Apply weights
        weight_s = Decimal(weight[0])
        weight_t = Decimal(weight[1])
        set_errors         *= weight_s
        set_transpositions *= weight_t
        
        pbs_unedited = pbs_total - (set_errors + set_transpositions)
        
        if return_parts:
            # Return the total sum of unmoved mass during all transformations,
            # and the total mass
            return pbs_unedited, pbs_total, \
                set_errors, set_transpositions
        else:
            # Return the total sum of unmoved mass during all transformations \
            # over the total mass
            return pbs_unedited / pbs_total


def pairwise_similarity(segs_dict_all, groups=False):
    '''
    Computes pairwise mean similarity.
    
    Arguments:
    segs_dict_all -- dict of {groups : { chapters : {annotators : segs} } }
    groups        -- True if the segs_dict_all contains multiple groups, False
                     if the dict does not contain groups (just chapters for one
                     group).
    
    Returns:
    The mean, standard deviation, and variance of pairwise similarity with the
    total number of substitutions and transpositions performed (full and near
    misses).
    '''
    values = list()
    total_substitutions  = 0
    total_transpositions = 0
    # Define fnc per group
    def per_group(group, values):
        '''
        Computes pairwise similarity for a group.
        
        Arguments:
        group  -- segmentation for a group of coders (all coders have segmented
                  all items)
        values -- list of total similarity values computed (is appended to)
        '''
        total_substitutions  = 0
        total_transpositions = 0
        for coder_segs in group.values():
            coders = coder_segs.keys()
            for m in range(0, len(coders)):         # pylint: disable=C0103
                for n in range(m+1, len(coders)):   # pylint: disable=C0103
                    segs_m = coder_segs[coders[m]]
                    segs_n = coder_segs[coders[n]]
                    boundaries_unmoved, boundaries_total, \
                    substitutions, transpositions = \
                        similarity(segs_m, segs_n, return_parts=True)
                    sim = float(Decimal(boundaries_unmoved) / boundaries_total)
                    total_substitutions  += substitutions
                    total_transpositions += transpositions
                    values.append(sim)
        return total_substitutions, total_transpositions
    # Parse by groups, or not
    if groups:
        for segs_dict_all_g in segs_dict_all.values():
            substitutions, transpositions = per_group(segs_dict_all_g, values)
            total_substitutions  += substitutions
            total_transpositions += transpositions
    else:
        substitutions, transpositions = per_group(segs_dict_all, values)
        total_substitutions  += substitutions
        total_transpositions += transpositions
    # Return mean, std dev, and variance
    return mean(values), std(values), var(values), \
        total_substitutions, total_transpositions

