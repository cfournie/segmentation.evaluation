'''
Python-language utils.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''


def enum(*sequential, **named):
    '''
    http://stackoverflow.com/a/1695250/2134
    '''
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
