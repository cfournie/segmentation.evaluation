'''
Abstract computation utilities.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
from segeval.util.math import mean, std, var, stderr
from itertools import combinations


def compute_pairwise_values(fnc_metric, dataset_a, dataset_b=None, **kwargs):
    '''
    Calculate mean pairwise segmentation metric pairs for functions that take
    pairs of segmentations.

    :param dataset: Segmentation mass dataset (including multiple \
                           codings).
    :param fnc_metric:     Metric function to call on segmentation mass pairs.
    :param permuted:       Permute coder combinations if true.
    :type dataset: dict
    :type fnc_metric:     func
    :type permuted:       bool
    '''

    pairs = dict()
    fnc_kwargs = dict(kwargs)
    # Obtain parameters
    permuted = fnc_kwargs['permuted']
    return_parts = fnc_kwargs['return_parts'] \
        if 'return_parts' in fnc_kwargs else False
    del fnc_kwargs['permuted']

    # Define fnc per group
    def __per_group__(prefix, inner_dataset_m, inner_dataset_n, has_two_datasets):
        '''
        Recurse through a dict to find levels where a metric can be calculated.

        :param inner_dataset: Segmentation mass dataset (including \
                                     multiple codings).
        :type inner_dataset: dict
        '''

        labels = set(inner_dataset_m.keys())
        if inner_dataset_n is not None:
            labels.update(inner_dataset_n.keys())
        for label in labels:
            # Get coders from both datasets
            coder_masses_m = inner_dataset_m[
                label] if label in inner_dataset_m else None
            coder_masses_n = inner_dataset_n[
                label] if inner_dataset_n is not None and label in inner_dataset_n else None
            # Skip this label if it is not contained within both datasets
            if has_two_datasets and (coder_masses_m is None or coder_masses_n is None):
                continue
            # Check to see if there is further nesting
            label_pairs = dict()
            # If is a group
            coder_pairs = None
            if has_two_datasets:
                coders_m = coder_masses_m.keys()
                coders_n = coder_masses_n.keys()
                coder_pairs = [(m, n) for m in coders_m for n in coders_n]
            else:
                coders = coder_masses_m.keys()
                coder_pairs = combinations(coders, 2)
                # We use the same data for both coders
                coder_masses_n = coder_masses_m
            for m, n in coder_pairs:
                segs_m = coder_masses_m[m]
                segs_n = coder_masses_n[n]
                entry_parts = list(prefix)
                entry_parts.extend([label, str(m), str(n)])
                entry = ','.join(entry_parts)
                if return_parts:
                    label_pairs[entry] = fnc_metric(segs_m, segs_n,
                                                    **fnc_kwargs)
                else:
                    label_pairs[entry] = fnc_metric(segs_m, segs_n,
                                                    **fnc_kwargs)
                # Handle permutation
                if permuted and not has_two_datasets:
                    entry_parts = list(prefix)
                    entry_parts.extend([label, str(n), str(m)])
                    entry = ','.join(entry_parts)
                    if return_parts:
                        label_pairs[entry] = \
                            fnc_metric(segs_n, segs_m, **fnc_kwargs)
                    else:
                        label_pairs[entry] = fnc_metric(segs_n, segs_m,
                                                        **fnc_kwargs)
            # Add all
            for entry, pair in label_pairs.items():
                pairs[entry] = pair
            # Erase
            label_pairs = dict()
    # Parse
    has_two_datasets = dataset_b is not None
    __per_group__(tuple(), dataset_a, dataset_b, has_two_datasets)
    # Return mean, std dev, and variance
    return pairs


def summarize(pairs):
    '''
    Takes a list of values and returns the mean, standard deviation, variance, standard error, and number of values.

    :param pairs: List of numerical values
    :type pairs: list
    '''
    return mean(pairs.values()), std(pairs.values()), var(pairs.values()), \
        stderr(pairs.values()), len(pairs)
