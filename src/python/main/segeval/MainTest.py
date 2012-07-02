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
    # pylint: disable=R0904,C0301
    
    test_data_dir = os.path.join(os.path.split(__file__)[0], 'data')
    
    print_output = True
    test_help    = False
    
    EXPECTED_FILE_STRINGS = [
'Pi*_s \n \t1+2+3+4+5+6+7\t= 0.7165532879818594104308390023',
'K*_s \n \t1+2+3+4+5+6+7\t= 0.7170345217883418222976796831',
'B_s \n \t1+2+3+4+5+6+7\t= 0.0014285714285714285714285714',
'F_1 \n \tmean\t= 0.5486480036131738918116627098\t(macro)\n\tstd\t= 0.1579255315223177090093893588\n\tvar\t= 0.0249404735066065643648383861\n\tstderr\t= 0.02497021901516212390630353805\t(n=40)',
'P \n \tmean\t= 0.569236111111111111111111111\t(macro)\n\tstd\t= 0.1958928076552311369113250286\n\tvar\t= 0.03837399209104938271604938268\n\tstderr\t= 0.03097337247178993532437300487\t(n=40)',
'R \n \tmean\t= 0.56812500000000000000000000\t(macro)\n\tstd\t= 0.1967217706661170373652606881\n\tvar\t= 0.03869945505401234567901234562\n\tstderr\t= 0.03110444303231145532699747260\t(n=40)',
'Pr \n \tmean\t= 0.3933140933140933140933140933\t(macro)\n\tstd\t= 0.1432599301657948205815072907\n\tvar\t= 0.02052340759110840880922651004\n\tstderr\t= 0.03126187971613534798006584564\t(n=21)',
'S \n \tmean\t= 0.7619047619047619047619047619\t(macro)\n\tstd\t= 0.07055015423823358837798727192\n\tvar\t= 0.004977324263038548752834467119\n\tstderr\t= 0.01539530581369118988034410932\t(n=21)',
'Pk \n \tmean\t= 0.3223684210526315789473684208\t(macro)\n\tstd\t= 0.08899835038466238748306496600\n\tvar\t= 0.007920706371191135734072022178\n\tstderr\t= 0.01407187476066278786833664467\t(n=40)',
'WindowDiff \n \tmean\t= 0.30375\t(macro)\n\tstd\t= 0.08615937267645348867219388312\n\tvar\t= 0.0074234375\n\tstderr\t= 0.01362299297144353664369233694\t(n=40)']

    EXPECTED_FOLDER_STRINGS = [
'Pi*_s \n \t1+2+3+4+5+6+7\t= 0.7165532879818594104308390023\n\tan1+an2+an3+an4\t= 1\n\tan5+an6\t= -0.5757942099675148626179719687',
'K*_s \n \t1+2+3+4+5+6+7\t= 0.7170345217883418222976796831\n\tan1+an2+an3+an4\t= 1\n\tan5+an6\t= -0.05952156715012243360331512524',
'B_s \n \t1+2+3+4+5+6+7\t= 0.0014285714285714285714285714\n\tan1+an2+an3+an4\t= 0.01455229356727327645713789012\n\tan5+an6\t= 0.3092215912041560442272265692',
'F_1 \n \tmean\t= 0.7286033348388224549215261291\t(macro)\n\tstd\t= 0.3239626640547745286898970139\n\tvar\t= 0.1049518077014667004704471820\n\tstderr\t= 0.03306430094362011655292214134\t(n=96)',
'P \n \tmean\t= 0.7371817129629629629629629628\t(macro)\n\tstd\t= 0.3279705495284159011523508245\n\tvar\t= 0.1075646813579711076817558297\n\tstderr\t= 0.03347335404186737660944801052\t(n=96)',
'R \n \tmean\t= 0.7367187499999999999999999999\t(macro)\n\tstd\t= 0.3284145188345961520541514860\n\tvar\t= 0.1078560961813593106995884774\n\tstderr\t= 0.03351866646943400531044047662\t(n=96)',
'Pr \n \tmean\t= 0.6583591012162440733869305296\t(macro)\n\tstd\t= 0.3625647993833832786266975493\n\tvar\t= 0.1314532337519129638574819243\n\tstderr\t= 0.0517949713404833255180996499\t(n=49)',
'S \n \tmean\t= 0.8163265306122448979591836735\t(macro)\n\tstd\t= 0.2726266332053075620573546388\n\tvar\t= 0.07432528113286130778842149114\n\tstderr\t= 0.03894666188647250886533637697\t(n=49)',
'Pk \n \tmean\t= 0.2176535087719298245614035085\t(macro)\n\tstd\t= 0.2873345796203152023025212293\n\tvar\t= 0.08256116064558325638658048630\n\tstderr\t= 0.02932596273028660385250146212\t(n=96)',
'WindowDiff \n \tmean\t= 0.2098958333333333333333333333\t(macro)\n\tstd\t= 0.2842772076969453810915086095\n\tvar\t= 0.08081353081597222222222222207\n\tstderr\t= 0.02901392101502961827511912967\t(n=96)']
    
    EXPECTED_OM_STRINGS = [
'1 - Pk \n \tmean\t= 0.6776315789473684210526315805\t(macro)\n\tstd\t= 0.08899835038466238748306496587\n\tvar\t= 0.007920706371191135734072022155\n\tstderr\t= 0.01407187476066278786833664465\t(n=40)',
'1 - WindowDiff \n \tmean\t= 0.69625\t(macro)\n\tstd\t= 0.08615937267645348867219388312\n\tvar\t= 0.0074234375\n\tstderr\t= 0.01362299297144353664369233694\t(n=40)']
    EXPECTED_WPR_STRINGS = [
'WinPR-f_1 \n \tmean\t= 0.6537078835417392808312562938\t(macro)\n\tstd\t= 0.1104334172259618258006709431\n\tvar\t= 0.01219553964020336212051245300\n\tstderr\t= 0.02409854731860048794927717470\t(n=21)',
'WinPR-p \n \tmean\t= 0.6700319521748093176664605238\t(macro)\n\tstd\t= 0.1469987063321598074606894023\n\tvar\t= 0.02160861966332855987419111370\n\tstderr\t= 0.03207774756322412707724005526\t(n=21)',
'WinPR-r \n \tmean\t= 0.6683725005153576582148010719\t(macro)\n\tstd\t= 0.1570297604076544084333187669\n\tvar\t= 0.02465834565368534800463416065\n\tstderr\t= 0.03426670302042171194576414586\t(n=21)']

    def test_load_files(self):
        '''
        Test the different ways to load files.
        '''
        metric = 'pi'
        result = 'Pi*_s \n \t1+2+3+4+5+6+7\t= 0.7165532879818594104308390023'
        argv = [metric, os.path.join(self.test_data_dir,
                                     'hearst1997.json')]
        self.assertEqual(result, main(argv))
        
        argv = [metric, '-f', 'json', os.path.join(self.test_data_dir,
                                                   'hearst1997.json')]
        self.assertEqual(result, main(argv))
        
        argv = [metric, '-f', 'tsv', os.path.join(self.test_data_dir,
                                                  'hearst1997.tsv')]
        self.assertEqual(result, main(argv))


    def test_all_but_winpr_folder(self):
        '''
        Run through each metric and load from a file.
        '''
        metrics = ['pi', 'k', 'b', 'f', 'p', 'r', 'pr', 's', 'pk', 'wd']
        for metric, expected in zip(metrics, self.EXPECTED_FOLDER_STRINGS):
            argv = [metric, os.path.abspath(os.path.join(self.test_data_dir,
                                                         '..'))]
            actual = main(argv)
            self.assertEqual(expected, actual)


    def test_all_but_winpr_metrics(self):
        '''
        Run through each metric and load from a file.
        '''
        metrics = ['pi', 'k', 'b', 'f', 'p', 'r', 'pr', 's', 'pk', 'wd']
        for metric, expected in zip(metrics, self.EXPECTED_FILE_STRINGS):
            argv = [metric, os.path.join(self.test_data_dir,
                                         'hearst1997.json')]
            actual = main(argv)
            self.assertEqual(expected, actual)


    def test_winpr_metrics(self):
        '''
        Run through each metric and load from a file.
        '''
        submetrics = ['f', 'p', 'r']
        for submetric, expected in zip(submetrics, self.EXPECTED_WPR_STRINGS):
            argv = ['wpr', submetric, os.path.join(self.test_data_dir,
                                                   'hearst1997.json')]
            actual = main(argv)
            self.assertEqual(expected, actual)


    def test_om_metrics(self):
        '''
        Run through each metric and load from a file.
        '''
        metrics = ['pk', 'wd']
        for metric, expected in zip(metrics, self.EXPECTED_OM_STRINGS):
            argv = [metric, '-om', os.path.join(self.test_data_dir,
                                         'hearst1997.json')]
            actual = main(argv)
            self.assertEqual(expected, actual)


    def test_file(self):
        '''
        Run through each metric and load from a file.
        '''
        metrics = ['pi', 'k', 'b', 'f', 'p', 'r', 'pr', 's', 'pk', 'wd']
        filesizes = [59, 58, 57, 1628, 1628, 1628, 806, 688, 1864, 815]
        for metric, expected_filesize in zip(metrics, filesizes):
            filename = 'testfile.tsv'
            if os.path.exists(filename):
                os.remove(filename)
            self.assertFalse(os.path.exists(filename))
            argv = [metric, '-o', filename, os.path.join(self.test_data_dir,
                                                         'hearst1997.json')]
            try:
                main(argv)
                self.assertTrue(os.path.exists(filename))
                actual_filesize = len(open(filename).read())
                self.assertEqual(expected_filesize, actual_filesize, 
                                 '%(metric)s %(expected)i != %(actual)i' % \
                                 {'metric'   : metric,
                                  'expected' : expected_filesize,
                                  'actual'   : actual_filesize})
            finally:
                if os.path.exists(filename):
                    os.remove(filename)
            
            self.assertFalse(os.path.exists(filename))


    def test_file_om(self):
        '''
        Run through each metric and load from a file.
        '''
        metrics = ['pk', 'wd']
        filesizes = [1868, 819]
        for metric, expected_filesize in zip(metrics, filesizes):
            filename = 'testfile.tsv'
            if os.path.exists(filename):
                os.remove(filename)
            self.assertFalse(os.path.exists(filename))
            argv = [metric, '-om', '-o', filename,
                    os.path.join(self.test_data_dir, 'hearst1997.json')]
            try:
                main(argv)
                self.assertTrue(os.path.exists(filename))
                actual_filesize = len(open(filename).read())
                self.assertEqual(expected_filesize, actual_filesize, 
                                 '%(metric)s %(expected)i != %(actual)i' % \
                                 {'metric'   : metric,
                                  'expected' : expected_filesize,
                                  'actual'   : actual_filesize})
            finally:
                if os.path.exists(filename):
                    os.remove(filename)
            
            self.assertFalse(os.path.exists(filename))


    def test_file_winpr(self):
        '''
        Run through each metric and load from a file.
        '''
        submetrics = ['f', 'p', 'r']
        filesizes = [1848, 1848, 1848]
        for submetric, expected_filesize in zip(submetrics, filesizes):
            
            filename = 'testfile.tsv'
            if os.path.exists(filename):
                os.remove(filename)
            self.assertFalse(os.path.exists(filename))
            argv = ['wpr', submetric, '-o', filename,
                    os.path.join(self.test_data_dir, 'hearst1997.json')]
            try:
                main(argv)
                self.assertTrue(os.path.exists(filename))
                actual_filesize = len(open(filename).read())
                self.assertEqual(expected_filesize, actual_filesize, 
                                 '%(metric)s %(expected)i != %(actual)i' % \
                                 {'metric'   : submetric,
                                  'expected' : expected_filesize,
                                  'actual'   : actual_filesize})
            finally:
                if os.path.exists(filename):
                    os.remove(filename)
            
            self.assertFalse(os.path.exists(filename))


    def test_file_s_detailed(self):
        '''
        Test detailed S output.
        '''
        expected_filesize = 2630
        filename = 'testfile.tsv'
        if os.path.exists(filename):
            os.remove(filename)
        self.assertFalse(os.path.exists(filename))
        argv = ['s', '-de', '-o', filename, os.path.join(self.test_data_dir,
                                                         'hearst1997.json')]
        try:
            main(argv)
            self.assertTrue(os.path.exists(filename))
            actual_filesize = len(open(filename).read())
            self.assertEqual(expected_filesize, actual_filesize, 
                             '%(metric)s %(expected)i != %(actual)i' % \
                             {'metric'   : 's',
                              'expected' : expected_filesize,
                              'actual'   : actual_filesize})
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

