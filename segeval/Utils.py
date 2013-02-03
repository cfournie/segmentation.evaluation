'''
Utility functions and classes for the package.

.. codeauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2012, Chris Fournier
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
