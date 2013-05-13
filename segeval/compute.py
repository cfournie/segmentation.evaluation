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
    from .data.jsonutils import FIELD_HAS_REFERENCE_CODER
    pairs = dict()
    fnc_kwargs = dict(kwargs)
    permuted = fnc_kwargs['permuted']
    return_parts = fnc_kwargs['return_parts']
    del fnc_kwargs['permuted']
    reference_coder_exists = False
    # Determine whether a reference coder is designated
    if FIELD_HAS_REFERENCE_CODER in dataset_masses.properties:
        reference_coder_exists = \
            dataset_masses.properties[FIELD_HAS_REFERENCE_CODER]
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
                isinstance(coder_masses.values()[0], list):
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
    __per_group__(list(), dataset_masses)
    # Return mean, std dev, and variance
    return pairs


def summarize(pairs):
    return mean(pairs.values()), std(pairs.values()), var(pairs.values()), \
        stderr(pairs.values()), len(pairs)


def compute_multiple_values(dataset, fnc_metric, kwargs_metric):
    '''
    Calculate segmentation metric values for functions that take
    dicts of items and their segmentations per coder (``items_masses``) while
    ensuring that all coders code all items in each group (dividing data as
    necessary into subgroups groups).
    
    .. seealso:: :func:`segeval.agreement.observed_agreement` for an example of\
     ``items_masses``.
    
    :param dataset: Segmentation mass dataset (including multiple \
                           codings).
    :param fnc_metric:     Metric function to call on segmentation mass pairs.
    :type dataset: dict
    :type fnc_metric:     func
    
    .. |compute_mean_return| replace:: Mean, standard deviation, variance, and \
        standard error of a segmentation metric.
    .. |compute_mean_return_type| replace:: :class:`decimal.Decimal`, \
        :class:`decimal.Decimal`, :class:`decimal.Decimal`, \
        :class:`decimal.Decimal`
        
    :returns: List of values produced by the specified metric
    :rtype: :class:`list` of :class:`decimal.Decimal`
    '''
    from .data import Dataset
    datasets = dict()
    values = dict()
    # pylint: disable=C0103
    if len(dataset) > 1:
        # Filter items by identical coders
        for item, coder_masses in dataset.items():
            coders = coder_masses.keys()
            coders.sort()
            coders = '+'.join(coders)
            if coders not in datasets:
                datasets[coders] = Dataset(properties=dataset.properties,
                                        boundary_types=dataset.boundary_types)
            datasets[coders][item] = coder_masses
        # If in the end there's only one set
        if len(values) is 1:
            values = {'all' : values.values()[0]}
    else:
        datasets['all'] = dataset
    # Define fnc per group
    for coders, cur_dataset in datasets.items():
        values[coders] = fnc_metric(cur_dataset, **kwargs_metric)
    # Return mean, std dev, and variance
    return values


def create_tsv_rows(header, values, expand=False):
    '''
    Convert a dict of values into a list of properly padded rows.
    
    :param filepath: Path and filename of a file to write to
    :param header:   List of known category names
    :param values:   Dict of computed values
    :type header: :class:`list`
    :type values: :class:`dict`
    '''
    # pylint: disable=R0914
    # Parse labels
    rows = list()
    max_len = 0
    for key, value in values.items():
        # Get label parts
        items_parts = key.split(',')
        # Expand if we are creating multiple rows per label part
        subvalues = None
        if expand:
            subvalues = value
        else:
            subvalues = [value]
        # Create rows
        for subvalue in subvalues:
            row = list(items_parts)
            if isinstance(subvalue, list):
                row.extend(subvalue)
            else:
                row.append(subvalue)
            rows.append(row)
            max_len = len(row) if len(row) > max_len else max_len
    # Pad rows to match the max depth/number of labels
    padded_rows = list()
    for row in rows:
        difference = max_len - len(row)
        if difference > 0:
            padded_row = list([''] * difference)
            padded_row.extend(row)
            padded_rows.append(padded_row)
        else:
            padded_rows.append(row)
    # Pad headers to match the depth/number of labels
    labels = max_len - len(header)
    padded_header = ['label%i' % i if i > 1 else 'label' \
                     for i in xrange(1, labels + 1)]
    padded_header.extend(header)
    # Return
    return padded_header, padded_rows

