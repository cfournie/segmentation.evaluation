'''
Created on May 12, 2013

@author: cfournie
'''

def enum(*sequential, **named):
    '''
    http://stackoverflow.com/a/1695250/2134
    '''
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)