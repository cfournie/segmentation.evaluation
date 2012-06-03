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
    
    EXPECTED_FILE_STRINGS = [
'Pi*_s = 0.7165532879818594104308390023',
'K*_s = 0.7170345217883418222976796831',
'B_s = 0.0014285714285714285714285714',
'F_1.0 \n \tmean\t= 0.5488257630783062008183635781\n\tstd\t= 0.1541776268839723\
153329934674\n\tvar\t= 0.02377074063157338283693571884\n\tstderr\t= 0.023790124\
31740241024748814012',
'P \n \tmean\t= 0.5705026455026455026455026452\n\tstd\t= 0.19133276680485545671\
50062579\n\tvar\t= 0.03660822765320119817474314828\n\tstderr\t= 0.0417522327051\
7067477184376665',
'R \n \tmean\t= 0.5708994708994708994708994710\n\tstd\t= 0.2009486961610950520518783548\n\tvar\t= 0.04038037848884409730970577530\n\tstderr\t= 0.04385060052194762366757538877',
'Pr \n \tmean\t= 0.3933140933140933140933140933\n\tstd\t= 0.1432599301657948205815072906\n\tvar\t= 0.02052340759110840880922651003\n\tstderr\t= 0.03126187971613534798006584562',
'S \n \tmean\t= 0.7619047619047619047619047619\n\tstd\t= 0.07055015423823358837798727192\n\tvar\t= 0.004977324263038548752834467119\n\tstderr\t= 0.01539530581369118988034410932',
'Pk \n \tmean\t= 0.3258145363408521303258145360\n\tstd\t= 0.08839695282480399887931269980\n\tvar\t= 0.007814021268710623676986953602\n\tstderr\t= 0.01363994594730826050014572596',
'WindowDiff \n \tmean\t= 0.3047619047619047619047619048\n\tstd\t= 0.08438116736509214477138630999\n\tvar\t= 0.007120181405895691609977324264\n\tstderr\t= 0.01302029679814566213216037145']
    
    EXPECTED_FOLDER_STRINGS = [
'Mean Pi*_s \n \tmean\t= 0.7165532879818594104308390023\n\tstd\t= 0\n\tvar\t= 0\
\n\tstderr\t= 0',
'Mean K*_s \n \tmean\t= 0.7170345217883418222976796831\n\tstd\t= 0\n\tvar\t= 0\
\n\tstderr\t= 0',
'Mean B_s \n \tmean\t= 0.0014285714285714285714285714\n\tstd\t= 0\n\tvar\t= 0\
\n\tstderr\t= 0',
'F_1.0 \n \tmean\t= 0.5488257630783062008183635781\n\tstd\t= 0.1541776268839723\
153329934674\n\tvar\t= 0.02377074063157338283693571884\n\tstderr\t= 0.023790124\
31740241024748814012',
'P \n \tmean\t= 0.5705026455026455026455026452\n\tstd\t= 0.19133276680485545671\
50062579\n\tvar\t= 0.03660822765320119817474314828\n\tstderr\t= 0.0417522327051\
7067477184376665',
'R \n \tmean\t= 0.5708994708994708994708994710\n\tstd\t= 0.2009486961610950520518783548\n\tvar\t= 0.04038037848884409730970577530\n\tstderr\t= 0.04385060052194762366757538877',
'Pr \n \tmean\t= 0.3933140933140933140933140933\n\tstd\t= 0.1432599301657948205815072906\n\tvar\t= 0.02052340759110840880922651003\n\tstderr\t= 0.03126187971613534798006584562',
'S \n \tmean\t= 0.7619047619047619047619047619\n\tstd\t= 0.07055015423823358837798727192\n\tvar\t= 0.004977324263038548752834467119\n\tstderr\t= 0.01539530581369118988034410932',
'Pk \n \tmean\t= 0.3258145363408521303258145360\n\tstd\t= 0.08839695282480399887931269980\n\tvar\t= 0.007814021268710623676986953602\n\tstderr\t= 0.01363994594730826050014572596',
'WindowDiff \n \tmean\t= 0.3047619047619047619047619048\n\tstd\t= 0.08438116736509214477138630999\n\tvar\t= 0.007120181405895691609977324264\n\tstderr\t= 0.01302029679814566213216037145']
    
    EXPECTED_OM_STRINGS = [
'1 - Pk \n \tmean\t= 0.6741854636591478696741854652\n\tstd\t= 0.088396952824803\
99887931269979\n\tvar\t= 0.0078140212687106236769869536\n\tstderr\t= 0.01363994\
594730826050014572596',
'1 - WindowDiff \n \tmean\t= 0.6952380952380952380952380952\n\tstd\t= 0.0843811\
6736509214477138630999\n\tvar\t= 0.007120181405895691609977324264\n\tstderr\t= \
0.01302029679814566213216037145']
    
    EXPECTED_WPR_STRINGS = [
'WinPR-f \n \tmean\t= 0.6537078835417392808312562943\n\tstd\t= 0.11043341722596\
18258006709431\n\tvar\t= 0.0121955396402033621205124530\n\tstderr\t= 0.02409854\
731860048794927717470',
'WinPR-p \n \tmean\t= 0.6700319521748093176664605229\n\tstd\t= 0.14699870633215\
98074606894023\n\tvar\t= 0.02160861966332855987419111370\n\tstderr\t= 0.0320777\
4756322412707724005526',
'WinPR-r \n \tmean\t= 0.6683725005153576582148010719\n\tstd\t= 0.15702976040765\
44084333187669\n\tvar\t= 0.02465834565368534800463416065\n\tstderr\t= 0.0342667\
0302042171194576414586']

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


    def test_all_but_winpr_folder(self):
        '''
        Run through each metric and load from a file.
        '''
        metrics = ['pi', 'k', 'b', 'f', 'p', 'r', 'pr', 's', 'pk', 'wd']
        for metric, output in zip(metrics, self.EXPECTED_FOLDER_STRINGS):
            argv = [metric, os.path.join(self.test_data_dir,
                                         '..')]
            self.assertEqual(main(argv), output)


    def test_all_but_winpr_metrics(self):
        '''
        Run through each metric and load from a file.
        '''
        metrics = ['pi', 'k', 'b', 'f', 'p', 'r', 'pr', 's', 'pk', 'wd']
        for metric, output in zip(metrics, self.EXPECTED_FILE_STRINGS):
            argv = [metric, os.path.join(self.test_data_dir,
                                         'hearst1997.json')]
            self.assertEqual(output, main(argv))


    def test_winpr_metrics(self):
        '''
        Run through each metric and load from a file.
        '''
        submetrics = ['f', 'p', 'r']
        for submetric, output in zip(submetrics, self.EXPECTED_WPR_STRINGS):
            argv = ['wpr', submetric, os.path.join(self.test_data_dir,
                                                   'hearst1997.json')]
            self.assertEqual(output, main(argv))


    def test_om_metrics(self):
        '''
        Run through each metric and load from a file.
        '''
        metrics = ['pk', 'wd']
        for metric, output in zip(metrics, self.EXPECTED_OM_STRINGS):
            argv = [metric, '-om', os.path.join(self.test_data_dir,
                                         'hearst1997.json')]
            self.assertEqual(output, main(argv))


    def test_file(self):
        '''
        Run through each metric and load from a file.
        '''
        metrics = ['b']
        filesizes = [50]
        for metric, filesize in zip(metrics, filesizes):
            filename = 'testfile.tsv'
            if os.path.exists(filename):
                os.remove(filename)
            self.assertFalse(os.path.exists(filename))
            argv = [metric, '-o', filename, os.path.join(self.test_data_dir,
                                                         'hearst1997.json')]
            try:
                main(argv)
                self.assertTrue(os.path.exists(filename))
                self.assertEqual(filesize, len(open(filename).read()))
            finally:
                if os.path.exists(filename):
                    os.remove(filename)
            
            self.assertFalse(os.path.exists(filename))         


    def test_help_output(self):
        '''
        Test the help output.
        '''
        argv = ['wd', '-h']
        if self.print_output and self.test_help:
            main(argv)

