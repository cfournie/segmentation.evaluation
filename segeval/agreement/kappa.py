'''
Inter-coder agreement statistic Fleiss' Kappa.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import, division
from decimal import Decimal
from segeval.agreement import __fnc_metric__, __actual_agreement_linear__


def __fleiss_kappa_linear__(dataset, **kwargs):
    '''
    Calculates Fleiss' :math:`\kappa` (or multi-:math:`\kappa`), originally proposed in
    [DaviesFleiss1982]_.  For 2 coders, this is equivalent to Cohen's :math:`\kappa`
    [Cohen1960]_.
    '''
    metric_kwargs = dict(kwargs)
    metric_kwargs['return_parts'] = True
    # Arguments
    return_parts = kwargs['return_parts']
    # Check that there are more than 2 coders
    if len([True for coder_segs in dataset.values()
            if len(coder_segs.keys()) < 2]) > 0:
        raise Exception('Less than 2 coders specified.')
    # Check that there are an identical number of items
    if len(set([len(coder_segs.values()) for coder_segs in dataset.values()])) != 1:
        raise Exception('Unequal number of items contained.')
    # Initialize totals
    all_numerators, all_denominators, _, coders_boundaries = \
        __actual_agreement_linear__(dataset, **metric_kwargs)
    # Calculate Aa
    A_a = Decimal(sum(all_numerators)) / sum(all_denominators)
    # Calculate Ae
    coders = list(coders_boundaries.keys())
    P_segs = list()
    for m in range(0, len(coders) - 1):
        for n in range(m + 1, len(coders)):
            boundaries_m = sum(info[0] for info in
                               coders_boundaries[coders[m]])
            total_boundaries_m = sum(info[1] for info in
                                     coders_boundaries[coders[m]])
            boundaries_n = sum(info[0] for info in
                               coders_boundaries[coders[n]])
            total_boundaries_n = sum(info[1] for info in
                                     coders_boundaries[coders[n]])
            P_segs.append((Decimal(boundaries_m) / total_boundaries_m) *
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


def fleiss_kappa_linear(dataset, **kwargs):
    '''
    Calculates Fleiss' :math:`\kappa` (or multi-:math:`\kappa`), originally proposed in
    [DaviesFleiss1982]_.  For 2 coders, this is equivalent to Cohen's :math:`\kappa`
    [Cohen1960]_.
    '''
    return __fnc_metric__(__fleiss_kappa_linear__, dataset, **kwargs)
