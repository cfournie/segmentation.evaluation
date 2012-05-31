'''
Inter-coder agreement metrics.  This module provides inter-coder agreement
metrics adapted for segmentation (read [FournierInkpen2012]_) that make use of
segmentation similarity [FournierInkpen2012]_, including:

* Kappa [Cohen1960]_, [DaviesFleiss1982]_ and
* Pi [Scott1955]_, [Fleiss1971]_

To discuss measures of inter-coder (or inter-annotator) agreement, we use a
modified version of [ArtsteinPoesio2008]_'s terminology, as presented in
[FournierInkpen2012]_, where the set of:

* *Items* is :math:`\{i|i \in I\}` with cardinality **i**;
* *Categories* is :math:`\{k|k \in K\}` with cardinality **k**;
* *Coders* is :math:`\{c|c \in C\}` with cardinality **c**;
* *Segmentations* of an item :math:`i` by a coder :math:`c` is 
  :math:`\{s|s \in S\}`, where when :math:`s_{ic}`  is specified with only one
  subscript, it denotes :math:`s_{c}`, for all relevant items (:math:`i`); and
* *Types* of segmentation boundaries is :math:`\{t|t \in T\}` with
  cardinality **t**.

For segmentation, we assume that the set of categories is the
presence of a segmentation boundary :math:`\\text{seg}` of type
:math:`t` at a position in a segmentation [FournierInkpen2012]_:

.. math::
    K = \\{\\text{seg}_t | t \in T\\}

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
import math
from decimal import Decimal
from ..similarity.SegmentationSimilarity import similarity as similarity_linear


def load_tests(loader, tests, pattern):
    '''
    A ``load_tests()`` function utilizing the default loader
    :func:`segeval.Utils.default_load_tests`.
    
    .. seealso:: The `load_tests protocol <http://docs.python.org/library/\
    unittest.html#load-tests-protocol>`_.
    '''
    #pylint: disable=W0613
    from ..Utils import default_load_tests
    return default_load_tests(__file__, loader, tests)


def choose(n, k):
    '''
    Calculates a number of combinations (i.e., 4 choose 2).
    
    .. math::
        C(n,k) = \\frac{n!}{k!(n-k)!}
    
    :param n: Number of elements to choose from.
    :param k: Number of elements to chose.
    
    :returns: Number of combinations.
    :rtype: :func:`int`
    '''
    # pylint: disable=C0103
    numerator   = math.factorial(n)
    denominator = (math.factorial(k) * math.factorial(n-k))
    return numerator / denominator


def permute(n, k):
    '''
    Calculates a number of permutations (i.e., 4 permute 2).
    
    .. math::
        P(n,k) = \\frac{n!}{(n-k)!}
    
    :param n: Number of elements to permute from.
    :param k: Number of elements to permute.
    
    :returns: Number of permutations.
    :rtype: :func:`int`
    '''
    # pylint: disable=C0103
    numerator   = math.factorial(n)
    denominator = (math.factorial(n-k))
    return numerator / denominator


def actual_agreement(items_masses):
    '''
    Calculate actual (i.e., observed or :math:`\\text{A}_a`), segmentation
    agreement without accounting for chance, using [ArtsteinPoesio2008]_'s
    formulation as adapted in [FournierInkpen2012]_:
    
    .. math::
        \\text{A}_a = \\frac{
            \sum_{i \in I} \\text{mass}(i) \cdot \\text{S}(s_{i1},s_{i2})
        }{
            \sum_{i \in I} \\text{mass}(i) 
        }
        
    Or, for more than two coders:
    
    .. math::
        \\text{A}_a = \\frac{1}{{\\textbf{c} \\choose 2}}
        \sum^{\\textbf{c}-1}_{m=1}
        \sum^{\\textbf{c}}_{n=m+1}
        \\frac{
            \sum_{i \in I} \\text{mass}(i) \cdot \\text{S}(s_{im},s_{in})
        }{
            \sum_{i \in I} \\big( \\text{mass}(i) - 1 \\big)
        }
        
    Where :math:`\\text{S}(s_{i1},s_{i2})` is defined in 
    :func:`segeval.similarity.SegmentationSimilarity.similarity`.
    
    :param items_masses: Segmentation masses for a collection of items where \
                        each item is multiply coded (all coders code all items).
    :type items_masses: dict
    
    :returns: Potential boundaries unmoved, all potential boundaries, and the \
              boundaries per coder.
    :rtype: :func:`list`, :func:`list`, :func:`dict`
    
    An example of the dictionary structure if the ``items_masses``
    parameter is::
    
            items_masses = {
                'item1' : {
                    'coder1' : [5],
                    'coder2' : [2,3],
                    'coder2' : [1,1,3]
                },
                'item2' : {
                    'coder1' : [8],
                    'coder2' : [4,4],
                    'coder2' : [2,2,4]
                }
            }
    
    Other real and contrived examples can be found in 
    :mod:`segeval.data.Samples`.
    
    '''
    # pylint: disable=C0103
    all_pbs_unedited = list()
    all_pbs          = list()
    coders_boundaries = dict()
    coders = items_masses.values()[0].keys()
    # FOr each permutation of coders
    for m in range(0, len(coders) - 1):
        for n in range(m+1, len(coders)):
            for item in items_masses.keys():
                segs_a = items_masses[item][coders[m]]
                segs_b = items_masses[item][coders[n]]
                pbs_unedited, total_pbs = \
                    similarity_linear(segs_a, segs_b, return_parts=True)[0:2]
                all_pbs_unedited.append(pbs_unedited)
                all_pbs.append(total_pbs)
                # Create in dicts if not present
                if coders[m] not in coders_boundaries:
                    coders_boundaries[coders[m]] = list()
                if coders[n] not in coders_boundaries:
                    coders_boundaries[coders[n]] = list()
                # Add per-coder values to dicts
                coders_boundaries[coders[m]].append(
                    [Decimal(len(segs_a)),
                     total_pbs])
                coders_boundaries[coders[n]].append(
                    [Decimal(len(segs_b)),
                     total_pbs])
    return all_pbs_unedited, all_pbs, coders_boundaries

