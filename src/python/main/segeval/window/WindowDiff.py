'''
Implementation of the WindowDiff segmentation evaluation metric described in
[PevznerHearst2002]_ with an optional modification to fix incorrect error
counting at the beginning and end of segmentations provided by 
[LamprierEtAl2007]_.

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
from . import compute_window_size, parser_one_minus_support
from .. import SegmentationMetricError, compute_pairwise, \
    convert_masses_to_positions, compute_pairwise_values, create_tsv_rows
from ..data import load_file
from ..data.TSV import write_tsv
from ..data.Display import render_mean_values, render_mean_micro_values, \
    render_permuted


DEFAULT_PERMUTED = True


def create_paired_window(hypothesis_positions, reference_positions, window_size,
                  lamprier_et_al_2007_fix):
    '''
    Create a set of pairs of units from each segmentation to go over using a
    window.
    '''
    phantom_size = window_size - 1
    phantom_size = 1 if phantom_size <= 0 else phantom_size
    if lamprier_et_al_2007_fix == False:
        units_ref_hyp = zip(reference_positions, hypothesis_positions)
    else:
        phantom = [0] * phantom_size
        units_ref_hyp = zip(phantom + reference_positions + phantom,
                            phantom + hypothesis_positions + phantom)
    return units_ref_hyp, phantom_size


def window_diff(hypothesis_positions, reference_positions, window_size=None,
                one_minus=False, lamprier_et_al_2007_fix=False,
                convert_from_masses=False, return_parts=False):
    '''
    Calculates the WindowDiff segmentation evaluation metric score for a
    hypothetical segmentation against a reference segmentation for a given
    window size.  The standard method of calculating the window size
    is performed a window size is not specified.
    
    :param hypothesis_positions:     Hypothesis segmentation section labels
                                        sequence.
    :param reference_positions:      Reference segmentation section labels
                                        sequence.
    :param window_size:              The size of the window that is slid over \
                                        the two segmentations used to count \
                                        mismatches (default is None and will \
                                        use the average window size)
    :param one_minus:                Return 1-WindowDiff to make it no longer \
                                         a penalty-metric.
    :param lamprier_et_al_2007_fix:  Apply a fix for improperly counted errors \
                                        at the beginning and end of \
                                        segmentations, provided by \
                                        _[LamprierEtAl2007].
    :param convert_from_masses:      Convert the segmentations provided from \
                                        masses into positions.
    :type hypothesis_positions: list
    :type reference_positions: list
    :type window_size: int
    :type one_minus: bool
    :type lamprier_et_al_2007_fix: bool
    :type convert_from_masses: bool
    
    .. note:: See :func:`segeval.convert_masses_to_positions` for an example of
              the input format.
    '''
    # pylint: disable=C0103,R0913,R0914,R0912
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
    units_ref_hyp, phantom_size = create_paired_window(hypothesis_positions,
                                                       reference_positions,
                                                       window_size,
                                                       lamprier_et_al_2007_fix)
    # Slide window over and sum the number of varying windows
    sum_differences = 0
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
    n = len(reference_positions) + 1
    if lamprier_et_al_2007_fix:
        n += (phantom_size * 2)
    win_diff = Decimal(sum_differences) / (n - window_size)
    if win_diff > 1:
        raise SegmentationMetricError('Incorrect value calculated.')
    if not one_minus:
        if return_parts:
            return sum_differences, n - window_size
        else:
            return win_diff
    else:
        return Decimal('1.0') - win_diff


def pairwise_window_diff(dataset_masses, one_minus=False,
                         lamprier_et_al_2007_fix=False,
                         window_size=None,
                         convert_from_masses=True):
    '''
    Calculate mean pairwise segmentation F-Measure.
    
    .. seealso:: :func:`window_diff`
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
        return window_diff(hypothesis_masses, reference_masses,
                           window_size=window_size, one_minus=one_minus,
                           lamprier_et_al_2007_fix=lamprier_et_al_2007_fix,
                           convert_from_masses=convert_from_masses)
    
    return compute_pairwise(dataset_masses, wrapper, permuted=DEFAULT_PERMUTED)


def pairwise_window_diff_micro(dataset_masses, one_minus=False,
                               lamprier_et_al_2007_fix=False,
                               window_size=None,
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
        return window_diff(hypothesis_masses, reference_masses,
                           window_size=window_size, one_minus=False,
                           lamprier_et_al_2007_fix=lamprier_et_al_2007_fix,
                           convert_from_masses=convert_from_masses,
                           return_parts=return_parts)
    pairs = compute_pairwise_values(dataset_masses, wrapper,
                                    return_parts=True,
                                    permuted=DEFAULT_PERMUTED)
    
    windows, total = 0, 0
    for values in pairs.values():
        cur_windows, cur_total = values
        windows += cur_windows
        total += cur_total
    
    wd = Decimal(windows) / Decimal(total)
    
    if one_minus:
        return Decimal('1.0') - wd
    else:
        return wd


OUTPUT_NAME = render_permuted('Mean WindowDiff value', DEFAULT_PERMUTED)
SHORT_NAME  = 'WindowDiff'


def values_window_diff(dataset_masses, name, one_minus,
                       lamprier_et_al_2007_fix):
    '''
    Produces a TSV for this metric
    '''
    # Define a fnc to pass parameters
    def wrapper(hypothesis_masses, reference_masses):
        '''
        Wrapper to provide parameters.
        '''
        return window_diff(hypothesis_masses, reference_masses,
                           one_minus=one_minus, convert_from_masses=True,
                           lamprier_et_al_2007_fix=lamprier_et_al_2007_fix)
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
    lamprier_et_al_2007_fix = args['lamprier_et_al_2007']
    micro = args['micro']
    name = SHORT_NAME
    
    if one_minus:
        name = '1 - %s' % name
    
    # Is a TSV requested?
    if args['output'] != None:
        # Create a TSV
        output_file = args['output'][0]
        header, rows = values_window_diff(values, name, one_minus,
                                          lamprier_et_al_2007_fix)
        write_tsv(output_file, header, rows)
    elif micro:
        mean = pairwise_window_diff_micro(values, one_minus=one_minus)
        output = render_mean_micro_values(name, mean)
    else:
        # Create a string to output
        mean, std, var, stderr, n = pairwise_window_diff(values, one_minus)
        output = render_mean_values(name, mean, std, var, stderr, n)
    return output


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    from ..data import parser_add_file_support
    from .. import parser_micro_support
    parser = subparsers.add_parser('wd',
                                   help=OUTPUT_NAME)
    parser_add_file_support(parser)
    parser_one_minus_support(parser)
    parser_micro_support(parser)
    
    parser.add_argument('--lamprier_et_al_2007',
                        default=False,
                        action='store_true',
                        help='Applies the phantom-boundary fix from Lamprier \
                            et al. (2007) to properly count errors at the \
                            beginning and end of a segmentation; default is \
                            false to remain canon with existing reported \
                            values.')
    
    parser.set_defaults(func=parse)

