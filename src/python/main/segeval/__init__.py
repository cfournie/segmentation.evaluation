'''
Segmentation evaluation metric package. Provides evaluation metrics to
evaluate the performance of both human and automatic text (i.e., discourse)
segmenters.  This package contains a new metric called Segmentation Similarity
(S) [FournierInkpen2012]_ which is recommended for usage along with a variety
of inter-coder agreement coefficients that utilize S.

To use S, see the :mod:`segeval.similarity` module.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2011-2012, Chris Fournier
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#       
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================
import os
from decimal import Decimal
from collections import Counter
from .Math import mean, std, var, stderr


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        os.sep.join(['..'] * 1)))

DEBUG_MODE  = False
EXPERIMENTS = False


def load_tests(loader, tests, pattern):
    '''
    A ``load_tests()`` function utilizing the default loader
    :func:`segeval.Utils.default_load_tests`.
    
    .. seealso:: The `load_tests protocol <http://docs.python.org/library/\
    unittest.html#load-tests-protocol>`_.
    '''
    #pylint: disable=W0613
    from Utils import default_load_tests
    return default_load_tests(__file__, loader, tests)


def convert_positions_to_masses(positions):
    '''
    Convert an ordered sequence of boundary position labels into a
    sequence of segment masses, e.g., ``[1,1,1,1,1,2,2,2,3,3,3,3,3]`` becomes
    ``[5,3,5]``.
    
    :param segments: Ordered sequence of which segments a unit belongs to.
    :type segments: list
    
    :returns: Segment mass sequence.
    :rtype: :func:`list`
    
    .. deprecated:: 1.0
    '''
    counts = Counter(positions)
    masses = list()
    for i in range(1, max(counts.keys()) + 1):
        masses.append(counts[i])
    return masses


def convert_masses_to_positions(masses):
    '''
    Converts a sequence of segment masses into an ordered sequence of section
    labels for each unit, e.g., ``[5,3,5]`` becomes
    ``[1,1,1,1,1,2,2,2,3,3,3,3,3]``.
    
    :param masses: Segment mass sequence.
    :type masses: list
    
    :returns: Ordered sequence of which segments a unit belongs to.
    :rtype: :func:`list`
    '''
    sequence = list()
    for i, mass in enumerate(masses):
        sequence.extend([i + 1] * mass)
    return sequence


def compute_pairwise(dataset_masses, fnc_metric, permuted=False):
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
    
    :returns: |compute_mean_return|
    :rtype: |compute_mean_return_type|
    '''
    pairs = compute_pairwise_values(dataset_masses, fnc_metric, permuted)
    return mean(pairs.values()), std(pairs.values()), var(pairs.values()), \
        stderr(pairs.values()), len(pairs)


def compute_pairwise_values(dataset_masses, fnc_metric, permuted=False,
                            return_parts=False):
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
    # pylint: disable=C0103,R0912
    from .data.JSON import FIELD_HAS_REFERENCE_CODER
    pairs = dict()
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
                                fnc_metric(segs_m, segs_n,
                                                   return_parts=return_parts)
                        else:
                            label_pairs[entry] = fnc_metric(segs_m, segs_n)
                        # Handle permutation
                        if permuted:
                            entry_parts = list(prefix)
                            entry_parts.extend([label, str(n), str(m)])
                            entry = ','.join(entry_parts)
                            if return_parts:
                                label_pairs[entry] = \
                                    fnc_metric(segs_n, segs_m,
                                                    return_parts=return_parts)
                            else:
                                label_pairs[entry] = fnc_metric(segs_n, segs_m)
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
                    if max_reference_entry != None:
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


def compute_multiple_values(dataset, fnc_metric):
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
                datasets[coders] = Dataset()
            datasets[coders][item] = coder_masses
        # If in the end there's only one set
        if len(values) == 1:
            values = {'all' : values.values()[0]}
    else:
        datasets['all'] = dataset
    # Define fnc per group
    for coders, cur_dataset in datasets.items():
        values[coders] = fnc_metric(cur_dataset)
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


def parser_micro_support(parser):
    '''
    Add support for the "micro" mean parameter to instead return a micro mean.
    
    :param parser: Argument parser
    :type parser: argparse.ArgumentParser
    '''
    parser.add_argument('-m', '--micro',
                        action='store_true',
                        default=False,
                        help='Specifies that a micro mean is to be returned;'+\
                        ' default is macro mean.')


class SegmentationMetricError(Exception):
    '''
    Indicates that a runtime check has failed, and the algorithm is performing
    incorrectly, or input validation has failed.  Generation of this exception
    is tested.
        
    :param message: Explanation for the exception.
    :type message: str
    '''
    
    def __init__(self, message):
        '''
        Initializer.
        
        :param message: Explanation for the exception.
        :type message: str
        '''
        Exception.__init__(self, message)


class InputError(Exception):
    '''
    Indicates that an input parameter is invalid.
        
    :param message: Explanation for the exception.
    :type message: str
    '''
    
    def __init__(self, message):
        '''
        Initializer.
        
        :param message: Explanation for the exception.
        :type message: str
        '''
        Exception.__init__(self, message)

