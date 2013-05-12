'''
Created on Apr 13, 2013

@author: cfournie
'''
from collections import Counter


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