'''
Created on Apr 13, 2013

@author: cfournie
'''
from .util.math import mean, std, var, stderr


def compute_pairwise_values(dataset_masses, fnc_metric, **kwargs):
    '''
    Calculate mean pairwise segmentation metric pairs for functions that take
    pairs of segmentations.
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :param fnc_metric:     Metric function to call on segmentation mass pairs.
    :param permuted:       Permute coder combinations if true.
    :type dataset_masses: dict
    :type fnc_metric:     func
    :type permuted:       bool
    
    :returns: List of values
    :rtype: :func:`list`
    '''
    # pylint: disable=C0103,R0912,W0142
    from .data.jsonutils import Field
    pairs = dict()
    fnc_kwargs = dict(kwargs)
    permuted = fnc_kwargs['permuted']
    return_parts = fnc_kwargs['return_parts'] \
        if 'return_parts' in fnc_kwargs else False
    del fnc_kwargs['permuted']
    reference_coder_exists = False
    # Determine whether a reference coder is designated
    if Field.has_reference_coder in dataset_masses.properties:
        reference_coder_exists = \
            dataset_masses.properties[Field.has_reference_coder]
    if reference_coder_exists:
        permuted = False
    # Define fnc per group
    def __per_group__(prefix, inner_dataset_masses):
        '''
        Recurse through a dict to find levels where a metric can be calculated.
        
        
        :param inner_dataset_masses: Segmentation mass dataset (including \
                                     multiple codings).
        :type inner_dataset_masses: dict
        '''
        # pylint: disable=R0912,R0914
        for label, coder_masses in inner_dataset_masses.items():
            label_pairs = dict()
            
            if len(coder_masses.values()) > 0 and \
                isinstance(coder_masses.values()[0], tuple):
                # If is a group
                coders = coder_masses.keys()
                for m in range(0, len(coders)):
                    for n in range(m+1, len(coders)):
                        if reference_coder_exists and \
                            'reference' in coders[m] and \
                            'reference' in coders[n]:
                            continue
                        
                        segs_m = coder_masses[coders[m]]
                        segs_n = coder_masses[coders[n]]
                        entry_parts = list(prefix)
                        entry_parts.extend([label,
                                            str(coders[m]),
                                            str(coders[n])])
                        entry = ','.join(entry_parts)
                        if return_parts:
                            label_pairs[entry] = \
                                fnc_metric(segs_m, segs_n, **fnc_kwargs)
                        else:
                            label_pairs[entry] = fnc_metric(segs_m, segs_n,
                                                            **fnc_kwargs)
                        # Handle permutation
                        if permuted:
                            entry_parts = list(prefix)
                            entry_parts.extend([label, str(n), str(m)])
                            entry = ','.join(entry_parts)
                            if return_parts:
                                label_pairs[entry] = \
                                    fnc_metric(segs_n, segs_m, **fnc_kwargs)
                            else:
                                label_pairs[entry] = fnc_metric(segs_n, segs_m,
                                                                **fnc_kwargs)
                # Add to main set
                if reference_coder_exists:
                    max_reference_entry = None
                    max_reference_pair  = 0
                    # Perform reference exclusion
                    for entry, pair in label_pairs.items():
                        coder_parts = entry.split(',')
                        coders_string = coder_parts.pop()
                        coders_string += coder_parts.pop()
                        if 'reference' in coders_string:
                            if pair > max_reference_pair:
                                max_reference_entry = entry
                                max_reference_pair  = pair 
                        else:
                            pairs[entry] = pair
                    # Add only if there is a max
                    if max_reference_entry is not None:
                        pairs[max_reference_entry] = max_reference_pair
                            
                else:
                    # Add all
                    for entry, pair in label_pairs.items():
                        pairs[entry] = pair
                # Erase
                label_pairs = dict()
            else:
                # Else, recurse deeper
                innter_prefix = list(prefix)
                innter_prefix.append(label)
                __per_group__(innter_prefix, coder_masses)
    # Parse
    __per_group__(tuple(), dataset_masses)
    # Return mean, std dev, and variance
    return pairs


def summarize(pairs):
    return mean(pairs.values()), std(pairs.values()), var(pairs.values()), \
        stderr(pairs.values()), len(pairs)

