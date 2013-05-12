'''
Segmentation evaluation metric package. Provides evaluation metrics to
evaluate the performance of both human and automatic text (i.e., discourse)
segmenters.  This package contains a new metric called Segmentation Similarity
(S) [FournierInkpen2012]_ which is recommended for usage along with a variety
of inter-coder agreement coefficients that utilize S.

To use S, see the :mod:`segeval.similarity` module.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import os
from decimal import Decimal
from collections import Counter
from .format import BoundaryFormat


# Package description
__version_number__ = '2.0'
__release__ = 'alpha'
__version__ = '-'.join((__version_number__, __release__))
__project_name__ = 'SegEval'
__package_name__ = 'segeval'
__author__ = 'Chris Fournier'
__author_email__ = 'chris.m.fournier@gmail.com'
__copyright__ = '2012-2013, ' + __author__


METRIC_DEFAULTS = {
    'boundary_format' : BoundaryFormat.mass,
    'permuted' : False,
    'one_minus' : False,
    'return_parts' : False
}