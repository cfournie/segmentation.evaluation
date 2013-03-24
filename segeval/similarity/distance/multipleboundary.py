'''
Multiple-boundary edit distance.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import division
from itertools import permutations


# Addition/deletion tuple indices
A_TYPE = 0
A_SIDE = 1 # a = from a, b = from b

# Substitution tuple indices
S_TYPE1 = 0
S_TYPE2 = 1

# n-wise transposition tuple indices
T_POS1 = 0
T_POS2 = 1
T_TYPE = 2


def boundary_string_from_masses(segment_masses):
    '''
    Creates a "boundary string", or sequence of boundary type sets from a
    sequence of boundary masses.
    
    :param segment_masses: Segmentation masses.
    :type segment_masses:  list
    :returns: A sequence of boundary type sets
    :rtype: :func:`list` of :func:`set` objects containing :func:`int` values.
    '''
    string = [set() for _ in xrange(0, sum(segment_masses) + 1)]
    # Iterate over each position
    pos = 0
    for mass in segment_masses:
        string[pos].add(1)
        string[pos + mass].add(1)
        pos += mass
    # Return
    return [set(pb) for pb in string]


def __additions_substitutions__(d, a, b):
    '''
    Compute the number of additions and substitutions for a given pair of
    boundary string positions using:
    
    :param d: Symmetric difference between the pair.
    :param a: Difference between the pair; A / B.
    :param b: Difference between the pair; B / A.
    :type d: set
    :type a: set
    :type b: set
    '''
    # pylint: disable=C0103
    additions     = abs(len(a) - len(b))
    substitutions = (len(d) - additions) / 2
    return additions, substitutions


def __additions_substitutions_sets__(d, a, b):
    '''
    Compute the sets of additions and substitutions for a given pair of
    boundary string positions using:
    
    :param d: Symmetric difference between the pair.
    :param a: Difference between the pair; A / B.
    :param b: Difference between the pair; B / A.
    :type d: set
    :type a: set
    :type b: set
    '''
    # pylint: disable=C0103
    substitutions = list()
    delta = None
    for perm_a in permutations(sorted(a)):
        for perm_b in permutations(sorted(b)):
            current_substitutions = zip(perm_a, perm_b)
            current_substitutions = set(current_substitutions)
            current_delta = sum(abs(a_i - b_i) \
                                for a_i, b_i in current_substitutions)
            if delta is None or current_delta < delta:
                delta = current_delta
                substitutions = current_substitutions
    # Collect all substitutions
    substituted = list()
    added = list()
    for a_i, b_i in substitutions:
        substituted.append(a_i)
        substituted.append(b_i)
    additions = d - set(substituted)
    # Add from a
    for addition in a - set(substituted):
        added.append((addition, 'a'))
    # Add from b
    for addition in b - set(substituted):
        added.append((addition, 'b'))
    assert len(added) is len(additions)
    return added, set(substitutions)


def __has_substitutions__(i, j, d, options_set):
    '''
    Determine whether two substitutions are present involving the boundary 'd'
    at the positions 'i' and 'j'.
    '''
    # pylint: disable=C0103
    present = False
    if i in options_set and d in options_set[i][0] and \
       j in options_set and d in options_set[j][0]:
        d_i, a_i, b_i = options_set[i]
        d_j, a_j, b_j = options_set[j]
        if __additions_substitutions__(d_i, a_i, b_i)[1] > 0 and \
           __additions_substitutions__(d_j, a_j, b_j)[1] > 0:
            present = True
    return present
       
        
def __overlaps_existing__(i, j, d, options_transp):
    '''
    Determine whether a  transposition would overlap another that has been
    previously identified involving the boundary 'd' at the positions 'i' and
    'j'.
    '''
    # pylint: disable=C0103
    def check_position(position):
        '''
        Check a position for an overlapping transposition
        '''
        if position in options_transp:
            for t in options_transp[position]:
                # If the transposition 't' is of the boundary type 'd'
                if t[2] is d:
                    return True
    return check_position(i) or check_position(j)


def __transpositions__(boundary_string_a, boundary_string_b, n, options_set):
    '''
    Identify all non-overlapping minimal transpositions between two boundary
    strings while removing the additions/deletions and substitutions that they
    would overlap from the set of potential additions/deletions and
    substitutions.
    '''
    # pylint: disable=C0103,R0914
    options_transp = dict()
    transpositions = list()
    for n_i in sorted(n):
        n_i = n_i - 1
        for i in xrange(0, len(boundary_string_a) - n_i):
            j = i + n_i
            # Select edge sets
            a_i = boundary_string_a[i]
            a_j = boundary_string_a[j]
            b_i = boundary_string_b[i]
            b_j = boundary_string_b[j]
            # Compute symmetric differences
            diff_i = a_i ^ b_i
            diff_j = a_j ^ b_j
            diff_a = a_i ^ a_j
            diff_b = b_i ^ b_j
            # Detect potential transposition
            t_p = diff_i & diff_j & diff_a & diff_b
            # Apply each transposition found by boundary type
            for d in t_p:
                # Create transposition representation
                option_transp = (i, j, d)
                # Check to see that it does not overlap an existing 
                # transposition and that 2 substitutions are not removed
                if not __overlaps_existing__(i, j, d, options_transp) and \
                   not __has_substitutions__(i, j, d, options_set):
                    # Add
                    transpositions.append(option_transp)
                    # Record positions covered
                    if i not in options_transp:
                        options_transp[i] = list()
                    if j not in options_transp:
                        options_transp[j] = list()
                    options_transp[i].append(option_transp)
                    options_transp[j].append(option_transp)
                    # Removing potential set errors that overlap
                    options_set[i][0].discard(d)
                    options_set[i][1].discard(d)
                    options_set[i][2].discard(d)
                    options_set[j][0].discard(d)
                    options_set[j][1].discard(d)
                    options_set[j][2].discard(d)
    return transpositions


def __optional_set_edits__(boundary_string_a, boundary_string_b):
    '''
    Identify all potential additions/deletions and substitutions.
    '''
    # pylint: disable=C0103
    options_set = dict()
    for i, value in enumerate(zip(boundary_string_a, boundary_string_b)):
        a_i, b_i = value
        a = a_i - b_i
        b = b_i - a_i
        d = a_i ^ b_i
        # Record additions/deletions
        if len(d) > 0:
            options_set[i] = (d, a, b)
    return options_set


def __boundary_edit_distance__(boundary_string_a, boundary_string_b, n_t):
    '''
    Identify the minimum set of additions, substitutions, and transpositions
    that could be applied between two boundary strings for a given set
    of transpositions spanning lengths 'n_t'.
    
    :param t_n: transposition spanning sizes allowed
    :type t_n:  list or set
    
    '''
    # pylint: disable=C0103
    
    # Find potential addition/deletion/substitution operations
    options_set = __optional_set_edits__(boundary_string_a,
                                         boundary_string_b)
    # Find transpositions
    transpositions = __transpositions__(boundary_string_a,
                                        boundary_string_b, n_t, options_set)
    # Construct additions and substitions
    additions     = list()
    substitutions = list()
    for d, a, b in options_set.values():
        current_additions, current_substitutions = \
            __additions_substitutions_sets__(d, a, b)
        additions.extend(current_additions)
        substitutions.extend(current_substitutions)
    # Return
    return additions, substitutions, transpositions
    

def boundary_edit_distance(boundary_string_a, boundary_string_b, n_t=2):
    '''
    Convenience function to create spanning lengths given a maximum 'n_t'.
    '''
    # pylint: disable=C0103
    try:
        n_t = range(2, n_t + 1)
    except:
        pass
    return __boundary_edit_distance__(boundary_string_a, boundary_string_b, n_t)

