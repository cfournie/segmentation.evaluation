'''
Utility functions and classes for the package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
from segeval.compute import compute_pairwise_values


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


def __fnc_metric__(fnc_metric, args, kwargs, kw_defaults):

    from segeval.data import Dataset
    # Create default keyword arguments
    metric_kwargs = dict(kw_defaults)
    metric_kwargs.update(kwargs)
    # Initialize arguments
    hypothesis = None
    reference = None
    dataset = None
    # Parse arguments
    if len(args) == 2:
        hypothesis, reference = args
    elif len(args) == 1:
        dataset = args[0]
    elif len(args) == 0:
        if 'hypothesis' in kwargs and 'reference' in kwargs:
            hypothesis = kwargs['hypothesis']
            reference = kwargs['reference']
            del metric_kwargs['hypothesis']
            del metric_kwargs['reference']
        elif 'dataset' in kwargs:
            dataset = kwargs['dataset']
            del metric_kwargs['dataset']
        else:
            raise SegmentationMetricError('Expected either a reference and hypothesis or dataset argument.')
    # Fix the case when people put in just a single int by accident, e.g., (20) => (20,)
    if isinstance(hypothesis, int):
        hypothesis = (hypothesis, )
    if isinstance(reference, int):
        reference = (reference, )
    # Compute
    if dataset:
        # Compute pairwise values over all coders in a dataset
        metric_kwargs['boundary_format'] = dataset.boundary_format
        return compute_pairwise_values(fnc_metric, dataset, **metric_kwargs)
    elif hypothesis and reference:
        # Compute values between hypotheses (i.e, automatic) and reference
        # (i.e., manual) coder segmentations
        if isinstance(hypothesis, Dataset) and isinstance(reference, Dataset):
            # Compare pairwise values between coders paired from two datasets
            metric_kwargs['boundary_format'] = hypothesis.boundary_format
            if hypothesis.boundary_format is not reference.boundary_format:
                raise SegmentationMetricError(
                    'Datasets contain differing boundary formats; {0} != {1}'
                    .format(hypothesis.boundary_format, reference.boundary_format))
            return compute_pairwise_values(fnc_metric, hypothesis, reference, **metric_kwargs)
        else:
            # Compare a single pair of segmentations
            del metric_kwargs['permuted']
            return fnc_metric(hypothesis, reference, **metric_kwargs)
    # Except if insufficient arguments supplied
    raise SegmentationMetricError('Incorrect arguments specified; expected 1 or 2, obtained {0} of value: {1}'.format(str(len(args)), str(args)))
