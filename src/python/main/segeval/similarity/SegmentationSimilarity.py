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
from .distance.SingleBoundaryDistance import linear_edit_distance
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
    :param return_parts:      Scales how precision and recall are averaged.
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
            linear_edit_distance(segment_masses_a, segment_masses_b, n)[1:3]
        
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


def pairwise_similarity(dataset_masses, n=DEFAULT_N, weight=DEFAULT_WEIGHT,
                        scale_transp=DEFAULT_SCALE, return_parts=False):
    '''
    Calculate mean pairwise S.
    
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
    def wrapper(segment_masses_a, segment_masses_b, return_parts=return_parts):
        '''
        Wrapper to provide parameters.
        '''
        return similarity(segment_masses_a, segment_masses_b, n, weight,
                  scale_transp, return_parts)
    
    return compute_pairwise(dataset_masses, wrapper, permuted=DEFAULT_PERMUTED)


def pairwise_similarity_micro(dataset_masses, n=DEFAULT_N,
                              weight=DEFAULT_WEIGHT,
                              scale_transp=DEFAULT_SCALE):
    '''
    Calculate mean pairwise S.
    
    .. seealso:: :func:`similarity`
    .. seealso:: :func:`segeval.compute_pairwise`
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :type dataset_masses: dict
    
    :returns: Mean (micro)
    :rtype: :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103,R0913,R0914
    def wrapper(segment_masses_a, segment_masses_b, return_parts=True):
        '''
        Wrapper to provide parameters.
        '''
        return similarity(segment_masses_a, segment_masses_b, n, weight,
                  scale_transp, return_parts)
    
    pairs = compute_pairwise_values(dataset_masses, wrapper,
                                   permuted=DEFAULT_PERMUTED,
                                   return_parts=True)
    
    
    pbs_unedited, pbs_total = 0, 0
    for values in pairs.values():
        cur_pbs_unedited, cur_pbs_total = values[0:2]
        pbs_unedited += cur_pbs_unedited
        pbs_total += cur_pbs_total
    
    return Decimal(pbs_unedited) / Decimal(pbs_total)


OUTPUT_NAME = 'Mean S metric'
SHORT_NAME  = 'S'


def values_s_detailed(dataset_masses, n=DEFAULT_N, weight=DEFAULT_WEIGHT,
                      scale_transp=DEFAULT_SCALE):
    '''
    Produces a TSV for this metric
    '''
    # pylint: disable=C0103
    header = list(['coder1', 'coder2', 'error', 'edits', 'boundaries', 'n'])
    def wrapper(segment_masses_a, segment_masses_b, return_parts):
        '''
        Wrapper to provide parameters.
        '''
        return similarity(segment_masses_a, segment_masses_b, n, weight,
                  scale_transp, return_parts)
    # Get values
    values = compute_pairwise_values(dataset_masses, wrapper, return_parts=True)
    adjusted_values = dict()
    for label, value in values.items():
        subvalues = list()
        set_errors, set_transpositions = value[4:6]
        # For set errors
        for _ in set_errors:
            subvalues.append(['sub', 1, 1, 1])
        # For transposition errors
        for set_transposition in set_transpositions:
            subvalues.append(['transp', 1, set_transposition.boundaries,
                             set_transposition.n])
        adjusted_values[label] = subvalues
    return create_tsv_rows(header, adjusted_values, expand=True)


def values_s(dataset_masses, n=DEFAULT_N, weight=DEFAULT_WEIGHT,
                      scale_transp=DEFAULT_SCALE):
    '''
    Produces a TSV for this metric
    '''
    # pylint: disable=C0103
    header = list(['coder1', 'coder2', 'pbs_unedited', 'pbs_total', \
                   'sub_edits', 'transp_edits', SHORT_NAME])
    def wrapper(segment_masses_a, segment_masses_b, return_parts):
        '''
        Wrapper to provide parameters.
        '''
        return similarity(segment_masses_a, segment_masses_b, n, weight,
                  scale_transp, return_parts)
    # Get values
    values = compute_pairwise_values(dataset_masses, wrapper, return_parts=True)
    adjusted_values = dict()
    for label, value in values.items():
        # Get values
        pbs_unedited, pbs_total, total_set_errors, \
                total_set_transpositions = value[0:4]
        s = Decimal(pbs_unedited) / Decimal(pbs_total)
        # Store values
        adjusted_values[label] = [pbs_unedited, pbs_total, total_set_errors, \
                total_set_transpositions, s]
    return create_tsv_rows(header, adjusted_values)


def parse(args):
    '''
    Parse this module's metric arguments and perform requested actions.
    '''
    # pylint: disable=C0103,R0914
    output = None
    values = load_file(args)
    # Parse args
    n  = args['n']
    wt = args['wt']
    ws = args['ws']
    te = args['te']
    weight = DEFAULT_WEIGHT
    micro = args['micro']
    if wt != 1.0 or ws != 1.0:
        weight = (ws, wt)
    # Is a TSV requested?
    if args['output'] != None:
        # Create a TSV
        output_file = args['output'][0]
        if args['detailed']:
            header, rows = values_s_detailed(values, n, weight, te)
        else:
            header, rows = values_s(values, n, weight, te)
        write_tsv(output_file, header, rows)
    elif micro:
        # Create a string to output
        mean = pairwise_similarity_micro(values, n, weight, te)
        output = render_mean_micro_values(SHORT_NAME, mean)
    else:
        # Create a string to output
        mean, std, var, stderr, n = pairwise_similarity(values, n, weight, te)
        output = render_mean_values(SHORT_NAME, mean, std, var, stderr, n)
    # Return
    return output


def parser_s_support(parser):
    '''
    Add support for S parameters
    
    :param parser: Argument parser
    :type parser: argparse.ArgumentParser
    '''
    parser.add_argument('-n',
                        type=int,
                        default=DEFAULT_N,
                        help='The maximum number of PBs that boundaries can '+\
                              'span to be considered transpositions (n<2 '+\
                              ('means no transpositions); default is %i.' \
                                    % DEFAULT_N))
    parser.add_argument('-wt',
                        type=float,
                        default=DEFAULT_WEIGHT[0],
                        help='Weight, 0 <= wt <= 1, to scale transposition '+\
                            'error by; default is 1 (no scaling).')
    parser.add_argument('-ws',
                        type=float,
                        default=DEFAULT_WEIGHT[0],
                        help='Weight, 0 <= wt <= 1, to scale substitution '+\
                            'error by; default is 1 (no scaling).')
    parser.add_argument('-te',
                        type=bool,
                        default=DEFAULT_SCALE,
                        help='Scale transpositions by their size and the '+\
                            'number of boundaries the span; %s by default' \
                            % str(DEFAULT_SCALE))


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    from ..data import parser_add_file_support
    from .. import parser_micro_support
    parser = subparsers.add_parser('s',
                                   help=OUTPUT_NAME)
    parser_add_file_support(parser)
    parser_s_support(parser)
    parser_micro_support(parser)
    parser.add_argument('-de', '--detailed',
                        action='store_true',
                        default=False,
                        help='When specifying an output TSV file, specify '+\
                            'this to obtain a detailed error breakdown per '+\
                            'edit')
    parser.set_defaults(func=parse)

