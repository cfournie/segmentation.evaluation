'''
Segmentation similarity evaluation metric functions [FournierInkpen2012]_.

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
from .distance.MultipleBoundary import boundary_edit_distance
from .. import SegmentationMetricError, compute_pairwise, \
    compute_pairwise_values, create_tsv_rows
from ..data import load_file
from ..data.TSV import write_tsv
from ..data.Display import render_mean_values, render_mean_micro_values


DEFAULT_N      = 2
DEFAULT_WEIGHT = (1, 1)
DEFAULT_SCALE  = True
DEFAULT_PERMUTED = False


def similarity(segment_masses_a, segment_masses_b, n=DEFAULT_N,
               weight=DEFAULT_WEIGHT, scale_transp=DEFAULT_SCALE,
               return_parts=False):
    # pylint: disable=C0103,R0913,R0914
    '''
    Calculates similarity between two sequences of segment masses using
    boundary edit distance as in [FournierInkpen2012]_.
    
    .. math::
        \\text{S}(s_{i1},s_{i2}) = \\frac
        {\\textbf{t} \cdot \\text{mass}(i) - \\textbf{t} - \\text{d}(s_{i1},s_{i2},T)}
        {\\textbf{t} \cdot \\text{mass}(i) - \\textbf{t}}
    
    :param segment_masses_a:  Segmentation masses.
    :param segment_masses_b:  Segmentation masses.
    :param n:                 The maximum number of PBs that boundaries can \
                                  span to be considered transpositions (n<2 \
                                  means no transpositions)
    :param weight:            Weights for substitution and transposition \
                                  operations
    :param scale_transp:      If true, scales transpositions by their size \
                                  and the number of boundaries
    :param return_parts:      If false, returns a :class:`decimal.Decimal`, \
                                  else, return the statistics used to create \
                                  the decimal
    :type segment_masses_a: list
    :type segment_masses_b: list
    :type n: int
    :type weight: :func:`tuple` of :func:`float` objects \
                        (substitutions,transpositions)
    :type scale_transp: bool
    :type return_parts: bool
    
    :returns: Similarity, where 0.0 <= sim <= 1.0, or the pbs unedited, total \
        pbs, substitutions and transpositions
    :rtype: :class:`decimal.Decimal`, or :func:`int`, :func:`int`, \
        :func:`int`, :func:`int`
    '''
    # Total number of segments to be evaluated
    if len(segment_masses_a) == 0 and len(segment_masses_b) == 0:
        if return_parts:
            return 0, 0
        else:
            return Decimal('1.0')
    elif sum(segment_masses_a) != sum(segment_masses_b):
        raise SegmentationMetricError('Segmentation masses differ (%i != %i)' \
                                      % (sum(segment_masses_a),
                                         sum(segment_masses_b)))
    elif 0 in segment_masses_a or 0 in segment_masses_b:
        raise SegmentationMetricError('Non-plausable mass 0 present')
    else:
        # Compute total pbs
        pbs_total = sum(segment_masses_a) - 1
        
        # Compute edit distance
        set_transpositions, set_errors = \
            boundary_edit_distance(segment_masses_a, segment_masses_b, n)[1:3]
        
        # Get totals
        total_set_transpositions = len(set_transpositions)
        total_set_errors         = len(set_errors)
        
        # Scale transpositions
        if scale_transp:
            total_set_transpositions = 0
            for set_transposition in set_transpositions:
                total_set_transpositions += set_transposition.te()
        
        # Apply weights
        if weight != DEFAULT_WEIGHT:
            weight_s = Decimal(weight[0])
            weight_t = Decimal(weight[1])
            total_set_errors         = Decimal(total_set_errors) * weight_s
            total_set_transpositions = Decimal(total_set_transpositions) * \
                                            weight_t
        
        pbs_unedited = pbs_total - (total_set_errors + total_set_transpositions)
        
        if return_parts:
            # Return the total sum of unmoved mass during all transformations,
            # and the total mass
            return pbs_unedited, pbs_total, total_set_errors, \
                total_set_transpositions, set_errors, set_transpositions
        else:
            # Return the total sum of unmoved mass during all transformations \
            # over the total mass
            return Decimal(pbs_unedited) / Decimal(pbs_total)
