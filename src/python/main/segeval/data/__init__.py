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
from .. import convert_positions_to_masses

RESULTS             = ['summary', 'tsv']

DEFAULT_DELIMITER   = '\t'


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
    

def input_linear_mass_tsv(tsv_filename, delimiter=DEFAULT_DELIMITER):
    '''
    Load a linear segmentation mass TSV file.
    
    :param tsv_filename: path to the mass file containing segment mass codings.
    :param delimiter:    the delimiter used when reading a TSV file (by default,
                         a tab, but it can also be a comma, whitespace, etc.
    :type tsv_filename: str
    :type delimiter: str
    
    :returns: Segmentation mass codings.
    :rtype: :func:`dict`
    '''
    # List version of file
    header = []
    segment_masses = dict()
    # Open file
    csv_file = open(tsv_filename, 'rU')
    # Read in file
    try:
        reader = csv.reader(csv_file, delimiter=delimiter)
        for i, row in enumerate(reader):
            # Read annotators from header
            if i == 0:
                for item in row[1:]:
                    header.append(item)
            # Read data
            else:
                coder = None
                for j, col in enumerate(row):
                    # Skip the first col
                    if j == 0:
                        coder = str(col)
                        segment_masses[coder] = list()
                    elif j > 0:
                        segment_masses[coder].append(int(col))
    # pylint: disable=C0103
    except Exception as exception:
        raise DataIOError('Error occurred processing file: %s' \
                                      % tsv_filename, exception)
    finally:
        csv_file.close()
    return segment_masses


def input_linear_positions_tsv(tsv_filename, delimiter=DEFAULT_DELIMITER):
    '''
    Load a segment position TSV file.
    
    :param csv_filename: path to the mass file containing segment position
                         codings.
    :param delimiter:    the delimiter used when reading a TSV file (by default,
                         a tab, but it can also be a comma, whitespace, etc.
    :type csv_filename: str
    :type delimiter: str
    
    .. deprecated:: 1.0
    
    .. warning:: This i/o function is for legacy files only and will be removed
        in later versions.
    
    :returns: Segmentation mass codings.
    :rtype: :func:`dict`
    '''
    coder_positions = input_linear_mass_tsv(tsv_filename, delimiter)
    # Convert each segment position to masses
    for coder, positions in coder_positions.items():
        coder_positions[coder] = convert_positions_to_masses(positions)
    # Return
    return coder_positions


def input_linear_mass_json(json_filename):
    '''
    Load a segment mass JSON file.
    
    :param json_filename: path to the mass file containing segment position
                          codings.
    :type json_filename: str
    
    :returns: Segmentation mass codings.
    :rtype: :func:`dict`
    
    .. seealso:: `JSON (JavaScript Object Notation) <http://www.json.org/>`_.
    '''
    codings = dict()
    data = dict()
    # Open file
    json_file = open(json_filename, 'rU')
    # Read in file
    try:
        data = json.load(json_file)
    except Exception as exception:
        raise DataIOError('Error occurred processing file: %s' \
                                      % json_filename, exception)
    # Check type
    if 'segmentation_type' in data:
        if data['segmentation_type'] != 'linear':
            raise DataIOError(
                'Segmentation type \'linear\' expected, but encountered %s' % \
                data['segmentation_type'])
    # Remove the metadata layer
    if 'codings' in data:
        data = data['codings']
    else:
        data = data
    # Convert coder labels into strings
    for key, value in data.items():
        codings[key] = value
    # Return
    return codings


FILETYPE_TSV  = 'tsv'
FILETYPE_JSON = 'json'

EXT = 'ext'
FNC = 'ext'
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
                        help='Delimiting character for TSV files; ignored if '+\
                        'JSON is specified and is a tab if unspecified')

