'''
Utility functions and classes for the package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from ..compute import compute_pairwise_values


def __fnc_metric__(fnc_metric, args, kwargs, kw_defaults):
    # pylint: disable=W0142
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
        elif 'dataset' in kwargs:
            dataset = kwargs['dataset']
    # Compute
    if dataset:
        metric_kwargs['boundary_format'] = dataset.boundary_format
        return compute_pairwise_values(dataset, fnc_metric, **metric_kwargs)
    elif hypothesis and reference:
        del metric_kwargs['permuted']
        return fnc_metric(hypothesis, reference, **metric_kwargs)
    # Except if insufficient arguments supplied
    raise Exception('Correct number of arguments not specified.')

