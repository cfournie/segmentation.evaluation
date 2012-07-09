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
from .Percentage import find_boundary_position_freqs
from . import fmeasure as ml_fmeasure, precision as ml_precision, \
    recall as ml_recall, vars_to_cf, cf_to_vars
from .. import compute_pairwise, compute_pairwise_values, create_tsv_rows
from ..data import load_file
from ..data.TSV import write_tsv
from ..data.Display import render_mean_values, render_mean_micro_values, \
    render_permuted


DEFAULT_BETA = 1.0
DEFAULT_PERMUTED = True


def confusion_matrix(hypothesis_masses, reference_masses):
    '''
    Calculates the confusion matrix (TP, FP, FN, TN) between a hypothesis
    and reference segmentation.
    
    Counts of true positives (:math:`TP`), false positives (:math:`FP`), and
    false negatives (:math:`FN`) are calculated as:
    
    .. math::
        TP = \\sum^{|hyp|}_{i=1}{\\text{tp}(hyp_i, ref_i)}, \quad
        FP = \\sum^{|hyp|}_{i=1}{\\text{fp}(hyp_i, ref_i)}, \quad
        FN = \\sum^{|hyp|}_{i=1}{\\text{fn}(hyp_i, ref_i)}
        
    .. math::
        \\text{tp}(hyp_i, ref_i) = &
        \\begin{cases}
            1    & \\text{if both } hyp_i \\text{ and } ref_i \\text{ are boundaries}  \\\\
            0    & \\text{else}
        \\end{cases} \\\\
        \\text{fp}(hyp_i, ref_i) = &
        \\begin{cases}
            1    & \\text{if } hyp_i \\text{ is a boundary and } ref_i \\text{ is not}  \\\\
            0    & \\text{else}
        \\end{cases} \\\\
        \\text{fn}(hyp_i, ref_i) = &
        \\begin{cases}
            1    & \\text{if is not a boundary } hyp_i \\text{ and } ref_i \\text{ is}  \\\\
            0    & \\text{else}
        \\end{cases} \\\\
        \\text{tn}(hyp_i, ref_i) = &
        \\begin{cases}
            1    & \\text{if both } hyp_i \\text{ and } ref_i \\text{ are not boundaries}  \\\\
            0    & \\text{else}
        \\end{cases}
    
    Each matching boundary position is considered a TP, whereas a missing
    boundary in the hypothesis is considered a FN, and an extra boundary in the
    hypothesis that is not found in the reference is considered a FP.  TNs
    do not occur.
    
    :param hypothesis_masses: Hypothesis segmentation masses
    :param reference_masses:  Reference segmentation masses
    :type hypothesis_masses: list
    :type reference_masses:  list
    
    :returns: F-measure or the values of the confusion matrix
    :rtype: :func:`int`, :func:`int`, :func:`int`, :func:`int`
    '''
    # pylint: disable=C0103
    positions_hyp = find_boundary_position_freqs([hypothesis_masses])
    positions_ref = find_boundary_position_freqs([reference_masses])
    tp = 0
    fp = 0
    fn = 0
    for pos in positions_ref.keys():
        if pos in positions_hyp:
            tp += 1
        else:
            fn += 1
    for pos in positions_hyp.keys():
        if pos not in positions_ref:
            fp += 1
    
    tn = sum(reference_masses) - 1 - len(positions_ref) - fn - fp
    
    return vars_to_cf(tp, fp, fn, tn)
        

def f_b_measure(hypothesis_masses, reference_masses, beta=DEFAULT_BETA):
    '''
    Calculates F-Measure between a hypothesis and reference segmentation,
    calculated as:
    
    .. math::
        \\text{F}_{\\beta}\\text{-measure} = \\frac{(1 + \\beta^2) \\cdot TP}\
        {(1 + \\beta^2) \\cdot TP + \\beta^2 \\cdot FN + FP}
    
    :param hypothesis_masses: Hypothesis segmentation masses
    :param reference_masses:  Reference segmentation masses
    :param beta:              Scales how precision and recall are averaged
    :type hypothesis_masses: list
    :type reference_masses:  list
    :type beta:              :func:`float` or :class:`decimal.Decimal`
    
    :returns: F-measure or the values of the confusion matrix
    :rtype: :class:`decimal.Decimal`
    
    .. seealso:: :func:`segeval.ml.fmeasure`
    '''
    # pylint: disable=C0103
    cf = confusion_matrix(hypothesis_masses, reference_masses)
    return ml_fmeasure(cf, beta)


def precision(hypothesis_masses, reference_masses):
    '''
    Calculates the precision between a hypothesis and reference segmentation,
    where precision is calculated as:
    
    .. math::
        \\text{Precision} = \\frac{TP}{TP + FP}
    
    Counts of true positives (:math:`TP`) and false negatives (:math:`FP`) are
    calculated as in :func:`f_b_measure`.
    
    :param hypothesis_masses: Hypothesis segmentation masses.
    :param reference_masses: Reference segmentation masses.
    :type hypothesis_masses: list
    :type reference_masses: list
    
    :returns: Precision.
    :rtype: :class:`decimal.Decimal`
    
    .. seealso:: :func:`segeval.ml.precision`
    '''
    # pylint: disable=C0103
    cf = confusion_matrix(hypothesis_masses, reference_masses)
    return ml_precision(cf)


def recall(hypothesis_masses, reference_masses):
    '''
    Calculates the recall between a hypothesis and reference segmentation,
    where recall is calculated as:
    
    .. math::
        \\text{Recall} = \\frac{TP}{TP + FN}
    
    Counts of true positives (:math:`TP`) and false negatives (:math:`FN`) are
    calculated as in :func:`f_b_measure`.
    
    :param hypothesis_masses: Hypothesis segmentation masses.
    :param reference_masses: Reference segmentation masses.
    :type hypothesis_masses: list
    :type reference_masses: list
    
    :returns: Precision.
    :rtype: :class:`decimal.Decimal`
    
    .. seealso:: :func:`segeval.ml.precision`
    '''
    # pylint: disable=C0103
    cf = confusion_matrix(hypothesis_masses, reference_masses)
    return ml_recall(cf)


def pairwise_ml_measure(dataset_masses, fnc=f_b_measure):
    '''
    Calculate mean pairwise segmentation F-Measure.
    
    .. seealso:: :func:`f_b_measure`
    .. seealso:: :func:`recall`
    .. seealso:: :func:`precision`
    .. seealso:: :func:`segeval.compute_pairwise`
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :type dataset_masses: dict
        
    :returns: Mean, standard deviation, variance, and standard error of a \
        segmentation metric.
    :rtype: :class:`decimal.Decimal`, :class:`decimal.Decimal`, \
        :class:`decimal.Decimal`, :class:`decimal.Decimal`
    '''
    return compute_pairwise(dataset_masses, fnc, permuted=DEFAULT_PERMUTED)


def pairwise_ml_measure_micro(dataset_masses, ml_fnc=ml_fmeasure):
    '''
    Computes the mean (micro) of a particular ml metric.
    
    .. seealso:: :func:`f_b_measure`
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :type dataset_masses: dict
        
    :returns: Mean (micro)
    :rtype: :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103
    
    pairs = compute_pairwise_values(dataset_masses, confusion_matrix)
    
    tp, fp, fn, tn = 0, 0, 0, 0
    for values in pairs.values():
        cur_tp, cur_fp, cur_fn, cur_tn =  cf_to_vars(values)
        tp += cur_tp
        fp += cur_fp
        fn += cur_fn
        tn += cur_tn
    
    return ml_fnc(vars_to_cf(tp, fp, fn, tn))


OUTPUT_NAME_F = render_permuted('Pairwise Mean F_beta measure', 
                                DEFAULT_PERMUTED)
OUTPUT_NAME_R = render_permuted('Pairwise Mean Recall value',
                                DEFAULT_PERMUTED)
OUTPUT_NAME_P = render_permuted('Pairwise Mean Precision value',
                                DEFAULT_PERMUTED)
SHORT_NAME_F  = 'F_%s'
SHORT_NAME_P  = 'P'
SHORT_NAME_R  = 'R'


def values_f_b_measure(dataset_masses, beta=DEFAULT_BETA):
    '''
    Produces a TSV for this metric
    '''
    # Define a fnc to retrieve F_Beta-Measure values
    def wrapper_f(hypothesis_masses, reference_masses, return_parts=False):
        # pylint: disable=W0613
        '''
        Wrapper to provide parameters.
        '''
        return f_b_measure(hypothesis_masses, reference_masses, beta)
    # Create header
    header = list(['coder1', 'coder2', SHORT_NAME_F % str(beta), SHORT_NAME_P, \
                   SHORT_NAME_R, 'TP', 'FP', 'FN', 'TN'])
    # Calculate values
    values_f = compute_pairwise_values(dataset_masses, wrapper_f,
                                       permuted=False)
    values_p = compute_pairwise_values(dataset_masses, precision,
                                       permuted=False)
    values_r = compute_pairwise_values(dataset_masses, recall,
                                       permuted=False)
    values_cf = compute_pairwise_values(dataset_masses, confusion_matrix,
                                        permuted=False)
    
    for label, value in values_cf.items():
        values_cf[label] = cf_to_vars(value)
    
    # Combine into one table
    combined_values = dict()
    for label in values_f.keys():
        row = list()
        row.append(values_f[label])
        row.append(values_p[label])
        row.append(values_r[label])
        row.extend(values_cf[label])
        combined_values[label] = row
    # Return
    return create_tsv_rows(header, combined_values)


def parse(args):
    '''
    Parse this module's metric arguments and perform requested actions.
    '''
    # pylint: disable=C0103,R0914
    output = None
    values = load_file(args)
    beta = 1
    micro = args['micro']
    if 'beta' in args and args['beta'] != 1:
        beta = args['beta']
    # Is a TSV requested?
    if args['output'] != None:
        # Create a TSV
        output_file = args['output'][0]
        header, rows = values_f_b_measure(values, beta)
        write_tsv(output_file, header, rows)
    elif micro:
        # Create a string to output
        subparser = args['subparser_name']
        if subparser == 'f':
            def wrapper(cf):
                '''
                Wrap ``ml_fmeasure`` so that it uses beta.
                '''
                return ml_fmeasure(cf, beta)
            mean = pairwise_ml_measure_micro(values, ml_fnc=wrapper)
            name = SHORT_NAME_F % str(beta)
        elif subparser == 'p':
            mean = pairwise_ml_measure_micro(values, ml_fnc=ml_precision)
            name = SHORT_NAME_P
        elif subparser == 'r':
            mean = pairwise_ml_measure_micro(values, ml_fnc=ml_recall)
            name = SHORT_NAME_R
        output = render_mean_micro_values(name, mean)
    else:
        # Create a string to output
        subparser = args['subparser_name']
        if subparser == 'f':
            def wrapper(hypothesis_masses, reference_masses):
                '''
                Wrap ``f_b_measure`` so that it uses beta.
                '''
                return f_b_measure(hypothesis_masses, reference_masses, beta)
            mean, std, var, stderr, n = pairwise_ml_measure(values,
                                                            fnc=wrapper)
            name = SHORT_NAME_F % str(beta)
        elif subparser == 'r':
            mean, std, var, stderr, n = pairwise_ml_measure(values,
                                                            fnc=recall)
            name = SHORT_NAME_R
        elif subparser == 'p':
            mean, std, var, stderr, n = pairwise_ml_measure(values,
                                                            fnc=precision)
            name = SHORT_NAME_P
        output = render_mean_values(name, mean, std, var, stderr, n)
    # Return
    return output


def parser_beta_support(parser):
    '''
    Add support for the "beta" parameter to allow for F_beta Measure calculation
    
    :param parser: Argument parser
    :type parser: argparse.ArgumentParser
    '''
    parser.add_argument('-b', '--beta',
                        type=float,
                        default=1.0,
                        help='Beta, the ratio of recall to precision in '+\
                             'F_beta measure; default is 1 (equal weight), '+\
                             '2 weights recall higher than precision, and '+\
                             '0.5 weights precision more than recall.')


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    from ..data import parser_add_file_support
    from .. import parser_micro_support
    parser_f = subparsers.add_parser('f',
                                   help=OUTPUT_NAME_F)
    parser_add_file_support(parser_f)
    parser_f.set_defaults(func=parse)
    parser_beta_support(parser_f)
    parser_micro_support(parser_f)
    parser_r = subparsers.add_parser('r',
                                   help=OUTPUT_NAME_R)
    parser_add_file_support(parser_r)
    parser_micro_support(parser_r)
    parser_r.set_defaults(func=parse)

    parser_p = subparsers.add_parser('p',
                                   help=OUTPUT_NAME_P)
    parser_add_file_support(parser_p)
    parser_micro_support(parser_p)
    parser_p.set_defaults(func=parse)

