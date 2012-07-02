'''
Implementation of the Pk segmentation evaluation metric described in 
[BeefermanBerger1999]_

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
from . import compute_window_size, parser_one_minus_support
from .. import SegmentationMetricError, compute_pairwise, \
    convert_masses_to_positions, compute_pairwise_values, create_tsv_rows
from ..data import load_file
from ..data.TSV import write_tsv
from ..data.Display import render_mean_values, render_mean_micro_values, \
    render_permuted


DEFAULT_PERMUTED = True


def pk(hypothesis_positions, reference_positions, window_size=None,
       one_minus=False, convert_from_masses=False, return_parts=False):
    '''
    Calculates the Pk segmentation evaluation metric score for a
    hypothetical segmentation against a reference segmentation for a given
    window size.  The standard method of calculating the window size
    is performed if a window size is not specified.
    
    :param hypothesis_positions: Hypothesis segmentation section labels
                                    sequence.
    :param reference_positions:  Reference segmentation section labels sequence.
    :param window_size:          The size of the window that is slid over the \
                                    two segmentations used to count mismatches \
                                    (default is None and will use the average \
                                    window size)
    :param one_minus:            Return 1-Pk to make it no longer a \
                                    penalty-metric.
    :param convert_from_masses:  Convert the segmentations provided from \
                                    masses into positions.
    :type hypothesis_positions: list
    :type reference_positions: list
    :type window_size: int
    :type one_minus: bool
    :type convert_from_masses: bool
    
    .. note:: See :func:`segeval.convert_masses_to_positions` for an example of
              the input format.
    '''
    # pylint: disable=C0103,R0913
    # Convert from masses into positions 
    if convert_from_masses:
        reference_positions  = convert_masses_to_positions(reference_positions)
        hypothesis_positions = convert_masses_to_positions(hypothesis_positions)
    # Check for input errors
    if len(reference_positions) != len(hypothesis_positions):
        raise SegmentationMetricError(
                    'Reference and hypothesis segmentations differ in position \
length (%(ref)i != %(hyp)i).' % {'ref' : len(reference_positions),
                                 'hyp' : len(hypothesis_positions)})
    # Compute window size to use if unspecified
    if window_size is None:
        window_size = compute_window_size(reference_positions)
    # Create a set of pairs of units from each segmentation to go over using a
    # window
    sum_differences = 0
    # Slide window over and sum the number of varying windows
    measurements = 0
    for i in xrange(0, len(reference_positions) - (window_size)):
        # Create probe windows with k boundaries inside
        window_ref = reference_positions[i:i+window_size+1]
        window_hyp = hypothesis_positions[i:i+window_size+1]
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
        if return_parts:
            return sum_differences, measurements
        else:
            return p_k
    else:
        return Decimal('1.0') - p_k


def pairwise_pk(dataset_masses, one_minus=False, convert_from_masses=True):
    '''
    Calculate mean pairwise segmentation F-Measure.
    
    .. seealso:: :func:`pk`
    .. seealso:: :func:`segeval.compute_pairwise`
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :type dataset_masses: dict
        
    :returns: Mean, standard deviation, variance, and standard error of a \
        segmentation metric.
    :rtype: :class:`decimal.Decimal`, :class:`decimal.Decimal`, \
        :class:`decimal.Decimal`, :class:`decimal.Decimal`
    '''
    def wrapper(hypothesis_masses, reference_masses):
        '''
        Wrapper to provide parameters.
        '''
        return pk(hypothesis_masses, reference_masses, one_minus=one_minus,
                  convert_from_masses=convert_from_masses)
    
    return compute_pairwise(dataset_masses, wrapper, permuted=DEFAULT_PERMUTED)


def pairwise_pk_micro(dataset_masses, one_minus=False,
                      convert_from_masses=True):
    '''
    Calculate mean (micro) pairwise pk.
    
    .. seealso:: :func:`percentage`
    .. seealso:: :func:`segeval.compute_pairwise`
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :type dataset_masses: dict
        
    :returns: Mean (micro)
    :rtype: :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103
    def wrapper(hypothesis_masses, reference_masses, return_parts=True):
        '''
        Wrapper to provide parameters.
        '''
        return pk(hypothesis_masses, reference_masses, one_minus=False,
                  convert_from_masses=convert_from_masses,
                  return_parts=return_parts)
    pairs = compute_pairwise_values(dataset_masses, wrapper,
                                    return_parts=True)
    
    windows, total = 0, 0
    for values in pairs.values():
        cur_windows, cur_total = values
        windows += cur_windows
        total += cur_total
    
    p_k = Decimal(windows) / Decimal(total)
    
    if one_minus:
        return Decimal('1.0') - p_k
    else:
        return p_k


OUTPUT_NAME = render_permuted('Mean Pk value', DEFAULT_PERMUTED)
SHORT_NAME  = 'Pk'


def values_pk(dataset_masses, name, one_minus):
    '''
    Produces a TSV for this metric
    '''
    # Define a fnc to pass parameters
    def wrapper(hypothesis_masses, reference_masses):
        '''
        Wrapper to provide parameters.
        '''
        return pk(hypothesis_masses, reference_masses, one_minus=one_minus,
                  convert_from_masses=True)
    # Get values
    header = list(['coder1', 'coder2', name])
    values = compute_pairwise_values(dataset_masses, wrapper,
                                     permuted=DEFAULT_PERMUTED)
    return create_tsv_rows(header, values)


def parse(args):
    '''
    Parse this module's metric arguments and perform requested actions.
    '''
    # pylint: disable=C0103
    output = None
    values = load_file(args)
    one_minus = args['oneminus']
    micro = args['micro']
    name = SHORT_NAME
    
    if one_minus:
        name = '1 - %s' % name
    
    # Is a TSV requested?
    if args['output'] != None:
        # Create a TSV
        output_file = args['output'][0]
        header, rows = values_pk(values, name, one_minus)
        write_tsv(output_file, header, rows)
    elif micro:
        mean = pairwise_pk_micro(values, one_minus=one_minus)
        output = render_mean_micro_values(name, mean)
    else:
        # Create a string to output
        mean, std, var, stderr, n = pairwise_pk(values, one_minus)
        output = render_mean_values(name, mean, std, var, stderr, n)
    return output


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    from ..data import parser_add_file_support
    from .. import parser_micro_support
    parser = subparsers.add_parser('pk',
                                   help=OUTPUT_NAME)
    parser_add_file_support(parser)
    parser_one_minus_support(parser)
    parser_micro_support(parser)
    parser.set_defaults(func=parse)

