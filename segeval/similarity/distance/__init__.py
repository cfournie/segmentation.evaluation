'''
Edit distance package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''


def identify_types(string_a, string_b):
    '''
    Construct a list of boundary types from two boundary strings.
    '''
    # Convert to strings and retrieve types
    boundary_types = set()
    for string in [string_a, string_b]:
        for position in string:
            for boundary_type in position:
                boundary_types.add(boundary_type)
    return frozenset(boundary_types)
