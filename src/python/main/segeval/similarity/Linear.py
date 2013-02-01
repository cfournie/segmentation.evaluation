'''
Created on Sep 4, 2012

@author: cfournie
'''
from decimal import Decimal
from .distance.MultipleBoundary import boundary_edit_distance
from segeval import compute_pairwise, compute_pairwise_values
from .. import SegmentationMetricError, compute_pairwise, \
    compute_pairwise_values, create_tsv_rows
from ..data import load_file
from ..data.TSV import write_tsv
from ..data.Display import render_mean_values, render_mean_micro_values


def boundary_string_from_masses(segment_masses):
    '''
    Creates a "boundary string", or sequence of boundary type sets.
    
    :param segment_masses: Segmentation masses.
    :type segment_masses:  list
    :returns: A sequence of boundary type sets
    :rtype: :func:`list` of :func:`set` objects containing :func:`int` values.
    '''
    string = [set() for _ in xrange(0, sum(segment_masses) - 1)]
    # Iterate over each position
    pos = 0
    for mass in segment_masses:
        cur_pos = pos + mass - 1
        if cur_pos < len(string):
            string[cur_pos].add(1)
        pos += mass
    # Return
    return [set(pb) for pb in string]


def boundaries(segment_masses):
    '''
    Counts the number of boundaries in a set of boundary masses.
    '''
    return len(segment_masses) - 1


def weight_a(additions):
    '''
    Default weighting function for addition edit operations.
    '''
    return len(additions)


def weight_s(substitutions, max_s, min_s=1):
    '''
    Default weighting function for substitution edit operations.
    '''
    # pylint: disable=W0613,C0103
    return len(substitutions)


def weight_s_scale(substitutions, max_s, min_s=1):
    '''
    Default weighting function for substitution edit operations.
    '''
    # pylint: disable=W0613,C0103
    return weight_t_scale(substitutions, max_s - min_s + 1)


def weight_t(transpositions, max_n):
    '''
    Default weighting function for transposition edit operations.
    '''
    # pylint: disable=W0613,C0103
    return len(transpositions)


def weight_t_scale(transpositions, max_n):
    '''
    Default weighting function for transposition edit operations.
    '''
    numerator   = 0
    if isinstance(transpositions, list):
        for transposition in transpositions:
            numerator += abs(transposition[0] - transposition[1])
        return Decimal(numerator) / max_n
    else:
        return Decimal(abs(transpositions[0] - transpositions[1])) / max_n


DEFAULT_PERMUTED = False
DEFAULT_N = 2
DEFAULT_BOUNDARY_TYPES = set([1])
DEFAULT_WEIGHT = (weight_a, weight_s, weight_t)
DEFAULT_CONVERT_TO_BOUNDARY_STRINGS = True

DEFAULT_BS_N = 5
DEFAULT_BS_WEIGHT = (weight_a, weight_s_scale, weight_t_scale)


def __boundary_similarity__(segs_a, segs_b,
                            boundary_types=DEFAULT_BOUNDARY_TYPES,
                            n=DEFAULT_BS_N, weight=DEFAULT_BS_WEIGHT,
                            convert_to_boundary_strings=\
                                DEFAULT_CONVERT_TO_BOUNDARY_STRINGS):
    '''
    Compute boundary similarity applying the weighting functions specified.
    '''
    # pylint: disable=C0103,R0913,R0914
    # Compute similarity
    pbs, count_edits, additions, substitutions, transpositions = \
        similarity(segs_a, segs_b, boundary_types=boundary_types, n=n,
                   weight=weight,
                   convert_to_boundary_strings=convert_to_boundary_strings,
                   return_values=True)
    # Count boundaries
    bs_a = segs_a
    bs_b = segs_b
    if convert_to_boundary_strings:
        bs_a = boundary_string_from_masses(segs_a)
        bs_b = boundary_string_from_masses(segs_b)
    # Compute
    full_misses = 0
    boundaries_all = 0
    matches = 0
    for set_a, set_b in zip(bs_a, bs_b):
        matches += len(set_a.intersection(set_b))
        full_misses += len(set_a.symmetric_difference(set_b))
        boundaries_all += len(set_a) + len(set_b)
    return pbs, count_edits, additions, substitutions, transpositions, \
            full_misses, boundaries_all, matches


def boundary_similarity(segs_a, segs_b,
                        boundary_types=DEFAULT_BOUNDARY_TYPES,
                        n=DEFAULT_BS_N, weight=DEFAULT_BS_WEIGHT,
                        convert_to_boundary_strings=\
                        DEFAULT_CONVERT_TO_BOUNDARY_STRINGS,
                        return_parts=False):
    '''
    BS type b.
    '''
    # pylint: disable=C0103,R0913,R0914
    values = __boundary_similarity__(segs_a, segs_b, boundary_types, n, weight,
                                     convert_to_boundary_strings)
    matches        = values[7]
    count_edits    = values[1] # Weighted
    additions      = values[2]
    substitutions  = values[3]
    transpositions = values[4]
    count_unweighted = len(additions) + len(substitutions) + len(transpositions)
    # Fraction
    denominator = count_unweighted + matches
    numerator   = denominator - count_edits
    if return_parts:
        return numerator, denominator
    else:
        return numerator / denominator if denominator > 0 else 1
    
    
def pairwise_similarity(dataset_masses, n=DEFAULT_N, weight=DEFAULT_WEIGHT,
            convert_to_boundary_strings=DEFAULT_CONVERT_TO_BOUNDARY_STRINGS):
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
    def wrapper(segment_masses_a, segment_masses_b, return_parts=False):
        '''
        Wrapper to provide parameters.
        '''
        return similarity(segment_masses_a, segment_masses_b,
                          dataset_masses.boundary_types, n,
                          weight,
                          convert_to_boundary_strings,
                          return_parts)
    # Compute values for pairs and return mean ,etc.
    return compute_pairwise(dataset_masses, wrapper, permuted=DEFAULT_PERMUTED)


def pairwise_similarity_micro(dataset_masses, n=DEFAULT_N,
                              weight=DEFAULT_WEIGHT,
                              return_parts=False,
                              fnc_similarity=similarity):
    '''
    Calculate mean pairwise S.
    
    .. seealso:: :func:`similarity`
    .. seealso:: :func:`segeval.compute_pairwise`
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :param return_parts:   If false, returns a :class:`decimal.Decimal`, \
                                else, return the statistics used to create \
                                the decimal
    :type dataset_masses: dict
    
    :returns: Mean (micro)
    :rtype: :class:`decimal.Decimal`, or :func:`int`, :func:`int`
    '''
    # pylint: disable=C0103,R0913,R0914
    def wrapper(segment_masses_a, segment_masses_b, return_parts=True):
        '''
        Wrapper to provide parameters.
        '''
        return fnc_similarity(segment_masses_a, segment_masses_b,
                              dataset_masses.boundary_types, n,
                              weight, return_parts=return_parts)
    # Compute values for pairs
    pairs = compute_pairwise_values(dataset_masses, wrapper,
                                    permuted=DEFAULT_PERMUTED,
                                    return_parts=True)
    # Sum and extend for each pair
    pbs, count_edits = 0, 0
    additions, substitutions, transpositions = list(), list(), list()
    for values in pairs.values():
        # Get
        current_pbs, current_count_edits, current_additions, \
            current_substitutions, current_transpositions = values
        # Sum
        pbs         += current_pbs
        count_edits += current_count_edits
        # Construct overall edit sets
        additions.extend(current_additions)
        substitutions.extend(current_substitutions)
        transpositions.extend(current_transpositions)
    # Return
    if return_parts:
        return pbs, count_edits, additions, substitutions, transpositions
    else:
        return (Decimal(count_edits) / Decimal(pbs))




def pairwise_b(dataset_masses, n=DEFAULT_N, weight=DEFAULT_WEIGHT,
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


def pairwise_b_micro(dataset_masses, n=DEFAULT_N,
                              weight=DEFAULT_WEIGHT,
                              scale_transp=DEFAULT_SCALE,
                              return_parts=False):
    '''
    Calculate mean pairwise B.
    
    .. seealso:: :func:`similarity`
    .. seealso:: :func:`segeval.compute_pairwise`
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :param return_parts:   If false, returns a :class:`decimal.Decimal`, \
                                else, return the statistics used to create \
                                the decimal
    :type dataset_masses: dict
    
    :returns: Mean (micro)
    :rtype: :class:`decimal.Decimal`, or :func:`int`, :func:`int`
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
    
    pbs_unedited, pbs_total, set_errors_total, set_transpositions_total = \
        0, 0, 0, 0
    set_errors = list()
    transpostions = list()
    for values in pairs.values():
        # get
        pair_pbs_unedited, pair_pbs_total, pair_set_errors_total, \
            pair_set_transpositions_total, pair_set_errors, \
            pair_set_transpositions = values
        # sum
        pbs_unedited             += pair_pbs_unedited
        pbs_total                += pair_pbs_total
        set_errors_total         += pair_set_errors_total
        set_transpositions_total += pair_set_transpositions_total
        # extend
        set_errors.extend(pair_set_errors)
        transpostions.extend(pair_set_transpositions)
    
    if return_parts:
        return pbs_unedited, pbs_total, set_errors_total, \
            set_transpositions_total, set_errors, transpostions
    else:
        return Decimal(pbs_unedited) / Decimal(pbs_total)


OUTPUT_NAME = 'Mean B metric'
SHORT_NAME  = 'B'


def values_b_detailed(dataset_masses, n=DEFAULT_N, weight=DEFAULT_WEIGHT,
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


def values_b(dataset_masses, n=DEFAULT_N, weight=DEFAULT_WEIGHT,
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
            header, rows = values_b_detailed(values, n, weight, te)
        else:
            header, rows = values_b(values, n, weight, te)
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


def parser_b_support(parser):
    '''
    Add support for B parameters
    
    :param parser: Argument parser
    :type parser: argparse.ArgumentParser
    '''
    parser.add_argument('-nt',
                        type=int,
                        default=DEFAULT_N,
                        help='The maximum number of PBs that boundaries can '+\
                              'span to be considered transpositions (nt<2 '+\
                              ('means no transpositions); default is %i.' \
                                    % DEFAULT_N))


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    from ..data import parser_add_file_support
    from .. import parser_micro_support
    parser = subparsers.add_parser('b',
                                   help=OUTPUT_NAME)
    parser_add_file_support(parser)
    parser_b_support(parser)
    parser_micro_support(parser)
    parser.add_argument('-de', '--detailed',
                        action='store_true',
                        default=False,
                        help='When specifying an output TSV file, specify '+\
                            'this to obtain a detailed error breakdown per '+\
                            'edit')
    parser.set_defaults(func=parse)
