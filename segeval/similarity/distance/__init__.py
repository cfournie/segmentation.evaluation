'''
Edit distance package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''

def load_tests(loader, tests, pattern):
    '''
    A load_tests functions utilizing the default loader.
    '''
    #pylint: disable=W0613
    from ...Utils import default_load_tests
    return default_load_tests(__file__, loader, tests)
