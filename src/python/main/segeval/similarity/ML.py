'''
Provides a segmentation similarity based precision, recall, and F_beta-measure.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2012, Chris Fournier
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
from .. import compute_pairwise_values
from .SegmentationSimilarity import similarity, DEFAULT_PERMUTED
from ..ml import fmeasure, precision, recall, vars_to_cf
from ..ml.FbMeasure import parser_beta_support, DEFAULT_BETA
from ..data import load_file
from ..data.Display import render_mean_micro_values, \
    render_permuted
    

def confusion_matrix(dataset_masses):
    '''
    Calculates a 2-class confusion matrix weighted by segmentation similarity.
    '''
    # pylint: disable=C0103
    tn = 0
    
    num_reference = 0
    num_total     = len(dataset_masses)
    
    values = compute_pairwise_values(dataset_masses, similarity,
                                     permuted=DEFAULT_PERMUTED,
                                     return_parts=False)
    
    for coder_masses in dataset_masses.values():
        if 'reference' in coder_masses.keys():
            num_reference += 1
    
    tp = sum(values.values())
    fp = num_total - len(values)
    fn = num_reference - len(values)
    
    return vars_to_cf(tp, fp, fn, tn)


def f_b_measure_s(dataset_masses, beta=DEFAULT_BETA):
    '''
    Micro F_b-measure.
    '''
    return fmeasure(confusion_matrix(dataset_masses), beta)


def precision_s(dataset_masses):
    '''
    Micro precision.
    '''
    return precision(confusion_matrix(dataset_masses))


def recall_s(dataset_masses):
    '''
    Micro recall.
    '''
    return recall(confusion_matrix(dataset_masses))


OUTPUT_NAME = render_permuted('S-based information retrieval metrics including:\
 precision, recall, and F_beta measure', 
                              DEFAULT_PERMUTED)
OUTPUT_NAME_F = render_permuted('Pairwise Mean S-based F_beta measure', 
                                DEFAULT_PERMUTED)
OUTPUT_NAME_R = render_permuted('Pairwise Mean S-based Recall value',
                                DEFAULT_PERMUTED)
OUTPUT_NAME_P = render_permuted('Pairwise Mean S-based Precision value',
                                DEFAULT_PERMUTED)
SHORT_NAME_F  = 'F_%s,s'
SHORT_NAME_P  = 'P_s'
SHORT_NAME_R  = 'R_s'
SUBSUBPARSER_NAME_F = 'f_s'
SUBSUBPARSER_NAME_P = 'p_s'
SUBSUBPARSER_NAME_R = 'r_s'


def parse(args):
    '''
    Parse this module's metric arguments and perform requested actions.
    '''
    # pylint: disable=C0103,R0914
    values = load_file(args)
    subsubparser_name = args['subsubparser_name']
    beta = 1
    if 'beta' in args and args['beta'] != 1:
        beta = args['beta']
    # Create a string to output
    if subsubparser_name == SUBSUBPARSER_NAME_F:
        mean = f_b_measure_s(values, beta)
        name = SHORT_NAME_F % str(beta)
    elif subsubparser_name == SUBSUBPARSER_NAME_P:
        mean = precision_s(values)
        name = SHORT_NAME_P
    elif subsubparser_name == SUBSUBPARSER_NAME_R:
        mean = recall_s(values)
        name = SHORT_NAME_R
    output = render_mean_micro_values(name, mean)
    # Return
    return output


def create_submetric_parser(subparsers):
    '''
    Setup a command line parser for this module's sub metrics.
    '''
    from ..data import parser_add_file_support
    from .. import parser_micro_support
    
    parser_f = subparsers.add_parser(SUBSUBPARSER_NAME_F,
                                     help='S-based F_beta Measure')
    parser_beta_support(parser_f)
    parser_add_file_support(parser_f)
    parser_micro_support(parser_f)
    parser_f.set_defaults(func=parse)
    
    parser_r = subparsers.add_parser(SUBSUBPARSER_NAME_R,
                                     help='S-based Recall')
    parser_add_file_support(parser_r)
    parser_micro_support(parser_r)
    parser_r.set_defaults(func=parse)
    
    parser_p = subparsers.add_parser(SUBSUBPARSER_NAME_P,
                                     help='S-based Precision')
    parser_add_file_support(parser_p)
    parser_micro_support(parser_p)
    parser_p.set_defaults(func=parse)


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    parser = subparsers.add_parser('s-ml',
                                   help=OUTPUT_NAME)
    
    subsubparsers = parser.add_subparsers(title='submetric', 
                                       description='Calculates a specified '+\
                                            'information retrieval (IR) '+\
                                            'metric based upon segmentation '+\
                                            'similarity (S)',
                                       help='Available IR metrics',
                                       dest='subsubparser_name')
    create_submetric_parser(subsubparsers)

