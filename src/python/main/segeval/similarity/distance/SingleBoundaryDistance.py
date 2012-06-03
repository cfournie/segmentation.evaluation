'''
Boundary edit distance for one boundary type [FournierInkpen2012]_.

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
from .MultipleBoundaryDistance import boundary_string_from_masses, \
    set_errors_transpositions_n_edits


def linear_edit_distance(segment_masses_a, segment_masses_b, n):
    '''
    Compute edit distance for linear single boundary type segmentations.
    
    :param segment_masses_a:  Segmentation masses.
    :param segment_masses_b:  Segmentation masses.
    :param n:                 The maximum number of PBs that boundaries can \
                                  span to be considered transpositions (n<2 \
                                  means no transpositions)
    :type segment_masses_a: list
    :type segment_masses_b: list
    :type beta: float
    '''
    # pylint: disable=C0103
    
    # Convert
    string_a = boundary_string_from_masses(segment_masses_a)
    string_b = boundary_string_from_masses(segment_masses_b)
    
    # There exist no boundaries at the beginning and end of linear single
    # boundary segmentations (that can differ)
    string_a[0]  = []
    string_a[-1] = []
    string_b[0]  = []
    string_b[-1] = []
    
    # Compute edit distance
    return set_errors_transpositions_n_edits(string_a, string_b, [1], n)
