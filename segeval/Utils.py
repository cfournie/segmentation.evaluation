'''
Utility functions and classes for the package.

.. codeauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import os
import unittest
from . import DECIMAL_PLACES


ROOT_PACKAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../'))


def default_load_tests(cur_file, loader, tests):
    '''
    Default functionality for module load_tests functions which 
    are contained in each module's __init__.py file)
    
    :param cur_file: __file__ from the calling module.
    :param loader: Test loader.
    :param tests: Test suite.
    :type cur_file: str
    :type loader: str
    :type tests: unittest.TestSuite
    
    :returns: A modified test suite.
    :rtype: :class:`unittest.TestSuite`
    
    .. seealso:: The `load_tests protocol <http://docs.python.org/library/\
    unittest.html#load-tests-protocol>`_.
    '''
    pattern = '*Test.py'
    cur_dir = os.path.split(cur_file)[0]
    discovered_tests = loader.discover(cur_dir,
                                       pattern=pattern,
                                       top_level_dir=ROOT_PACKAGE_DIR)
    tests.addTests(discovered_tests)
    return tests


class AlmostTestCase(unittest.TestCase):
    '''
    Provides helper functions for validating segmentation.
    '''
    # pylint: disable=R0904
    
    SKIP = False
    
    def assertAlmostEquals(self, first, second, places=DECIMAL_PLACES,
                           msg=None, delta=None):
        '''
        Automatically converts values to floats.
        '''
        # pylint: disable=C0103,R0913
        if isinstance(first, dict):
            for item in first.keys():
                try:
                    self.assertAlmostEquals(first[item], second[item], places,
                                            msg, delta)
                except Exception as e:
                    print first
                    print second
                    raise e
        elif isinstance(first, list) or isinstance(first, tuple):
            for item in zip(first, second):
                try:
                    self.assertAlmostEquals(item[0], item[1], places, msg,
                                            delta)
                except Exception as e:
                    print first
                    print second
                    raise e
        else:
            return unittest.TestCase.assertAlmostEquals(self,
                                                        float(first),
                                                        float(second),
                                                        places=places,
                                                        msg=msg,
                                                        delta=delta)
