'''
Machine learning metric package.  This package a variety of traditional machine
learning metrics that have been adapted for use in segmentation, including:

* F-measure; and
* Percentage agreement.

.. warning:: These are provided for comparison, but are not recommended for \
    segmentation evaluation.  Instead, use  the segmentation similarity
    metric [FournierInkpen2012]_ implemented in
    :func:`segeval.similarity.SegmentationSimilarity.similarity` and the
    associated inter-coder agreement coefficients in
    :mod:`segeval.agreement`.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from decimal import Decimal
from collections import defaultdict


def load_tests(loader, tests, pattern):
    '''
    A ``load_tests()`` function utilizing the default loader
    :func:`segeval.Utils.default_load_tests`.
    
    .. seealso:: The `load_tests protocol <http://docs.python.org/library/\
    unittest.html#load-tests-protocol>`_.
    '''
    #pylint: disable=W0613
    from ..utils import default_load_tests
    return default_load_tests(__file__, loader, tests)


def precision(cf):
    '''
    Calculate precision.
    
    .. math::
        \\text{Precision} = \\frac{TP}{TP + FP}
    
    :param tp: Number of true positives
    :param fp: Number of false positives
    
    :returns: Precision.
    :rtype: :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103
    if cf['tp'] is 0:
        return Decimal(0)
    else:
        return Decimal(cf['tp']) / Decimal(cf['tp'] + cf['fp'])
    
    
def recall(cf):
    '''
    Calculate recall.
    
    .. math::
        \\text{Recall} = \\frac{TP}{TP + FN}
    
    Arguments:
    :param tp: Number of true positives
    :param fn: Number of false negatives
    
    :returns: Recall.
    :rtype: :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103
    if cf['tp'] is 0:
        return Decimal(0)
    else:
        return Decimal(cf['tp']) / Decimal(cf['tp'] + cf['fn'])


def fmeasure(cf, beta=Decimal('1.0')):
    '''
    Calculate F-measure, also known as F-score.
    
    .. math::
        \\text{F}_{\\beta}\\text{-measure} = \\frac{(1 + \\beta^2) \\cdot TP}\
        {(1 + \\beta^2) \\cdot TP + \\beta^2 \\cdot FN + FP}
    
    :param tp: Number of true positives.
    :type tp: int
    :param fp: Number of false positives.
    :type fp: int
    :param fn: Number of false negatives.
    :type fn: int
    :param beta: Scales how precision and recall are averaged.
    :type beta: double
    
    :returns: F-measure.
    :rtype: :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103
    if cf['tp'] is 0 and cf['fp'] is 0 and cf['fn'] is 0:
        return Decimal('0')
    else:
        # Convert to Decimal
        tp   = Decimal(cf['tp'])
        fp   = Decimal(cf['fp'])
        fn   = Decimal(cf['fn'])
        beta = Decimal(str(beta))
        # Calculate terms
        beta2   = beta ** 2
        beta2_1 = Decimal('1.0') + beta2
        numerator   = beta2_1 * tp
        denomenator = (beta2_1 * tp) + (beta2 * fn) + fp
        # Perform division
        return numerator / denomenator


def vars_to_cf(tp, fp, fn, tn):
    '''
    Converts a set of variables to a confusion matrix dict.
    
    :param tp: Number of true positives.
    :param fp: Number of false positives.
    :param fn: Number of false negatives.
    :param tn: Number of true negatives.
    :type tp: int
    :type fp: int
    :type fn: int
    :type tn: int
    
    :returns: A dict representing a confusion matrix.
    :rtype: :func:`dict` containing tp, fp, fn, tn values.
    '''
    # pylint: disable=C0103
    return {'tp' : tp, 'fp' : fp, 'fn' : fn, 'tn' : tn}


def cf_to_vars(cf):
    '''
    Converts a set of variables to a confusion matrix dict.
    
    :param tp: Number of true positives.
    :param fp: Number of false positives.
    :param fn: Number of false negatives.
    :param tn: Number of true negatives.
    :type tp: int
    :type fp: int
    :type fn: int
    :type tn: int
    
    :returns: A dict representing a confusion matrix.
    :rtype: :func:`dict` containing tp, fp, fn, tn values.
    '''
    # pylint: disable=C0103
    return cf['tp'], cf['fp'], cf['fn'], cf['tn']


def find_boundary_position_freqs(masses_set):
    '''
    Converts a list of segmentation mass sets into a dict of boundary positions,
    and the frequency of the whether boundaries were chosen at that location or,
    or not,
    
    :param masses_set: List of segmentation masses
    :type masses_set: list
    
    :returns: :func:`dict` of boundary position frequencies.
    :rtype: :class:`decimal.Decimal`
    '''
    seg_positions = dict()
    for masses in masses_set:
        # Iterate over boundary positions that precede the index, excluding the
        # first position so that the start is not counted as a boundary
        for i in xrange(1, len(masses)):
            position = sum(masses[0:i])
            try:
                seg_positions[position] += 1
            except KeyError:
                seg_positions[position] = 1
    return seg_positions


class ConfusionMatrix(dict):
    
    def add(self, predicted, actual, value=1):
        self.__check__(predicted)
        self[predicted][actual] += value

    def get(self, predicted, actual):
        self.__check__(predicted)
        return self[predicted][actual]
    
    def __check__(self, predicted):
        if predicted not in self:
            self[predicted] = defaultdict(int)

