'''
Inter-coder agreement statistics.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division
from ..similarity import SIMILARITY_METRIC_DEFAULTS
from ..similarity.boundary import boundary_similarity


AGREEMENT_METRIC_DEFAULTS = dict(SIMILARITY_METRIC_DEFAULTS)
AGREEMENT_METRIC_DEFAULTS.update({
    'fnc_compare' : boundary_similarity,
    'return_parts' : False
})


def __fnc_metric__(fnc_metric, dataset, **kwargs):
    # pylint: disable=W0142
    metric_kwargs = dict(AGREEMENT_METRIC_DEFAULTS)
    metric_kwargs.update(kwargs)
    return fnc_metric(dataset, **metric_kwargs)


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
    # pylint: disable=C0103,R0914,W0142
    metric_kwargs = dict(kwargs)
    del metric_kwargs['fnc_compare']
    metric_kwargs['return_parts'] = True
    # Arguments
    fnc_compare = kwargs['fnc_compare']
    return_parts = kwargs['return_parts']
    # Initialize
    all_numerators    = list()
    all_denominators  = list()
    all_pbs           = list()
    coders_boundaries = dict()
    coders = dataset.values()[0].keys()
    # FOr each permutation of coders
    for m in range(0, len(coders) - 1):
        for n in range(m+1, len(coders)):
            for item in dataset.keys():
                segs_a = dataset[item][coders[m]]
                segs_b = dataset[item][coders[n]]
                # Compute similarity
                numerator, denominator = \
                    fnc_compare(segs_a, segs_b, **metric_kwargs)[0:2]
                # Obtain necessary values
                pbs = sum(segs_a) - 1
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
                coders_boundaries[coders[m]].append([len(segs_a), pbs])
                coders_boundaries[coders[n]].append([len(segs_b), pbs])
    if return_parts:
        return all_numerators, all_denominators, all_pbs, coders_boundaries
    else:
        return sum(all_numerators) / sum(all_denominators)


def actual_agreement_linear(dataset, **kwargs):
    # pylint: disable=W0142
    return __fnc_metric__(__actual_agreement_linear__, dataset, **kwargs)

