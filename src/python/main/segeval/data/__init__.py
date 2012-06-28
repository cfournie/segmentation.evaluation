'''
Data I/O package.  Used to import and export data to and from TSV and JSON
files.

.. seealso:: File format documentation in: `Segmentation Representation \
Specification <http://nlp.chrisfournier.ca/publications/#seg_spec>`_.

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
import csv
import json
from .TSV import input_linear_mass_tsv
from .JSON import input_linear_mass_json


RESULTS = ['summary', 'tsv']


def load_tests(loader, tests, pattern):
    '''
    A ``load_tests()`` function utilizing the default loader
    :func:`segeval.Utils.default_load_tests`.
    
    .. seealso:: The `load_tests protocol <http://docs.python.org/library/\
    unittest.html#load-tests-protocol>`_.
    '''
    #pylint: disable=W0613
    from ..Utils import default_load_tests
    return default_load_tests(__file__, loader, tests)


def name_from_filepath(filepath):
    '''
    Creates a default coder name from a filename.
    '''
    name = os.path.split(filepath)[1]
    name_basic = os.path.splitext(name)[0]
    name = name_basic if len(name_basic) > 0 else name
    return name


class DataIOError(Exception):
    '''
    Indicates that an input processing error has occurred.
    '''
    
    def __init__(self, message, exception):
        '''
        Initializer.
        
        :param message: Explanation for the exception.
        :type message: str
        '''
        Exception.__init__(self, message, exception)


FILETYPE_TSV  = 'tsv'
FILETYPE_JSON = 'json'

EXT = 'ext'
FNC = 'fnc'
FILETYPES           = {FILETYPE_TSV  : {EXT : ['.tsv', '.csv'],
                                        FNC : input_linear_mass_tsv},
                       FILETYPE_JSON : {EXT : ['.json', '.jsn'],
                                        FNC : input_linear_mass_json}}
FILETYPES_DEFAULT   = FILETYPE_JSON


def load_nested_folders_dict(containing_dir, filetype):
    '''
    Loads TSV files from a file directory structure, which reflects the
    directory structure in nested :func:`dict` with each directory name
    representing a key in these :func:`dict`.
    
    :param containing_dir: Root directory containing sub-directories which 
                           contain segmentation files.
    :param filetype:       File type to load (e.g., json or tsv).
    :type containing_dir: str
    :type filetype: str
    
    :returns: Segmentation mass codings.
    :rtype: :func:`dict`
    '''
    allowable_extensions = list(FILETYPES[filetype][EXT])
    fnc_load = FILETYPES[filetype][FNC]
    data = dict()
    datafile_found = False
    # List of entries
    files = dict()
    dirs = dict()
    # For each filesystem item
    for name in os.listdir(containing_dir):
        path = os.path.join(containing_dir, name)
        # Found a directory
        if os.path.isdir(path):
            dirs[name] = path
        # Found a file
        elif os.path.isfile(path):
            name, ext = os.path.splitext(name)
            if len(ext) > 0 and ext.lower() in allowable_extensions:
                files[name] = path
                datafile_found = True
    # If a data file was found
    if datafile_found:
        # If TSV files were found, load
        for name, filepath in files.items():
            data[name] = fnc_load(filepath)
    else:
        # If only dirs were found, recurse
        for name, dirpath in dirs.items():
            data[name] = load_nested_folders_dict(dirpath, filetype)
    return data


def load_file(args):
    '''
    Load a file or set of directories from command line arguments.
    
    :param args: Command line arguments
    :type args: dict
    
    :returns: The loaded values and whether a file was loaded or not.
    :rtype: :func:`dict`, :func:`bool`
    '''
    values = None
    
    input_path = args['input'][0]
    is_file = os.path.isfile(input_path)
    
    filetype = args['format']
    
    # Load file or dir
    if is_file:
        values = FILETYPES[filetype][FNC](input_path)
        values = {'item' : values}
    else:
        values = load_nested_folders_dict(input_path, filetype)
    
    return values, is_file


def parser_add_file_support(parser):
    '''
    Add support for file input and output parameters to an argument parser.
    
    :param parser: Argument parser
    :type parser: argparse.ArgumentParser
    '''
    
    parser.add_argument('-o', '--output',
                        type=str,
                        nargs=1,
                        required=False,
                        help='Output file or directory. If not specified, a '+\
                        'summary or results is printed to the console.')
    
    parser.add_argument('input',
                        type=str,
                        nargs=1,
                        action='store',
                        help='Input file or directory')
    
    parser.add_argument('-f', '--format',
                        type=str,
                        default=FILETYPES_DEFAULT,
                        choices=FILETYPES.keys(),
                        help='Input file format; default is %s' % \
                            FILETYPES_DEFAULT)
    
    parser.add_argument('-d', '--delimiter',
                        type=str,
                        default='\t',
                        help='Delimiting character for input TSV files; '+\
                        'ignored if JSON is specified, default is a tab '+\
                        'character')

