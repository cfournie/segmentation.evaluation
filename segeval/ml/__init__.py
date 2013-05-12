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
from __future__ import division
from decimal import Decimal
from collections import defaultdict
from ..util.math import mean


MICRO, MACRO = range(2)


def __value_micro_macro__(fnc, classes, arguments, classification=None,
                          version=MICRO):
    # pylint: disable=W0142
    if classification is None:
        if version is MICRO:
            # Micro-average
            numerator, denominator = 0, 0
            for classification in classes:
                arguments['classification'] = classification
                arguments['return_parts'] = True
                class_numerator, class_denominator = fnc(**arguments)
                numerator += class_numerator
                denominator += class_denominator
            if numerator == 0:
                return 0
            else:
                return Decimal(numerator) / denominator
        elif version is MACRO:
            # Macro-average
            values = list()
            for classification in classes:
                arguments['classification'] = classification
                value = fnc(**arguments)
                values.append(value)
            return mean(values)
    else:
        return fnc(**arguments)

    
def __precision__(matrix, classification, return_parts=False):
    # pylint: disable=C0103
    predicted = classification
    denominator = 0
    for actual in matrix.classes():
        denominator += matrix[predicted][actual]
    numerator = matrix[classification][classification]
    if return_parts:
        return numerator, denominator
    else:
        if numerator is 0:
            return Decimal(0)
        else:
            return Decimal(numerator) / Decimal(denominator)


def __recall__(matrix, classification, return_parts=False):
    # pylint: disable=C0103
    actual = classification
    denominator = 0
    for predicted in matrix.classes():
        denominator += matrix[predicted][actual]
    numerator = matrix[classification][classification]
    if return_parts:
        return numerator, denominator
    else:
        if numerator is 0:
            return Decimal(0)
        else:
            return Decimal(numerator) / Decimal(denominator)


def __fmeasure__(matrix, classification=None, beta=Decimal('1.0'),
                 return_parts=False):
    '''
    Calculate F-measure, also known as F-score.
    
    .. math::
        \\text{F}_{\\beta}\\text{-measure} = \\frac{(1 + \\beta^2) \\cdot TP}\
        {(1 + \\beta^2) \\cdot TP + \\beta^2 \\cdot FN + FP}
    
    :param matrix: Confusion matrix
    :param predicted: Precision for this classification label
    
    :type matrix: :class:`ConfusionMatrix`
    
    :returns: F-measure.
    :rtype: :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103
    class_precision = __precision__(matrix, classification)
    class_recall = __recall__(matrix, classification)
    if not return_parts and (class_precision == 0 or class_recall == 0):
        return 0
    else:
        # Convert to Decimal
        beta = Decimal(str(beta))
        # Calculate terms
        beta2   = beta ** 2
        beta2_1 = Decimal('1.0') + beta2
        numerator   = beta2_1 * class_precision * class_recall
        denominator = (beta2 * class_precision) + class_recall
        if return_parts:
            return numerator, denominator
        else:
            return Decimal(numerator) / Decimal(denominator)


def precision(matrix, classification=None, version=MICRO):
    '''
    Calculate precision.
    
    :param matrix: Confusion matrix
    :param classification: Precision for this classification label
    :param version: MICRO or MACRO precision

    :type matrix: :class:`ConfusionMatrix`
    
    :returns: Precision.
    :rtype: :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103
    classes = matrix.classes()
    arguments = dict()
    arguments['matrix'] = matrix
    arguments['classification'] = classification
    return __value_micro_macro__(__precision__, classes, arguments,
                                 classification, version)


def recall(matrix, classification=None, version=MICRO):
    '''
    Calculate recall.
    
    :param matrix: Confusion matrix
    :param classification: Recall for this classification label
    :param version: MICRO or MACRO recall

    :type matrix: :class:`ConfusionMatrix`
    
    :returns: Precision.
    :rtype: :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103
    classes = matrix.classes()
    arguments = dict()
    arguments['matrix'] = matrix
    arguments['classification'] = classification
    return __value_micro_macro__(__recall__, classes, arguments, classification,
                                 version)


def fmeasure(matrix, classification=None, beta=Decimal('1.0'), version=MICRO):
    '''
    Calculate FMeasure.
    
    :param matrix: Confusion matrix
    :param classification: FMeasure for this classification label
    :param version: MICRO or MACRO FMeasure

    :type matrix: :class:`ConfusionMatrix`
    
    :returns: Precision.
    :rtype: :class:`decimal.Decimal`
    '''
    # pylint: disable=C0103
    classes = matrix.classes()
    arguments = dict()
    arguments['matrix'] = matrix
    arguments['classification'] = classification
    arguments['beta'] = beta
    return __value_micro_macro__(__fmeasure__, classes, arguments,
                                 classification, version)


class _InnerConfusionMatrix(defaultdict):
    '''
    Inner dict of the confusion matrix; used to determine when the classes list
    is dirty.
    '''
    # pylint: disable=R0903
    
    def __init__(self, parent):
        self.__parent__ = parent
        defaultdict.__init__(self, int)

    def __setitem__(self, key, value):
        self.__parent__.__dirty_classes__ = True
        defaultdict.__setitem__(self, key, value)


class ConfusionMatrix(dict):
    '''
    Dict representation of a confusion matrix:
    
    matrix[predicted][actual]
    '''
    __classes__ = set()
    __dirty_classes__ = False
    
    def __setitem__(self, key, value):
        raise AttributeError('no such method')
        
    def __getitem__(self, key):
        '''
        Return default dicts and store them so that the following is possible:
        
        >>> matrix = ConfusionMatrix()
        >>> matrix['a']['b'] += 1
        >>> matrix['a']['b']
        1
        >>> matrix['a']['a'] = 1
        >>> matrix['a']['a']
        1
        >>> matrix['c']['d']
        0
        
        '''
        value = None
        if key not in self:
            value = _InnerConfusionMatrix(self)
            dict.__setitem__(self, key, value)
        else:
            value = dict.__getitem__(self, key)
        return value

    def classes(self):
        '''
        Retrieve the set of all classes.
        '''
        if self.__dirty_classes__:
            self.__classes__ = set()
            for predicted, values in self.items():
                self.__classes__.add(predicted)
                for actual in values.keys():
                    self.__classes__.add(actual)
            self.__dirty_classes__ = False
        return self.__classes__


__all__ = [MICRO, MACRO, precision, recall, fmeasure, ConfusionMatrix]

