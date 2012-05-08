'''
Data import package.

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
from .. import convert_segment_pos_to_masses


def load_tests(loader, tests, pattern):
    '''
    A ``load_tests()`` function utilizing the default loader :func:`segeval.Utils.default_load_tests`.
    
    .. seealso:: The `load_tests protocol <http://docs.python.org/library/unittest.html#load-tests-protocol>`_.
    '''
    #pylint: disable=W0613
    from ..Utils import default_load_tests
    return default_load_tests(__file__, loader, tests)


class SegmentationMetricError(Exception):
    '''
    Indicates that an input processing error has occurred.
    '''
    
    def __init__(self, message):
        Exception.__init__(self, message)


CSV_EXTENSIONS = ['.tsv', '.csv']


def load_nested_folders_dict(containing_dir, fnc_load):
    '''
    '''
    data = dict()
    csv_found = False
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
            files[name] = path
            if len(ext) > 0 and ext.lower() in CSV_EXTENSIONS:
                csv_found = True
    
    if csv_found:
        # If CSV files were found, load
        for name, filepath in files.items():
            data[name] = fnc_load(filepath)
    else:
        # If only dirs were found, recurse
        for name, dirpath in dirs.items():
            data[name] = load_nested_folders_dict(dirpath, fnc_load)
    
    return data
    

def input_linear_mass_csv(csv_filename):
    '''
    Load a mass CSV file.
    
    Arguments:
    csv_filename -- path to the mass file containing segment mass codings.
    
    Returns:
    Dictionary of chapter segment mass codings.
    '''
    # List version of file
    header = []
    segment_masses = dict()
    # Open file
    csv_file = open(csv_filename, 'rU')
    # Read in file
    try:
        reader = csv.reader(csv_file)
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
                        segment_masses[coder] = list()
                    elif j > 0:
                        segment_masses[coder].append(int(col))
    # pylint: disable=C0103
    except Exception as exception:
        raise SegmentationMetricError('Error occurred processing file: %s\n' \
                                      % csv_filename, exception)
    finally:
        csv_file.close()
    return segment_masses


def input_linear_segment_csv(csv_filename):
    '''
    Load a segment position CSV file.
    
    Arguments:
    csv_filename -- path to the mass file containing segment position codings.
    
    Returns:
    Dictionary of chapter segment mass codings.
    '''
    segment_positions = input_linear_mass_csv(csv_filename)
    # Convert each segment position to masses
    for coder, positions in segment_positions.items():
        segment_positions[coder] = convert_segment_pos_to_masses(positions)
    # Return
    return segment_positions

