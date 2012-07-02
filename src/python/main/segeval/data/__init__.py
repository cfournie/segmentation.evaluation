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


FIELD_SINGLE_FILE = 'single_file'


class Dataset(dict):
    '''
    Represents a set of segmentations produced by coders.
    '''
    # pylint: disable=R0903
    
    def __init__(self, masses=None, properties=None):
        '''
        Initialize.
        '''
        dict.__init__(self)
        # Masses
        if masses is not None:
            self.update(masses)
        # Properties
        if properties is not None:
            self.properties = dict()
            self.properties.update(properties)
        else:
            self.properties = dict()
        # Coders
        self.coders = set()
        # Populate coders
        for coder_masses in self.values():
            for coder in coder_masses.keys():
                self.coders.add(coder)
        
    def add(self, other, prepend_item=None):
        '''
        Add one dataset's data to this dataset
        '''
        # Combine item codings
        for item, codings in other.items():
            if prepend_item is not None:
                item_parts = list()
                item_parts.extend(prepend_item)
                item_parts.append(item)
                item = ','.join(item_parts)
            if item not in self:
                self[item] = dict()
            # For each coder, add ttheir coding
            for coder, item_masses in codings.items():
                self.coders.add(coder)
                if coder not in self[item]:
                    self[item][coder] = item_masses
                else:
                    raise DataIOError('Duplicate coders of same name \
%(coder)s found for item %(item)s' % {'coder' : coder, 'item' : item})


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
    
    def __init__(self, message, exception=None):
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


def load_nested_folders_dict(containing_dir, filetype, dataset=None,
                             prepend_item=list()):
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
    # pylint: disable=R0914
    # Create empty dataset
    if dataset is None:
        dataset = Dataset()
    # Vars
    allowable_extensions = list(FILETYPES[filetype][EXT])
    fnc_load = FILETYPES[filetype][FNC]
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
            other = fnc_load(filepath)
            dataset.add(other, prepend_item=prepend_item)
    # If only dirs were found, recurse
    for name, dirpath in dirs.items():
        new_prepend_item = list(prepend_item)
        new_prepend_item.append(name)
        # Recurse
        load_nested_folders_dict(dirpath,
                                 filetype,
                                 dataset=dataset,
                                 prepend_item=new_prepend_item)
    return dataset


def load_file(args):
    '''
    Load a file or set of directories from command line arguments.
    
    :param args: Command line arguments
    :type args: dict
    
    :returns: The loaded values and whether a file was loaded or not.
    :rtype: :func:`dict`, :func:`bool`
    '''
    input_path = args['input'][0]
    filetype = args['format']
    return __load_file__(input_path, filetype)
    
    
def __load_file__(input_path, filetype):
    dataset = None
    
    is_file = os.path.isfile(input_path)
    
    # Load file or dir
    if is_file:
        dataset = FILETYPES[filetype][FNC](input_path)
        dataset.properties[FIELD_SINGLE_FILE] = True
    else:
        dataset = load_nested_folders_dict(input_path, filetype,
                                           dataset=Dataset())
        dataset.properties[FIELD_SINGLE_FILE] = False
    
    return dataset


def load_files(args):
    '''
    Load a file or set of directories from command line arguments.
    
    :param args: Command line arguments
    :type args: dict
    
    :returns: The loaded values and whether a file was loaded or not.
    :rtype: :func:`dict`, :func:`bool`
    '''
    datasets = list()
    # Parse args
    filetype = args['format']
    input_paths = args['input']
    # For each path
    for input_path in input_paths:
        # Read
        dataset = __load_file__(input_path, filetype)
        #add
        datasets.append(dataset)
    # Return
    return datasets


def parser_add_format_support(parser):
    '''
    Add support for file input format and output parameters to an argument parser.
    
    :param parser: Argument parser
    :type parser: argparse.ArgumentParser
    '''
    
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
    
    parser.add_argument('-o', '--output',
                        type=str,
                        nargs=1,
                        required=False,
                        help='Output file or directory. If not specified, a '+\
                        'summary or results is printed to the console.')


def parser_add_file_support(parser):
    '''
    Add support for file input and output parameters to an argument parser.
    
    :param parser: Argument parser
    :type parser: argparse.ArgumentParser
    '''
    
    parser.add_argument('input',
                        type=str,
                        nargs=1,
                        action='store',
                        help='Input file or directory')
    
    parser_add_format_support(parser)

