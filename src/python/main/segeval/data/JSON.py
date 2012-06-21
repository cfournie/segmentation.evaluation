'''
JSON output module (for general JSON writing operations).

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
import json
import os
import codecs


def write_json(filepath, data):
    '''
    Write a JSON file using the given data.
    
    :param filepath:   Path and filename of a file to write to
    :param data:       Data, in dictionary or list form, to write
    :type filepath:   str
    :type dictionary: :class:`dict` or :class:`list`
    '''
    # Create a default filename if a dir is specified
    if os.path.isdir(filepath):
        filepath = os.path.join(filepath, 'output.tsv')
    # Open file
    json_file = codecs.open(filepath, 'w+', 'utf-8')
    try:
        json.dump(data, fp=json_file, sort_keys=True, indent=4)
    finally:
        json_file.close()
        

def output_linear_mass_json(filepath, dataset_masses, multiple):
    pass

def input_linear_mass_json(filepath):
    '''
    Load a segment mass JSON file.
    
    :param json_filename: path to the mass file containing segment position
                          codings.
    :type json_filename: str
    
    :returns: Segmentation mass codings.
    :rtype: :func:`dict`
    
    .. seealso:: `JSON (JavaScript Object Notation) <http://www.json.org/>`_.
    '''
    from . import DataIOError, name_from_filepath
    dataset_masses = dict()
    data           = dict()
    name = name_from_filepath(filepath)
    # Open file
    json_file = open(filepath, 'rU')
    # Read in file
    try:
        data = json.load(json_file)
    except Exception as exception:
        raise DataIOError('Error occurred processing file: %s' \
                                      % filepath, exception)
    # Check type
    if 'segmentation_type' in data:
        if data['segmentation_type'] != 'linear':
            raise DataIOError(
                'Segmentation type \'linear\' expected, but encountered %s' % \
                data['segmentation_type'])
    # Remove the metadata layer
    # If separated into multiple codings of one item per file
    if 'codings' in data:
        data = data['codings']
        item = name
        dataset_masses[item] = dict()
        # Convert coder labels into strings
        for coder, segment_masses in data.items():
            dataset_masses[item][coder] = segment_masses
    # If separated into multiple items for one coder per file
    elif 'items' in data:
        data = data['items']
        coder = name
        # Convert item labels into strings
        for item, segment_masses in data.items():
            dataset_masses[item] = {coder : segment_masses}
    # Return
    return dataset_masses
