'''
JSON output module (for general JSON writing operations).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import json
import os
import codecs
from ..util.lang import enum


Field = enum(segmentation_type='segmentation_type',
             # Structure
             items='items',
             codings='codings')

SegmentationType = enum(linear='linear')


def __write_json__(filepath, data):
    '''
    Write a JSON file using the given data.
    '''
    # Create a default filename if a dir is specified
    if os.path.isdir(filepath):
        filepath = os.path.join(filepath, 'output.json')
    # Open file
    json_file = codecs.open(filepath, 'w+', 'utf-8')
    try:
        json.dump(data, fp=json_file, sort_keys=True, indent=4)
    finally:
        json_file.close()
        

def output_linear_mass_json(filepath, dataset):
    '''
    Takes a file path and :class:`Dataset` and serializes it as JSON.

    :param filepath: Path to the mass file containing segment position codings.
    :type filepath: :func:`str`
    '''
    data = {Field.segmentation_type : SegmentationType.linear}
    if len(dataset) > 0:
        data[Field.items] = dataset
    else:
        data[Field.codings] = dataset
    data.update(dataset.properties)
    __write_json__(filepath, data)
    
    

def input_linear_mass_json(filepath):
    '''
    Reads a file path. Returns segmentation mass codings as a :class:`Dataset`.
    
    :param filepath: Path to the mass file containing segment position codings.
    :type filepath: :func:`str`
    '''
    from . import Dataset, DataIOError, name_from_filepath
    dataset = Dataset()
    data = dict()
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
    if Field.segmentation_type in data:
        if data[Field.segmentation_type] != SegmentationType.linear:
            raise DataIOError(
                'Segmentation type \'%(type)s\' expected, but encountered \
\'%(type_found)s\'' % {'type'       : SegmentationType.linear,
                   'type_found' : data[Field.segmentation_type]})
    # Duplicate to store other properties
    dataset.properties = data
    # Remove the metadata layer
    # If separated into multiple codings of one item per file
    if Field.codings in data:
        data = data[Field.codings]
        item = name
        dataset[item] = dict()
        # Convert coder labels into strings
        for coder, masses in data.items():
            dataset[item][coder] = tuple(masses)
        # Undo item
        dataset = dataset[item]
        # Remove from properties
        del dataset.properties[Field.codings]
    # If separated into multiple items for one coder per file
    elif Field.items in data:
        data = data[Field.items]
        # Convert item labels into strings
        for item, coder_masses in data.items():
            dataset[item] = dict()
            for coder, masses in coder_masses.items():
                dataset[item][coder] = tuple(masses)
        # Remove from properties
        del dataset.properties[Field.items]
    # Return
    return dataset

