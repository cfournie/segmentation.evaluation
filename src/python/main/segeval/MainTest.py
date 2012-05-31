'''
Tests for the console commands provided by __main__.py

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
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
from .__main__ import main


class TestMain(unittest.TestCase):
    '''
    Test command line functions.
    '''
    # pylint: disable=R0904
    
    test_data_dir = os.path.join(os.path.split(__file__)[0], 'data')
    
    print_output = True
    test_help    = False

    def test_load_files(self):
        '''
        Test the different ways to load files.
        '''
        metric = 'pi'
        argv = [metric, os.path.join(self.test_data_dir,
                                     'hearst1997.json')]
        self.assertEqual('Pi*_s = 0.7165532879818594104308390023', main(argv))
        
        argv = [metric, '-f', 'json', os.path.join(self.test_data_dir,
                                                   'hearst1997.json')]
        self.assertEqual('Pi*_s = 0.7165532879818594104308390023', main(argv))
        
        argv = [metric, '-f', 'tsv', os.path.join(self.test_data_dir,
                                                  'hearst1997.tsv')]
        self.assertEqual('Pi*_s = 0.7165532879818594104308390023', main(argv))


    def test_all_metrics(self):
        '''
        Run through each metric and load from a file.
        '''
        for metric in ['pi', 'k', 'b', 'f', 'p', 'r', 'pr', 's', 'pk', 'wd']:
            argv = [metric, os.path.join(self.test_data_dir,
                                         'hearst1997.json')]
            if self.print_output:
                print main(argv)


    def test_om_metrics(self):
        '''
        Run through each metric and load from a file.
        '''
        for metric in ['pk', 'wd']:
            argv = [metric, '-om', os.path.join(self.test_data_dir,
                                         'hearst1997.json')]
            if self.print_output:
                print main(argv)


    def test_help_output(self):
        '''
        Test the help output.
        '''
        argv = ['wd', '-h']
        if self.print_output and self.test_help:
            main(argv)

