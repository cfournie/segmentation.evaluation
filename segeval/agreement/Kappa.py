'''
Inter-coder agreement statistic Fleiss' Kappa.

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
from . import actual_agreement
from .. import compute_multiple_values, create_tsv_rows
from ..data import load_file
from ..data.TSV import write_tsv
from ..data.Display import render_agreement_coefficients
from . import actual_agreement_linear, DEFAULT_T_N
from ..similarity.Linear import boundary_similarity


def fleiss_kappa_linear(dataset, fnc_compare=boundary_similarity,
                        return_parts=False, t_n=DEFAULT_T_N):
    '''
    Calculates Fleiss' Kappa (or multi-Kappa), originally proposed in
    [DaviesFleiss1982]_, for segmentations.  Adapted in [FournierInkpen2012]_ 
    from the formulations provided in [Hearst1997]_ (p. 53) and using
    [ArtsteinPoesio2008]_'s formulation for expected agreement:
    
    .. math::
        \\text{A}^{\kappa^*}_e = \sum_{k \in K} \\bigg(
        \\frac{1}{{\\textbf{c} \\choose 2}}
        \sum^{\\textbf{c}-1}_{m=1}
        \sum^{\\textbf{c}}_{n=m+1} \\text{P}^\kappa_e(k|c_m) \cdot
            \\text{P}^\kappa_e(k|c_n) \\bigg)
    
    :param items_masses: Segmentation masses for a collection of items where \
                        each item is multiply coded (all coders code all items).
    :param return_parts: If true, return the numerator and denominator.
    :type item_masses:  dict
    :type return_parts: bool
    
    :returns: Fleiss's Kappa
    :rtype: :class:`decimal.Decimal`
    
    .. seealso:: :func:`segeval.agreement.actual_agreement` for an example of\
     ``items_masses``.
    
    .. note:: Applicable for more than 2 coders.
    '''
    # pylint: disable=C0103,R0914
    # Check that there are more than 2 coders
    if len([True for coder_segs in dataset.values() \
            if len(coder_segs.keys()) < 2]) > 0:
        raise Exception('Less than 2 coders specified.')
    # Check that there are an identical number of items
    num_items = len(dataset.values()[0].keys())
    if len([True for coder_segs in dataset.values() \
            if len(coder_segs.values()) != num_items]) > 0:
        raise Exception('Unequal number of items contained.')
    # Initialize totals
    all_numerators, all_denominators, _, coders_boundaries = \
            actual_agreement_linear(dataset, fnc_compare=fnc_compare, t_n=t_n)
    # Calculate Aa
    A_a = Decimal(sum(all_numerators)) / sum(all_denominators)
    # Calculate Ae
    coders = coders_boundaries.keys()
    P_segs = list()
    for m in range(0, len(coders) - 1):
        for n in range(m+1, len(coders)):
            boundaries_m       = sum(info [0] for info in \
                                 coders_boundaries[coders[m]])
            total_boundaries_m = sum(info [1] for info in \
                                 coders_boundaries[coders[m]])
            boundaries_n       = sum(info [0] for info in \
                                 coders_boundaries[coders[n]])
            total_boundaries_n = sum(info [1] for info in \
                                 coders_boundaries[coders[n]])
            P_segs.append((Decimal(boundaries_m) / total_boundaries_m) * \
                          (Decimal(boundaries_n) / total_boundaries_n))
    P_seg = Decimal(sum(P_segs)) / len(P_segs)
    A_e = P_seg
    # Calculate pi
    kappa = (A_a - A_e) / (Decimal('1') - A_e)
    # Return
    if return_parts:
        return A_a, A_e
    else:
        return kappa

OUTPUT_NAME = 'B-based Fleiss\' Multi Kappa coefficient'
SHORT_NAME  = 'K*_B'


def values_kappa(dataset_masses):
    '''
    Produces a TSV for this metric
    '''
    header = list([SHORT_NAME])
    values = compute_multiple_values(dataset_masses, fleiss_kappa)
    return create_tsv_rows(header, values)


def parse(args):
    '''
    Parse this module's metric arguments and perform requested actions.
    '''
    output = None
    values = load_file(args)
    # Is a TSV requested?
    if args['output'] != None:
        # Create a TSV
        output_file = args['output'][0]
        header, rows = values_kappa(values)
        write_tsv(output_file, header, rows)
    else:
        # Create a string to output and render for one or more items
        kappas = compute_multiple_values(values, fleiss_kappa)
        output = render_agreement_coefficients(SHORT_NAME, kappas)
    # Return
    return output


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    from ..data import parser_add_file_support
    parser = subparsers.add_parser('k',
                                   help=OUTPUT_NAME)
    parser_add_file_support(parser)
    parser.set_defaults(func=parse)