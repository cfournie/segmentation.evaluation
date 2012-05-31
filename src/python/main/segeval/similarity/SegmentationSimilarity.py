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
from .. import SegmentationMetricError, compute_pairwise


DEFAULT_N      = 2
DEFAULT_WEIGHT = (1, 1)
DEFAULT_SCALE  = True


def similarity(hypothesis_masses, reference_masses, n=DEFAULT_N,
               weight=DEFAULT_WEIGHT, scale_transp=DEFAULT_SCALE,
               return_parts=False):
    # pylint: disable=C0103,R0913,R0914
    '''
    Calculates similarity between two sequences of segment masses using
    boundary edit distance as in _[FournierInkpen2012].
    
    When evaluating segmentation, use this chart as a rule of thumb:
    
    
    :param hypothesis_masses: Hypothesis segmentation masses.
    :param reference_masses:  Reference segmentation masses.
    :param n:                 The maximum number of units that boundaries can \
                                  span to be considered transpositions (n<2 \
                                  means no transpositions)
    :param beta:              Scales how precision and recall are averaged.
    :param scale_transp:      If true, scales transpositions by their size \
                                  and the number of boundaires
    :param return_parts:      Scales how precision and recall are averaged.
    :type hypothesis_masses: list
    :type reference_masses: list
    :type beta: float
    :type beta: tuple
    :type beta: bool
    :type beta: bool

    Returns:
    if return_parts is False:
        
    else:
        The mass unmoved, and the total mass
    
    :returns: Similarity, where 0.0 <= sim <= 1.0, or the pbs unedited, total \
        pbs, substitutions and transpositions
    :rtype: :class:`decomal.Decimal`, or :func:`int`, :func:`int`, \
        :func:`int`, :func:`int`
    '''
    # Total number of segments to be evaluated
    if len(hypothesis_masses) == 0 and len(reference_masses) == 0:
        if return_parts:
            return 0, 0
        else:
            return Decimal('1.0')
    elif sum(hypothesis_masses) != sum(reference_masses):
        raise SegmentationMetricError('Unequal segmentation masses (%i != %i)' \
                                      % (sum(hypothesis_masses),
                                         sum(reference_masses)))
    elif 0 in hypothesis_masses or 0 in reference_masses:
        raise SegmentationMetricError('Non-plausable mass 0 present')
    else:
        # Compute total pbs
        pbs_total = sum(hypothesis_masses) - 1
        
        # Compute edit distance
        set_transpositions, set_errors, set_transpositions_details = \
            linear_edit_distance(hypothesis_masses, reference_masses, n)[1:4]
        
        # Scale transpositions
        if scale_transp:
            set_transpositions = 0
            for transposition in set_transpositions_details:
                set_transpositions += transposition.te()
        
        # Apply weights
        if weight != DEFAULT_WEIGHT:
            weight_s = Decimal(weight[0])
            weight_t = Decimal(weight[1])
            set_errors         = Decimal(set_errors) * weight_s
            set_transpositions = Decimal(set_transpositions) * weight_t
        
        pbs_unedited = pbs_total - (set_errors + set_transpositions)
        
        if return_parts:
            # Return the total sum of unmoved mass during all transformations,
            # and the total mass
            return pbs_unedited, pbs_total, \
                set_errors, set_transpositions
        else:
            # Return the total sum of unmoved mass during all transformations \
            # over the total mass
            return Decimal(pbs_unedited) / Decimal(pbs_total)


def pairwise_similarity(dataset_masses, n=DEFAULT_N, weight=DEFAULT_WEIGHT,
                        scale_transp=DEFAULT_SCALE):
    '''
    Calculate mean pairwise segmentation F-Measure.
    
    .. seealso:: :func:`similarity`
    .. seealso:: :func:`segeval.compute_pairwise`
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :type dataset_masses: dict
        
    :returns: Mean, standard deviation, variance, and standard error of a \
        segmentation metric.
    :rtype: :class:`decimal.Decimal`, :class:`decimal.Decimal`, \
        :class:`decimal.Decimal`, :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103,R0913,R0914
    def wrapper(hypothesis_masses, reference_masses):
        '''
        Wrapper to provide parameters.
        '''
        return similarity(hypothesis_masses, reference_masses, n, weight,
                  scale_transp)
    
    return compute_pairwise(dataset_masses, wrapper, permuted=False)


OUTPUT_NAME = 'Mean S'
SHORT_NAME  = 'S'


def parse(args):
    '''
    Parse this module's metric arguments and perform requested actions.
    '''
    from ..data import load_file
    from ..data.Display import render_mean_values
    values = load_file(args)[0]
    
    mean, std, var, stderr = pairwise_similarity(values)
    name = SHORT_NAME
    
    return render_mean_values(name, mean, std, var, stderr)


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    from ..data import parser_add_file_support
    parser = subparsers.add_parser('s',
                                   help=OUTPUT_NAME)
    parser_add_file_support(parser)
    parser.set_defaults(func=parse)

