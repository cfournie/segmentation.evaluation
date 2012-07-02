'''
TSV output module (for general TSV writing operations).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2011-2012, Chris Fournier
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
import csv
import os
from .. import convert_positions_to_masses


DEFAULT_DELIMITER = '\t'


def write_tsv(filepath, header, rows):
    '''
    Write a TSV file using the given header and rows.
    
    :param filepath: Path and filename of a file to write to
    :param header:   List of category names
    :param rows:     Data to write for all categories
    :type filepath: str
    :type header:   :class:`list`
    :type rows:     :class:`list` of :class:`list`
    '''
    # Create a default filename if a dir is specified
    if os.path.isdir(filepath):
        filepath = os.path.join(filepath, 'output.tsv')
    # Open file
    tsv = csv.writer(open(filepath, 'wb'), delimiter='\t', quotechar='"',
                     quoting=csv.QUOTE_MINIMAL)
    tsv.writerow(header)
    for row in rows:
        tsv.writerow(row)


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
    from . import Dataset, DataIOError, name_from_filepath
    # List version of file
    header = []
    dataset = Dataset()
    item = name_from_filepath(tsv_filename)
    dataset[item] = dict()
    # Open file
    csv_file = open(tsv_filename, 'rU')
    # Read in file
    try:
        reader = csv.reader(csv_file, delimiter=delimiter)
        for i, row in enumerate(reader):
            # Read annotators from header
            if i == 0:
                for col_name in row[1:]:
                    header.append(col_name)
            # Read data
            else:
                coder = None
                for j, col in enumerate(row):
                    # Skip the first col
                    if j == 0:
                        coder = str(col)
                        dataset[item][coder] = list()
                    elif j > 0:
                        dataset[item][coder].append(int(col))
    # pylint: disable=C0103
    except Exception as exception:
        raise DataIOError('Error occurred processing file: %s' \
                                      % tsv_filename, exception)
    finally:
        csv_file.close()
    return dataset


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
    dataset = input_linear_mass_tsv(tsv_filename, delimiter)
    # Convert each segment position to masses
    for item, coder_positions in dataset.items():
        for coder, positions in coder_positions.items():
            dataset[item][coder] = convert_positions_to_masses(positions)
    # Return
    return dataset

