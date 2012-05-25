'''
Provides a segmentation version of the F-Measure metric.

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
from .Percentage import find_boundary_position_freqs
from . import fmeasure
from .. import compute_pairwise


def f_b_measure(hypothesis_masses, reference_masses, beta=1.0):
    '''
    Calculates the F-Measure between a hypothesis and reference segmentation,
    where F-Measure is calculated as:
    
    .. math::
        \\text{F}_{\\beta}\\text{-measure} = \\frac{(1 + \\beta^2) \\cdot TP}\
        {(1 + \\beta^2) \\cdot TP + \\beta^2 \\cdot FN + FP}
    
    Counts of true positives (:math:`TP`), false positives (:math:`FP`), and
    false negatives (:math:`FN`) are calculated as:
    
    .. math::
        TP = \\sum^{|hyp|}_{i=1}{\\text{tp}(hyp_i, ref_i)}, \quad
        FP = \\sum^{|hyp|}_{i=1}{\\text{fp}(hyp_i, ref_i)}, \quad
        FN = \\sum^{|hyp|}_{i=1}{\\text{fn}(hyp_i, ref_i)}
        
    .. math::
        \\text{tp}(hyp_i, ref_i) = 
        \\begin{cases}
            1    & \\text{if both } hyp_i \\text{ and } ref_i \\text{ are boundaries}  \\\\
            0    & \\text{else}
        \\end{cases}
        
    .. math::
        \\text{fp}(hyp_i, ref_i) = 
        \\begin{cases}
            1    & \\text{if } hyp_i \\text{ is a boundary and } ref_i \\text{ is not}  \\\\
            0    & \\text{else}
        \\end{cases}
        
    .. math::
        \\text{fn}(hyp_i, ref_i) = 
        \\begin{cases}
            1    & \\text{if is not a boundary } hyp_i \\text{ and } ref_i \\text{ is}  \\\\
            0    & \\text{else}
        \\end{cases}
    
    Each matching boundary position is considered a TP, whereas a missing
    boundary in the hypothesis is considered a FN, and an extra boundary in the
    hypothesis that is not found in the reference is considered a FP.  TNs
    do not occur.
    
    :param hypothesis_masses: Hypothesis segmentation masses.
    :param reference_masses: Reference segmentation masses.
    :param beta: Scales how precision and recall are averaged.
    :type hypothesis_masses: list
    :type reference_masses: list
    :type beta: float
    
    :returns: F-measure.
    :rtype: :class:`decimal.Decimal`
    
    .. seealso:: :func:`segeval.ml.fmeasure`
    '''
    # pylint: disable=C0103
    positions_hyp = find_boundary_position_freqs([hypothesis_masses])
    positions_ref = find_boundary_position_freqs([reference_masses])
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
    return fmeasure(tp, fp, fn, beta)


def pairwise_f_b_measure(dataset_masses):
    '''
    Calculate mean pairwise segmentation F-Measure.
    
    .. seealso:: :func:`f_b_measure`
    .. seealso:: :func:`segeval.compute_pairwise`
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :type dataset_masses: dict
    
    :returns: Mean, standard deviation, and variance.
    :rtype: :class:`decimal.Decimal`, :class:`decimal.Decimal`, :class:`decimal.Decimal`
    '''
    return compute_pairwise(dataset_masses, f_b_measure, permuted=False)

