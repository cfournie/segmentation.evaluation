'''
Multiple-boundary edit distance.  Detailed in [FournierInkpen2012]_.

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
from decimal import Decimal


NO_BOUNDARY = '-'
BOUNDARY    = '|'


def boundary_string_from_masses(segment_masses):
    '''
    Creates a "boundary string", or sequence of boundary type sets.
    
    :param segment_masses: Segmentation masses.
    :type segment_masses:  list
    :returns: A sequence of boundary type sets
    :rtype: :func:`list` of :func:`set` onjects containing :func:`int` values.
    '''
    string = [set() for _ in xrange(0, sum(segment_masses) + 1)]
    
    pos = 0
    for mass in segment_masses:
        string[pos].add(1)
        string[pos + mass].add(1)
        pos += mass
    
    return [list(pb) for pb in string]



class SetError(object):
    '''
    Represents a set error at a particular potential boundary position.
    '''
    # pylint: disable=R0903
    
    def __init__(self, position, boundaries, boundary_types):
        '''
        Creates an object that represents a set error.
        
        :param position:      Position where the error occurs
        :param boundaries:    Number of boundaries involved.
        :param boundary_type: Boundary types involved.
        :type position:    int
        :type boundaries:  bool
        :type types:       bool
        '''
        # pylint: disable=C0103
        self.start          = position
        self.end            = position
        self.boundaries     = boundaries
        self.boundary_types = boundary_types
    
    def overlaps(self, other):
        '''
        Tests to see whether a transposition error overlaps with this set error.
        
        :param other: Other error object (usually a :func:`Transposition`)
        
        :returns: True if overlapping, False otherwise.
        :rtype: :func:`bool`
        '''
        overlap = False
        # Test bounds
        if other.boundary_type in self.boundary_types:
            if other.start >= self.start and other.start <= self.end:
                overlap = True
            elif other.end >= self.start and other.end <= self.end:
                overlap = True
            elif self.start >= other.start and self.start <= other.end:
                overlap = True
            elif self.end >= other.start and self.end <= other.end:
                overlap = True
        # Return
        return overlap
    
    def __str__(self):
        return '(%i,%i) b=%i t=%s' % (self.start, self.end,
                                        self.boundaries,
                                        ','.join(self.boundary_types))


def compare_sets(position, set_a, set_b):
    '''
    Calculate the number of substitution or addition/deletion operations
    required to edit one set to be the other.
    
    :param position: Position to calculate set error upon
    :param set_a:    First set to edit
    :param set_b:    Second set to edit
    :type position:  int
    :type set_a:     :func:`set` or :func:`list`
    :type set_b:     :func:`set` or :func:`list`
    
    :returns: A list of the substitutions and list of additions/deletions /
        performed
    :rtype: :func:`list`, :func:`list`
    '''
    # pylint: disable=W0141
    set_a, set_b = set(set_a), set(set_b)
    
    diff_ab = set_a.difference(set_b)
    diff_ba = set_b.difference(set_a)
    
    pairs = map(None, list(diff_ab), list(diff_ba))
    
    num_substitutions = min(len(diff_ab), len(diff_ba))
    num_add_or_del    = abs(len(diff_ab) - len(diff_ba))
    
    substitutions = list()
    add_or_del    = list()
    
    for pair in pairs:
        pair = list(pair)
        if None in pair:
            pair.remove(None)
            add_or_del.append(SetError(position, 1, pair))
        else:
            substitutions.append(SetError(position, 2, pair))
    
    if num_substitutions != len(substitutions):
        raise Exception('Incorrect substitution calculation')
    if num_add_or_del != len(add_or_del):
        raise Exception('Incorrect add_or_del calculation')
    
    return substitutions, add_or_del


def calculate_set_errors(string_a, string_b):
    '''
    Calculate set errors for two parallel boundary strings produced by
    :func:`boundary_string_from_masses`.
    
    .. seealso:: :func:`boundary_string_from_masses`
    
    :param string_a: Boundary string.
    :param string_b: Boundary string.
    :type string_a:  :func:`list` of :func:`set` onjects containing :func:`int`
    :type string_b:  :func:`list` of :func:`set` onjects containing :func:`int`
    :returns: Number of errors, and detailed information on errors as a list of\
        error objects
    :rtype: func:`int`, :func:`list`
    '''
    set_error_details = list()
    for i in range(0, len(string_a)):
        boundary_type_a_i = []
        boundary_type_b_i = []
        try:
            boundary_type_a_i = string_a[i]
        except KeyError:
            pass
        try:
            boundary_type_b_i = string_b[i]
        except KeyError:
            pass
        substitutions, add_or_del = compare_sets(i,
                                                 boundary_type_a_i,
                                                 boundary_type_b_i)
        set_error_details.extend(substitutions)
        set_error_details.extend(add_or_del)
    return set_error_details


class Transposition(object):
    '''
    Represents a transposition error that spans a sequence of potential
    boundary position.
    '''
    
    def __init__(self, start, end, boundary_type, boundaries):
        '''
        Creates an object that represents a transposition error.
        
        :param start:         Position of the beginning boundary in the \
                              transposition
        :param end:           Position of the end boundary in the transposition
        :param boundary_type: Type of boundary
        :param boundaries:    Number of boundaries involved in a transposition
        :type start:         int
        :type end:           int
        :type boundary_type: int
        :type boundaries:    int
        
        '''
        # pylint: disable=C0103
        self.start         = start
        self.end           = end
        self.boundaries    = boundaries
        self.boundary_type = boundary_type
        self.n             = (end - start) + 1
    
    def overlaps(self, other):
        '''
        Check to see if a transposition overlaps.
        '''
        overlap = False
        
        if other.boundary_type == self.boundary_type:
            if other.start >= self.start and other.start <= self.end:
                overlap = True
            elif other.end >= self.start and other.end <= self.end:
                overlap = True
            elif self.start >= other.start and self.start <= other.end:
                overlap = True
            elif self.end >= other.start and self.end <= other.end:
                overlap = True
        
        return overlap
    
    def te(self):      # pylint: disable=C0103
        '''
        Transposition error scaling function (te).
        
        .. math::
            \\text{te}(n,b)=b-(^1/_b)^{n-2} \quad \\text{where } n \geq 2 \\text{ and } b > 0
        
        :param n: PBs over which transpositions are allowed
        :param b: number of boundaries involved in the current transposition
        :type n: int
        :type b: int
        
        :returns: Scaled penalty for the transposition in question
        :rtype: :class:`decimal.Decimal`
        '''
        max_penalty = Decimal(self.boundaries*2)
        discount = (Decimal(1)/Decimal(self.boundaries*2)) ** (self.n-2)
        return max_penalty - discount
    
    def __str__(self):
        return '(%i,%i) b=%i t=%i' % (self.start, self.end, self.boundaries,
                                      self.boundary_type)
        

def set_errors_transpositions_n_edits(string_a, string_b, boundary_types, n):
    '''
    Computes edit distance of boundary strings using n-wise transpositions and
    substitutions (symmetrically).
    
    Arguments:
    :param string_a:       Boundary string
    :param string_b:       Boundary string to compare against
    :param boundary_types: Boundary types used
    :param n:              Maximum transposition window size allows (e.g. \
                                allows off by n-1)
    :type string_a:       :func:`list` of :func:`set` onjects containing \
                            :func:`int`
    :type string_b:       :func:`list` of :func:`set` onjects containing \
                            :func:`int`
    :type boundary_types: :func:`list` of :func:`int`
    :type n:                int
    
    .. seealso:: :func:`boundary_string_from_masses`
    
    :returns: edit distance, list of transpositions per position, and a list of 
        set errors (additions/substitutions)
    :rtype: func:`int`, func:`list` of class:`Transposition`, func:`list` of \
        class:`SetError`
    '''
    # pylint: disable=R0914,C0103,R0912
    
    # Identify the number of direct set errors
    set_errors = calculate_set_errors(string_a, string_b)
    
    # Define boundary type string renderer
    def render_boundary_type_string(subsequence, boundary_type):
        '''
        Creates an actual string representing boundaries of one type for a 
        subsequence of the large boundary set sequence.
        
        :param subsequence:   sequence of boundary type sets
        :param boundary_type: boundary type
        :type subsequence:    func:`list` of :func:`set` onjects containing \
                                :func:`int`
        :type boundary_type:  int
        '''
        string = ''
        for part in subsequence:
            if boundary_type in part:
                string += BOUNDARY
            else:
                string += NO_BOUNDARY
        return string
    
    set_transpositions = list()
    
    def find_overlapping_transpositions(current):
        '''
        Find transpositions which overlap each other.
        
        :param current: Transposition
        :type current:  Transposition
        
        :returns: Overlapping transpositions and the number of boundaries that \
            they span
        :rtype: :func:`list` of :class:`Transposition`, :func:`int`
        '''
        overlap = list()
        boundaries = 0
        for transposition in set_transpositions:
            if transposition.overlaps(current):
                overlap.append(transposition)
                boundaries += transposition.boundaries
        return overlap, boundaries
        
    # Identify the number of transposed set items if n >= 2
    if n >= 2:
        pairs = zip(string_a, string_b)
        test_n = range(2, n+1)
        for n_i in test_n:
            i = 0
            while i < len(pairs) - 1:
                # If out of the range
                if n_i + i > (len(pairs)):
                    break
                
                # Get subsequences
                pos_start = i
                pos_end   = (i+n_i)
                pairs_i  = pairs[pos_start:pos_end]
                subseq_a = [pair[0] for pair in pairs_i]
                subseq_b = [pair[1] for pair in pairs_i]
                
                # Look for transpositions by type
                types_transposed = list()
                for boundary_type in boundary_types:
                    string_t_a = render_boundary_type_string(subseq_a,
                                                             boundary_type)
                    string_t_b = render_boundary_type_string(subseq_b,
                                                             boundary_type)
                    boundaries = string_t_a.count(BOUNDARY)
                    
                    # Test to see if it is a potential minimal width transp
                    if string_t_b[0] != BOUNDARY and string_t_b[-1] != BOUNDARY:
                        continue
                    
                    # If can be transposed
                    if string_t_a != string_t_b and \
                        string_t_a[::-1] == string_t_b:
                        transp = Transposition(pos_start,
                                               pos_end - 1,
                                               boundary_type,
                                               boundaries)
                        types_transposed.append(transp)
                
                # If found transpositions, add to the list
                for transposition in types_transposed:
                    overlap, boundaries = find_overlapping_transpositions(
                                                                transposition)
                    
                    if len(overlap) == 0:
                        set_transpositions.append(transposition)
                    else:
                        if transposition.boundaries > boundaries:
                            # Remove overlapping
                            for transp_overlap in overlap:
                                set_transpositions.remove(transp_overlap)
                            # Add new
                            set_transpositions.append(transposition)
                    
                i += 1
    
    # Discount substitutions by transpositions
    untransposted_set_errors = list()
    transposted_set_errors   = list()
    for set_error in set_errors:
        overlap = False
        for transposition in set_transpositions:
            if set_error.overlaps(transposition):
                overlap = True
                break
        if overlap == False:
            untransposted_set_errors.append(set_error)
        else:
            transposted_set_errors.append(set_error)
    
    # Calculate distance
    distance = len(untransposted_set_errors) + len(set_transpositions)
    
    return distance, set_transpositions, untransposted_set_errors
        

