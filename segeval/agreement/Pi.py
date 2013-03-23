'''
Inter-coder agreement statistic Fleiss' Pi.

.. codeauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from decimal import Decimal
from .. import compute_multiple_values, create_tsv_rows
from ..data import load_file
from ..data.TSV import write_tsv
from ..data.Display import render_agreement_coefficients
from . import actual_agreement_linear, DEFAULT_N_T
from ..similarity.Linear import boundary_similarity


def scotts_pi_linear(items_masses, return_parts=False, n_t=DEFAULT_N_T):
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
    return fleiss_pi_linear(items_masses, return_parts, n_t)


def fleiss_pi_linear(items_masses, fnc_compare=boundary_similarity,
                     return_parts=False, n_t=DEFAULT_N_T):
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
    all_numerators, all_denominators, _, coders_boundaries = \
        actual_agreement_linear(items_masses, fnc_compare=fnc_compare, n_t=n_t)
    # Calculate Aa
    A_a = Decimal(sum(all_numerators)) / sum(all_denominators)
    # Calculate Ae
    p_e_segs = list()
    for boundaries_info in coders_boundaries.values():
        for item in boundaries_info:
            boundaries, total_boundaries = item
            p_e_seg = Decimal(boundaries) / total_boundaries
            p_e_segs.append(p_e_seg)
    # Calculate P_e_seg
    P_e_seg = Decimal(sum(p_e_segs)) / len(p_e_segs)
    A_e = (P_e_seg ** 2)
    # Calculate pi
    pi = (A_a - A_e) / (Decimal('1') - A_e)
    # Return
    if return_parts:
        return A_a, A_e
    else:
        return pi



OUTPUT_NAME     = 'B-based Fleiss\' Multi Pi coefficient'
SHORT_NAME      = 'Pi*_B'


def values_pi(dataset_masses):
    '''
    Produces a TSV for this metric
    '''
    header = list([SHORT_NAME])
    values = compute_multiple_values(dataset_masses, fleiss_pi_linear)
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
        pis = compute_multiple_values(values, fleiss_pi_linear)
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
