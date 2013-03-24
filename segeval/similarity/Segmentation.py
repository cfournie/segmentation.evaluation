'''
Similarity package

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from decimal import Decimal
from . import descriptive_statistics, DEFAULT_N_T, DEFAULT_BOUNDARY_TYPES, \
    DEFAULT_WEIGHT, DEFAULT_CONVERT_TO_BOUNDARY_STRINGS
from .. import compute_pairwise, compute_pairwise_values


def segmentation_similarity(segs_a, segs_b,
                            boundary_types=DEFAULT_BOUNDARY_TYPES,
                            n_t=DEFAULT_N_T, weight=DEFAULT_WEIGHT,
                            convert_to_boundary_strings=\
                            DEFAULT_CONVERT_TO_BOUNDARY_STRINGS,
                            return_parts=False):
    '''
    S
    '''
    # pylint: disable=C0103,R0913,R0914
    values = descriptive_statistics(segs_a, segs_b,
                                     boundary_types=boundary_types, n_t=n_t,
                                     weight=weight,
                                     convert_to_boundary_strings=\
                                        convert_to_boundary_strings)
    count_edits = values[0]
    pbs = values[7] * len(boundary_types)
    # Fraction
    denominator = pbs
    numerator   = pbs - count_edits
    if return_parts:
        return numerator, denominator
    else:
        return numerator / denominator if denominator > 0 else 1


def pairwise_similarity(dataset_masses, n=DEFAULT_N_T, weight=DEFAULT_WEIGHT,
            convert_to_boundary_strings=DEFAULT_CONVERT_TO_BOUNDARY_STRINGS):
    '''
    Calculate mean pairwise boundary similarity (B).
    
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
        return segmentation_similarity(segment_masses_a, segment_masses_b,
                                       dataset_masses.boundary_types, n,
                                       weight,
                                       convert_to_boundary_strings,
                                       return_parts)
    # Compute values for pairs and return mean ,etc.
    return compute_pairwise(dataset_masses, wrapper)


def pairwise_similarity_micro(dataset_masses, n=DEFAULT_N_T,
                              weight=DEFAULT_WEIGHT,
                              return_parts=False):
    '''
    Calculate mean pairwise boundary similarity (B).
    
    .. seealso:: :func:`boundary_similarity`
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
        return segmentation_similarity(segment_masses_a, segment_masses_b,
                                       dataset_masses.boundary_types, n,
                                       weight, return_parts=return_parts)
    # Compute values for pairs
    pairs = compute_pairwise_values(dataset_masses, wrapper,
                                    permuted=False,
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

