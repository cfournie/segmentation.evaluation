'''
Test data for unit tests that has been selected from
(KazantsevaSzpakowicz2012)_, (Hearst1997)_, or contrived.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
from segeval.data import Dataset
from segeval.format import BoundaryFormat


KAZANTSEVA2012_G5 = Dataset(
    {'ch1': {'an4': (2, 8, 2, 1),
             'an1': (11, 2),
             'an2': (2, 1, 7, 2, 1),
             'an3': (9, 4)},
     'ch11':{'an4': (10, 4, 3, 2, 1, 8, 3, 2, 6, 1, 2, 8, 10, 9, 4, 10, 4,
                     8, 4, 3, 5, 4),
             'an1': (20, 22, 8, 11, 11, 11, 13, 11, 4),
             'an2': (1, 7, 2, 4, 3, 3, 10, 1, 1, 5, 3, 2, 8, 3, 3, 3, 14,
                     4, 1, 1, 4, 4, 2, 7, 3, 2, 3, 3, 2, 1, 1),
             'an3': (10, 10, 15, 11, 4, 10, 13, 5, 4, 23, 6)},
     'ch4': {'an4': (2, 9, 2, 5, 2, 19, 1, 6),
             'an1': (17, 25, 4),
             'an2': (1, 10, 2, 4, 1, 2, 3, 10, 6, 6, 1),
             'an3': (12, 5, 29)},
     'ch3': {'an4': (2, 3, 4, 2, 5, 17, 4, 1),
             'an1': (6, 5, 27),
             'an2': (3, 8, 2, 3, 17, 2, 2, 1),
             'an3': (3, 15, 15, 5)}})
'''
Segmentations provided by 4 coders (labeled group 5) of 4 chapters of
"The Moonstone" (Collins1868)_ collected by (KazantsevaSzpakowicz2012)_::

    KAZANTSEVA2012_G5 = Dataset(
        {'ch1': {'an4': (2, 8, 2, 1),
                 'an1': (11, 2),
                 'an2': (2, 1, 7, 2, 1),
                 'an3': (9, 4)},
         'ch11':{'an4': (10, 4, 3, 2, 1, 8, 3, 2, 6, 1, 2, 8, 10, 9, 4, 10, 4,
                          8, 4, 3, 5, 4),
                 'an1': (20, 22, 8, 11, 11, 11, 13, 11, 4),
                 'an2': (1, 7, 2, 4, 3, 3, 10, 1, 1, 5, 3, 2, 8, 3, 3, 3, 14,
                          4, 1, 1, 4, 4, 2, 7, 3, 2, 3, 3, 2, 1, 1),
                 'an3': (10, 10, 15, 11, 4, 10, 13, 5, 4, 23, 6)},
         'ch4': {'an4': (2, 9, 2, 5, 2, 19, 1, 6),
                 'an1': (17, 25, 4),
                 'an2': (1, 10, 2, 4, 1, 2, 3, 10, 6, 6, 1),
                 'an3': (12, 5, 29)},
         'ch3': {'an4': (2, 3, 4, 2, 5, 17, 4, 1),
                 'an1': (6, 5, 27),
                 'an2': (3, 8, 2, 3, 17, 2, 2, 1),
                 'an3': (3, 15, 15, 5)}})
'''


KAZANTSEVA2012_G2 = Dataset(
    {'ch8': {'an5':  (9, 7, 5, 12, 4, 2),
             'an6':  (3, 5, 4, 3, 6, 7, 5, 4, 2),
             'an7':  (2, 6, 2, 2, 2, 8, 8, 3, 4, 1, 1),
             'an10': (2, 6, 4, 3, 6, 7, 5, 4, 1, 1),
             'an8':  (8, 4, 21, 4, 2),
             'an9':  (3, 5, 4, 10, 9, 6, 2)},
     'ch10':{'an5':  (24, 6, 45, 6, 2),
             'an6':  (3, 3, 2, 3, 8, 1, 4, 6, 11, 22, 10, 6, 4),
             'an7':  (3, 3, 2, 16, 6, 45, 4, 1, 1, 1, 1),
             'an10': (3, 5, 16, 5, 8, 2, 23, 13, 4, 4),
             'an8':  (8, 16, 6, 32, 11, 6, 1, 3),
             'an9':  (3, 3, 2, 11, 5, 6, 45, 4, 4)},
     'ch2': {'an5':  (4, 7, 3, 1),
             'an6':  (4, 7, 3, 1),
             'an7':  (5, 6, 3, 1),
             'an10': (5, 5, 4, 1),
             'an8':  (14, 1),
             'an9':  (14, 1)},
     'ch5': {'an5':  (9, 4, 5, 9, 8, 7),
             'an6':  (2, 1, 6, 3, 2, 4, 17, 7),
             'an7':  (19, 15, 8),
             'an10': (4, 10, 5, 1, 14, 4, 4),
             'an8':  (9, 4, 6, 16, 3, 4),
             'an9':  (13, 6, 15, 8)}})
'''
Segmentations provided by 6 coders (labeled group 2) of 4 chapters of
"The Moonstone" (Collins1868)_ collected by (KazantsevaSzpakowicz2012)_::

    KAZANTSEVA2012_G2 = Dataset(
        {'ch8': {'an5':  (9, 7, 5, 12, 4, 2),
             'an6':  (3, 5, 4, 3, 6, 7, 5, 4, 2),
             'an7':  (2, 6, 2, 2, 2, 8, 8, 3, 4, 1, 1),
             'an10': (2, 6, 4, 3, 6, 7, 5, 4, 1, 1),
             'an8':  (8, 4, 21, 4, 2),
             'an9':  (3, 5, 4, 10, 9, 6, 2)},
     'ch10':{'an5':  (24, 6, 45, 6, 2),
             'an6':  (3, 3, 2, 3, 8, 1, 4, 6, 11, 22, 10, 6, 4),
             'an7':  (3, 3, 2, 16, 6, 45, 4, 1, 1, 1, 1),
             'an10': (3, 5, 16, 5, 8, 2, 23, 13, 4, 4),
             'an8':  (8, 16, 6, 32, 11, 6, 1, 3),
             'an9':  (3, 3, 2, 11, 5, 6, 45, 4, 4)},
     'ch2': {'an5':  (4, 7, 3, 1),
             'an6':  (4, 7, 3, 1),
             'an7':  (5, 6, 3, 1),
             'an10': (5, 5, 4, 1),
             'an8':  (14, 1),
             'an9':  (14, 1)},
     'ch5': {'an5':  (9, 4, 5, 9, 8, 7),
             'an6':  (2, 1, 6, 3, 2, 4, 17, 7),
             'an7':  (19, 15, 8),
             'an10': (4, 10, 5, 1, 14, 4, 4),
             'an8':  (9, 4, 6, 16, 3, 4),
             'an9':  (13, 6, 15, 8)}})
'''

HEARST_1997_STARGAZER = Dataset(
    {'stargazer':
        {'1': (2,3,3,1,3,6,3),
         '2': (2,8,2,4,2,3),
         '3': (2,1,2,3,1,3,1,3,2,2,1),
         '4': (2,1,4,1,1,3,1,4,3,1),
         '5': (3,2,4,3,5,4),
         '6': (2,3,4,2,2,5,3),
         '7': (2,3,2,2,3,1,3,2,3)}
     })
'''
Segmentations provided by 7 coders of a magazine article titled
"Stargazers look for life" (Baker1990)_ collected by (Hearst1997)_::

    HEARST_1997_STARGAZER = \
        {'1' : (2,3,3,1,3,6,3),
         '2' : (2,8,2,4,2,3),
         '3' : (2,1,2,3,1,3,1,3,2,2,1),
         '4' : (2,1,4,1,1,3,1,4,3,1),
         '5' : (3,2,4,3,5,4),
         '6' : (2,3,4,2,2,5,3),
         '7' : (2,3,2,2,3,1,3,2,3)}
'''

HYPOTHESIS_STARGAZER = Dataset(
    {'stargazer':
        {'h1': (2,6,4,2,4,3),
         'h2': (2,1,1,1,5,8,2,1)}
     })
'''
Segmentations provided by 7 coders of a magazine article titled
"Stargazers look for life" (Baker1990)_ collected by (Hearst1997)_::

    HEARST_1997_STARGAZER = \
        {'1' : (2,3,3,1,3,6,3),
         '2' : (2,8,2,4,2,3),
         '3' : (2,1,2,3,1,3,1,3,2,2,1),
         '4' : (2,1,4,1,1,3,1,4,3,1),
         '5' : (3,2,4,3,5,4),
         '6' : (2,3,4,2,2,5,3),
         '7' : (2,3,2,2,3,1,3,2,3)}
'''


COMPLETE_AGREEMENT = Dataset(
    {'item1': {'an4': (2, 8, 2, 1),
               'an1': (2, 8, 2, 1),
               'an2': (2, 8, 2, 1),
               'an3': (2, 8, 2, 1)},
     'item2': {'an4': (20, 22, 8, 11, 11, 11, 13, 11, 4),
               'an1': (20, 22, 8, 11, 11, 11, 13, 11, 4),
               'an2': (20, 22, 8, 11, 11, 11, 13, 11, 4),
               'an3': (20, 22, 8, 11, 11, 11, 13, 11, 4)},
     'item3': {'an4': (2, 9, 2, 5, 2, 19, 1, 6),
               'an1': (2, 9, 2, 5, 2, 19, 1, 6),
               'an2': (2, 9, 2, 5, 2, 19, 1, 6),
               'an3': (2, 9, 2, 5, 2, 19, 1, 6)},
     'item4': {'an4': (6, 5, 27),
               'an1': (6, 5, 27),
               'an2': (6, 5, 27),
               'an3': (6, 5, 27)}})
'''
Contrived segmentations created by Chris Fournier to demonstrate complete
agreement, but varying item sizes::

    COMPLETE_AGREEMENT = Dataset(
        {'item1': {'an4': (2, 8, 2, 1),
                   'an1': (2, 8, 2, 1),
                   'an2': (2, 8, 2, 1),
                   'an3': (2, 8, 2, 1)},
         'item2': {'an4': (20, 22, 8, 11, 11, 11, 13, 11, 4),
                   'an1': (20, 22, 8, 11, 11, 11, 13, 11, 4),
                   'an2': (20, 22, 8, 11, 11, 11, 13, 11, 4),
                   'an3': (20, 22, 8, 11, 11, 11, 13, 11, 4)},
         'item3': {'an4': (2, 9, 2, 5, 2, 19, 1, 6),
                   'an1': (2, 9, 2, 5, 2, 19, 1, 6),
                   'an2': (2, 9, 2, 5, 2, 19, 1, 6),
                   'an3': (2, 9, 2, 5, 2, 19, 1, 6)},
         'item4': {'an4': (6, 5, 27),
                   'an1': (6, 5, 27),
                   'an2': (6, 5, 27),
                   'an3': (6, 5, 27)}})
'''

LARGE_DISAGREEMENT = Dataset(
    {'item1': {'an5': (12,),
               'an6': (1,) * 12},
     'item2': {'an5': (20,),
               'an6': (1,) * 20},
     'item3': {'an5': (5,),
               'an6': (1,) * 5},
     'item4': {'an5': (42,),
               'an6': (1,) * 42}})
'''
Contrived segmentations created by Chris Fournier to demonstrate large
disagreement, but varying item sizes::

    LARGE_DISAGREEMENT = Dataset(
        {'item1': {'an4': (12),
                   'an1': (1) * 12},
         'item2': {'an4': (20),
                   'an1': (1) * 20},
         'item3': {'an4': (5),
                   'an1': (1) * 5},
         'item4': {'an4': (42),
                   'an1': (1) * 42}})
'''

MULTIPLE_BOUNDARY_TYPES = Dataset(
    {'item1': {'an5': (frozenset([1]), frozenset(), frozenset(), frozenset(),
                       frozenset([1])),
               'an6': (frozenset([1]), frozenset(), frozenset(), frozenset(),
                       frozenset([2]))},
     'item2': {'an5': (frozenset([1]), frozenset(), frozenset(), frozenset(),
                       frozenset([1])),
               'an6': (frozenset(), frozenset(), frozenset(), frozenset([1]),
                       frozenset())}},
    boundary_types=frozenset([1, 2]),
    boundary_format=BoundaryFormat.sets)
'''
Contrived segmentations created by Chris Fournier to demonstrate large
disagreement, but varying item sizes::

    MULTIPLE_BOUNDARY_TYPES = Dataset(
        {'item1': {'an4': (12),
                   'an1': (1) * 12},
         'item2': {'an4': (20),
                   'an1': (1) * 20},
         'item3': {'an4': (5),
                   'an1': (1) * 5},
         'item4': {'an4': (42),
                   'an1': (1) * 42}})
'''
