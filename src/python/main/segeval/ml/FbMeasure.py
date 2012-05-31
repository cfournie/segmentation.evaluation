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
from . import fmeasure, precision as ml_precision, recall as ml_recall
from .. import compute_pairwise


DEFAULT_BETA = 1.0


def f_b_measure(hypothesis_masses, reference_masses, beta=DEFAULT_BETA):
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
    return fmeasure(tp, fp, fn, beta)


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
    positions_hyp = find_boundary_position_freqs([hypothesis_masses])
    positions_ref = find_boundary_position_freqs([reference_masses])
    tp = 0
    fp = 0
    for pos in positions_ref.keys():
        if pos in positions_hyp:
            tp += 1
    for pos in positions_hyp.keys():
        if pos not in positions_ref:
            fp += 1
    return ml_precision(tp, fp)


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
    positions_hyp = find_boundary_position_freqs([hypothesis_masses])
    positions_ref = find_boundary_position_freqs([reference_masses])
    tp = 0
    fn = 0
    for pos in positions_ref.keys():
        if pos in positions_hyp:
            tp += 1
        else:
            fn += 1
    return ml_recall(tp, fn)


def pairwise_f_b_measure(dataset_masses, beta=DEFAULT_BETA, permuted=True):
    '''
    Calculate mean pairwise segmentation F-Measure.
    
    .. seealso:: :func:`f_b_measure`
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
        return f_b_measure(hypothesis_masses, reference_masses, beta)
    return compute_pairwise(dataset_masses, wrapper, permuted=permuted)


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
    return compute_pairwise(dataset_masses, fnc, permuted=False)


OUTPUT_NAME_F = 'Pairwise Mean F_beta Measure'
OUTPUT_NAME_R = 'Pairwise Mean Recall'
OUTPUT_NAME_P = 'Pairwise Mean Precision'
SHORT_NAME_F  = 'F_%s'
SHORT_NAME_R  = 'R'
SHORT_NAME_P  = 'P'


def parse(args):
    '''
    Parse this module's metric arguments and perform requested actions.
    '''
    from ..data import load_file
    from ..data.Display import render_mean_values
    values = load_file(args)[0]
    
    subparser = args['subparser_name']
    if subparser == 'f':
        beta = args['beta']
        mean, std, var, stderr = pairwise_f_b_measure(values, beta)
        name = SHORT_NAME_F % str(beta)
    elif subparser == 'r':
        mean, std, var, stderr = pairwise_ml_measure(values, fnc=recall)
        name = SHORT_NAME_R
    elif subparser == 'p':
        mean, std, var, stderr = pairwise_ml_measure(values, fnc=precision)
        name = SHORT_NAME_P
    
    return render_mean_values(name, mean, std, var, stderr)


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
    parser_f = subparsers.add_parser('f',
                                   help=OUTPUT_NAME_F)
    parser_add_file_support(parser_f)
    parser_f.set_defaults(func=parse)
    parser_beta_support(parser_f)
    parser = subparsers.add_parser('r',
                                   help=OUTPUT_NAME_R)
    parser_add_file_support(parser)
    parser.set_defaults(func=parse)

    parser = subparsers.add_parser('p',
                                   help=OUTPUT_NAME_P)
    parser_add_file_support(parser)
    parser.set_defaults(func=parse)

