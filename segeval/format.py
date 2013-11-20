'''
Segmentation encoding format converstion utilities.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
from itertools import groupby
from segeval.util.lang import enum


BoundaryFormat = enum(position='position', mass='mass', sets='sets', nltk='nltk')


def convert_positions_to_masses(positions):
    '''
    Convert an ordered sequence of boundary position labels into a
    sequence of segment masses, e.g., ``[1,1,1,1,1,2,2,2,3,3,3,3,3]`` becomes
    ``[5,3,5]``.

    :param segments: Ordered sequence of which segments a unit belongs to.
    :type segments: tuple

    .. deprecated:: 1.0
    '''
    return tuple([len(list(group)) for _, group in groupby(positions)])


def convert_masses_to_positions(masses):
    '''
    Converts a sequence of segment masses into an ordered sequence of section
    labels for each unit, e.g., ``[5,3,5]`` becomes
    ``[1,1,1,1,1,2,2,2,3,3,3,3,3]``.

    :param masses: Segment mass sequence.
    :type masses: tuple
    '''
    sequence = list()
    for i, mass in enumerate(masses):
        sequence.extend([i + 1] * mass)
    return tuple(sequence)


def boundary_string_from_masses(masses):
    '''
    Creates a "boundary string", or sequence of boundary type sets from a list of segment masses, e.g., ``[5,3,5]`` becomes
    ``[(),(),(),(),(1),(),(),(1),(),(),(),()]``.


    :param masses: Segmentation masses.
    :type masses: tuple
    '''
    string = [set() for _ in range(0, sum(masses) - 1)]
    # Iterate over each position
    pos = 0
    for mass in masses:
        cur_pos = pos + mass - 1
        if cur_pos < len(string):
            string[cur_pos].add(1)
        pos += mass
    # Return
    return tuple([frozenset(pb) for pb in string])


def convert_nltk_to_masses(string, boundary_symbol='1'):
    '''
    Convert an `NLTK <http://nltk.org/>`_-formatted segmentation into masses, e.g., ``000001000100000`` becomes
    ``[5,3,5]``.

    For more information, see `nltk.metrics.segmentation <http://nltk.org/api/nltk.metrics.html#module-nltk.metrics.segmentation>`_.

    :param string: NLTK-formatted segmentation.
    :type string: str
    :param boundary_symbol: String that represents a boundary.
    :type boundary_symbol: str
    '''
    masses = [len(segment) + 1 for segment in string.split(boundary_symbol)]
    return tuple(masses)
