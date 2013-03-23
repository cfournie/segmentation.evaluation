'''
Arstein Poesio's annotator bias.

References:
    
    Ron Artstein and Massimo Poesio. 2008. Inter-coder agreement for
    computational linguistics. Computational Linguistics, 34(4):555-596. MIT
    Press.

.. codeauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from .Kappa import fleiss_kappa_linear
from .Pi import fleiss_pi_linear
from . import DEFAULT_N_T
from ..similarity.Boundary import boundary_similarity
from .. import compute_multiple_values, create_tsv_rows
from ..data import load_file
from ..data.TSV import write_tsv
from ..data.Display import render_agreement_coefficients


def artstein_poesio_bias_linear(dataset, fnc_compare=boundary_similarity,
                                n_t=DEFAULT_N_T):
    '''
    Artstein and Poesio's annotator bias, or B (Artstein and Poesio, 2008,
    pp. 572).
    
    Arguments:
    segs_set_all -- A list of document segments for each coder (each in the
                    same item order), e.g.: [an1, an2, an3], where an1 = 
                    [d1, d2, d3], where d1 = segmass_d1.
    
    Returns:
    B as a Decimal object.
    '''
    # pylint: disable=C0103
    A_pi_e     =    fleiss_pi_linear(dataset, fnc_compare=fnc_compare,
                                     return_parts=True, n_t=n_t)[1]
    A_fleiss_e = fleiss_kappa_linear(dataset, fnc_compare=fnc_compare,
                                     return_parts=True, n_t=n_t)[1]
    return A_pi_e - A_fleiss_e


OUTPUT_NAME     = 'B-based Artstein and Poesio\'s (2008) Bias value'
SHORT_NAME      = 'Bias_B'
SHORT_NAME_MEAN = 'Mean %s' % SHORT_NAME


def values_artstein_poesio_bias(dataset_masses):
    '''
    Produces a TSV for this metric
    '''
    header = list([SHORT_NAME])
    values = compute_multiple_values(dataset_masses,
                                     artstein_poesio_bias_linear)
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
        header, rows = values_artstein_poesio_bias(values)
        write_tsv(output_file, header, rows)
    else:
        # Create a string to output and render for one or more items
        biases = compute_multiple_values(values,
                                         artstein_poesio_bias_linear)
        output = render_agreement_coefficients(SHORT_NAME, biases)
    # Return
    return output


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    from ..data import parser_add_file_support
    parser = subparsers.add_parser('b',
                                   help=OUTPUT_NAME)
    parser_add_file_support(parser)
    parser.set_defaults(func=parse)