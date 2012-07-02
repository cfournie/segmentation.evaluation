'''
This module contains implementations of Scott's and Fleiss' Pi, adapted in
[FournierInkpen2012]_ for segmentation (in as similar a manner as [Hearst1997]_)
using the formulation of Kappa provided in [ArtsteinPoesio2008]_.

Pi's general form could be described, as it is in [ArtsteinPoesio2008]_, in 
terms of actual agreement (:math:`\\text{A}_a`) and expected agreement 
(:math:`\\text{A}_e`) as:

.. math::
    \pi,\pi^* = \\frac{\\text{A}_a-\\text{A}_e}{1 \
    - \\text{A}_e}

:math:`\pi` represents Scott's Pi (for 2 coders), whereas :math:`\pi^*`
represents its generalization to more than 2 coders.  Each metric calculates
:math:`\\text{A}_a` using :func:`segeval.agreement.actual_agreement` and
only varies the calculation of :math:`\\text{A}_e`.


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
from . import actual_agreement
from .. import compute_multiple_values, create_tsv_rows
from ..data import load_file
from ..data.TSV import write_tsv
from ..data.Display import render_agreement_coefficients


def scotts_pi(items_masses, return_parts=False):
    '''
    Calculates Scott's Pi, originally proposed in [Scott1955]_, for
    segmentations.  Adapted in [FournierInkpen2012]_ from the formulations
    provided in [Hearst1997]_ and [ArtsteinPoesio2008]_'s formulation for
    expected agreement:
    
    .. math::
        \\text{A}^\pi_e = \sum_{k \in K} \\big(\\text{P}^\pi_e(k)\\big)^2
    
    .. math::
        \\text{P}^\pi_e(\\text{seg}_t) = 
        \\frac{
            \sum_{c \in C}\sum_{i \in I}|\\text{boundaries}(t, s_{ic})|
        }{
            \\textbf{c} \cdot \sum_{i \in I} \\big( \\text{mass}(i) - 1 \\big)
        }
    
    :param items_masses: Segmentation masses for a collection of items where \
                        each item is multiply coded (all coders code all items).
    :param return_parts: If true, return the numerator and denominator
    :type item_masses:  dict
    :type return_parts: bool
    
    :returns: Scott's Pi
    :rtype: :class:`decimal.Decimal`
    
    .. seealso:: :func:`segeval.agreement.actual_agreement` for an example of\
     ``items_masses``.
    
    .. note:: Applicable for only 2 coders.
    '''
    # Check that there are no more than 2 coders
    if len([True for coder_segs in items_masses.values() \
            if len(coder_segs.keys()) > 2]) > 0:
        raise Exception('Unequal number of items specified.')
    # Check that there are an identical number of items
    num_items = len(items_masses.values()[0].keys())
    if len([True for coder_segs in items_masses.values() \
            if len(coder_segs.values()) != num_items]) > 0:
        raise Exception('Unequal number of items contained.')
    # Return
    return fleiss_pi(items_masses, return_parts)


def fleiss_pi(items_masses, return_parts=False):
    '''
    Calculates Fleiss' Pi (or multi-Pi), originally proposed in [Fleiss1971]_,
    for segmentations (and described in [SiegelCastellan1988]_ as K).
    Adapted from the formulations
    provided in [Hearst1997]_ (p. 53) and [ArtsteinPoesio2008]_'s formulation
    for expected agreement:
    
    .. math::
        \\text{A}^{\pi^*}_e = \sum_{k \in K} \\big(\\text{P}^\pi_e(k)\\big)^2
    
    :param items_masses: Segmentation masses for a collection of items where \
                        each item is multiply coded (all coders code all items).
    :param return_parts: If true, return the numerator and denominator.
    :type items_masses:  dict
    :type return_parts: bool
    
    :returns: Fleiss's Pi
    :rtype: :class:`decimal.Decimal`
    
    .. seealso:: :func:`segeval.agreement.actual_agreement` for an example of\
     ``items_masses``.
    
    .. note:: Applicable for more than 2 coders.
    '''
    # pylint: disable=C0103,R0914
    # Check that there are an equal number of items for each coder
    num_items = len(items_masses.values()[0].keys())
    if len([True for coder_segs in items_masses.values() \
            if len(coder_segs.values()) != num_items]) > 0:
        raise Exception('Unequal number of items contained.')
    # Initialize totals
    unmoved_masses, total_masses, coders_boundaries_totalboundaries = \
        actual_agreement(items_masses)
    # Calculate Aa
    A_a = Decimal(sum(unmoved_masses)) / sum(total_masses)
    # Calculate Ae
    p_e_segs = list()
    for boundaries_info in coders_boundaries_totalboundaries.values():
        for item in boundaries_info:
            boundaries, total_boundaries = item
            p_e_seg = boundaries / total_boundaries
            p_e_segs.append(p_e_seg)
    # Calculate P_e_seg
    P_e_seg = Decimal(sum(p_e_segs)) / len(p_e_segs)
    A_e = (P_e_seg ** 2)
    # Calculate pi
    pi = (A_a - A_e) / (Decimal('1.0') - A_e)
    # Return
    if return_parts:
        return A_a, A_e
    else:
        return pi


OUTPUT_NAME     = 'S-based Fleiss\' Multi Pi coefficient'
SHORT_NAME      = 'Pi*_s'


def values_pi(dataset_masses):
    '''
    Produces a TSV for this metric
    '''
    header = list([SHORT_NAME])
    values = compute_multiple_values(dataset_masses, fleiss_pi)
    return create_tsv_rows(header, values)


def parse(args):
    '''
    Parse this module's metric arguments and perform requested actions.
    '''
    # pylint: disable=C0103
    output = None
    values = load_file(args)
    # Is a TSV requested?
    if args['output'] != None:
        # Create a TSV
        output_file = args['output'][0]
        header, rows = values_pi(values)
        write_tsv(output_file, header, rows)
    else:
        # Create a string to output and render for one or more items
        pis = compute_multiple_values(values, fleiss_pi)
        output = render_agreement_coefficients(SHORT_NAME, pis)
    # Return
    return output


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    from ..data import parser_add_file_support
    parser = subparsers.add_parser('pi',
                                   help=OUTPUT_NAME)
    parser_add_file_support(parser)
    parser.set_defaults(func=parse)

