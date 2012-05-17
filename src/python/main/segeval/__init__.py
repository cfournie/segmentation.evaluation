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
from numpy import mean, std, var
from collections import Counter

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
    Calculate mean pairwise segmentation metric values.
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :param fnc_metric:     Metric function to call on segmentation mass pairs.
    :param permuted:       Permute coder combinations if true.
    :type dataset_masses: dict
    :type fnc_metric:     func
    :type permuted:       bool
    
    :returns: Mean, standard deviation, and variance of segmentation metric.
    :rtype: :func:`float`, :func:`float`, :func:`float`
    '''
    # pylint: disable=C0103
    values = list()
    # Define fnc per group
    def __per_group__(inner_dataset_masses):
        '''
        Calculate pairwise segmentation F-Measure for each group and append to
        output.
        
        
        '''
        for coder_masses in inner_dataset_masses.values():
            if len(coder_masses.values()) > 0 and \
                isinstance(coder_masses.values()[0], list):
                # If is a group
                coders = coder_masses.keys()
                for m in range(0, len(coders)):
                    for n in range(m+1, len(coders)):
                        segs_m = coder_masses[coders[m]]
                        segs_n = coder_masses[coders[n]]
                        values.append(float(fnc_metric(segs_m, segs_n)))
                        if permuted:
                            values.append(float(fnc_metric(segs_n, segs_m)))
            else:
                # Else, recurse deeper
                __per_group__(coder_masses)
    # Parse
    __per_group__(dataset_masses)
    # Return mean, std dev, and variance
    return mean(values), std(values), var(values)


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

