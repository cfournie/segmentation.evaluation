'''
Inter-coder agreement statistics.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import, division
from segeval.data import get_coders
from segeval.similarity import SIMILARITY_METRIC_DEFAULTS
from segeval.similarity.boundary import boundary_similarity
from segeval.similarity.distance import identify_types
from segeval.format import (BoundaryFormat, boundary_string_from_masses,
                            convert_positions_to_masses, convert_nltk_to_masses)
from segeval.util import SegmentationMetricError


AGREEMENT_METRIC_DEFAULTS = dict(SIMILARITY_METRIC_DEFAULTS)
AGREEMENT_METRIC_DEFAULTS.update({
    'fnc_compare': boundary_similarity,
    'return_parts': False
})


def __fnc_metric__(fnc_metric, dataset, **kwargs):
    metric_kwargs = dict(AGREEMENT_METRIC_DEFAULTS)
    metric_kwargs.update(kwargs)
    if hasattr(dataset, 'boundary_types'):
        metric_kwargs['boundary_types'] = dataset.boundary_types
    if hasattr(dataset, 'boundary_format'):
        metric_kwargs['boundary_format'] = dataset.boundary_format
    return fnc_metric(dataset, **metric_kwargs)


def __potential_boundaries__(segmentation_a, segmentation_b, **kwargs):
    boundary_format = kwargs['boundary_format']
    boundary_string_a = segmentation_a
    boundary_string_b = segmentation_b
    # Convert from NLTK types
    if boundary_format == BoundaryFormat.nltk:
        boundary_string_a = convert_nltk_to_masses(segmentation_a)
        boundary_string_b = convert_nltk_to_masses(segmentation_b)
        boundary_format = BoundaryFormat.mass
    # Check format
    if boundary_format == BoundaryFormat.sets:
        pass
    elif boundary_format == BoundaryFormat.mass:
        boundary_string_a = boundary_string_from_masses(boundary_string_a)
        boundary_string_b = boundary_string_from_masses(boundary_string_b)
    elif boundary_format == BoundaryFormat.position:
        boundary_string_a = convert_positions_to_masses(boundary_string_a)
        boundary_string_b = convert_positions_to_masses(boundary_string_b)
        boundary_string_a = boundary_string_from_masses(boundary_string_a)
        boundary_string_b = boundary_string_from_masses(boundary_string_b)
    else:
        raise SegmentationMetricError('Unsupported boundary format')
    # Compute boundary types if required
    boundary_types = identify_types(boundary_string_a, boundary_string_b)
    return len(boundary_string_a) * len(boundary_types)


def __boundaries__(segmentation, **kwargs):
    boundary_format = kwargs['boundary_format']
    boundary_string = segmentation
    # Convert from NLTK types
    if boundary_format == BoundaryFormat.nltk:
        boundary_string = convert_nltk_to_masses(segmentation)
        boundary_format = BoundaryFormat.mass
    # Check format
    if boundary_format == BoundaryFormat.sets:
        pass
    elif boundary_format == BoundaryFormat.mass:
        boundary_string = boundary_string_from_masses(boundary_string)
    elif boundary_format == BoundaryFormat.position:
        boundary_string = convert_positions_to_masses(boundary_string)
        boundary_string = boundary_string_from_masses(boundary_string)
    else:
        raise SegmentationMetricError('Unsupported boundary format')
    return sum([len(position) for position in boundary_string])


def __actual_agreement_linear__(dataset, **kwargs):
    '''
    Calculate actual (i.e., observed or :math:`\\text{A}_a`), segmentation
    agreement without accounting for chance, using [ArtsteinPoesio2008]_'s
    formulation as adapted in [FournierInkpen2012]_:

    .. math::
        \\text{A}_a = \\frac{
            \sum_{i \in I} \\text{mass}(i) \cdot \\text{S}(s_{i1},s_{i2})
        }{
            \sum_{i \in I} \\text{mass}(i)
        }

    Or, for more than two coders:

    .. math::
        \\text{A}_a = \\frac{1}{{\\textbf{c} \\choose 2}}
        \sum^{\\textbf{c}-1}_{m=1}
        \sum^{\\textbf{c}}_{n=m+1}
        \\frac{
            \sum_{i \in I} \\text{mass}(i) \cdot \\text{S}(s_{im},s_{in})
        }{
            \sum_{i \in I} \\big( \\text{mass}(i) - 1 \\big)
        }

    Where :math:`\\text{S}(s_{i1},s_{i2})` is defined in
    :func:`segeval.similarity.SegmentationSimilarity.similarity`.

    :param items_masses: Segmentation masses for a collection of items where \
                        each item is multiply coded (all coders code all items).
    :type items_masses: dict

    :returns: Potential boundaries unmoved, all potential boundaries, and the \
              boundaries per coder.
    :rtype: :func:`list`, :func:`list`, :func:`dict`

    An example of the dictionary structure if the ``items_masses``
    parameter is::

            items_masses = {
                'item1' : {
                    'coder1' : [5],
                    'coder2' : [2,3],
                    'coder2' : [1,1,3]
                },
                'item2' : {
                    'coder1' : [8],
                    'coder2' : [4,4],
                    'coder2' : [2,2,4]
                }
            }

    Other real and contrived examples can be found in
    :mod:`segeval.data.Samples`.

    '''
    metric_kwargs = dict(kwargs)
    del metric_kwargs['fnc_compare']
    metric_kwargs['return_parts'] = True
    # Arguments
    fnc_compare = kwargs['fnc_compare']
    return_parts = kwargs['return_parts']
    # Initialize
    all_numerators = list()
    all_denominators = list()
    all_pbs = list()
    coders_boundaries = dict()
    # Obtain the list of coders
    coders = list(get_coders(dataset))
    # For each permutation of coders
    for m in range(0, len(coders) - 1):
        for n in range(m + 1, len(coders)):
            for item in dataset.keys():
                segs_a = dataset[item][coders[m]]
                segs_b = dataset[item][coders[n]]
                # Compute similarity
                numerator, denominator = \
                    fnc_compare(segs_a, segs_b, **metric_kwargs)[0:2]
                # Obtain necessary values
                pbs = __potential_boundaries__(segs_a, segs_b, **metric_kwargs)
                # Add all pbs
                all_numerators.append(numerator)
                all_denominators.append(denominator)
                all_pbs.append(pbs)
                # Create in dicts if not present
                if coders[m] not in coders_boundaries:
                    coders_boundaries[coders[m]] = list()
                if coders[n] not in coders_boundaries:
                    coders_boundaries[coders[n]] = list()
                # Add per-coder values to dicts
                coders_boundaries[coders[m]].append([__boundaries__(segs_a, **metric_kwargs), pbs])
                coders_boundaries[coders[n]].append([__boundaries__(segs_b, **metric_kwargs), pbs])
    if return_parts:
        return all_numerators, all_denominators, all_pbs, coders_boundaries
    else:
        return sum(all_numerators) / sum(all_denominators)


def actual_agreement_linear(dataset, **kwargs):

    return __fnc_metric__(__actual_agreement_linear__, dataset, **kwargs)
