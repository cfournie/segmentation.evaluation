'''
JSON output module (for general JSON writing operations).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import json
import os
import codecs
from segeval.util.lang import enum


Field = enum(
    # Property fields
    segmentation_type='segmentation_type',
    # Structural fields
    items='items'
)

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
    data = {Field.segmentation_type: SegmentationType.linear}
    data[Field.items] = dataset
    data.update(dataset.properties)
    __write_json__(filepath, data)


def input_linear_mass_json(filepath):
    '''
    Reads a file path. Returns segmentation mass codings as a :class:`Dataset`.

    :param filepath: Path to the mass file containing segment position codings.
    :type filepath: :func:`str`
    '''
    from segeval.data import Dataset, DataIOError
    dataset = Dataset()
    data = dict()
    # Open file
    json_file = open(filepath, 'rU')
    # Read in file
    try:
        data = json.load(json_file)
    except Exception as exception:
        raise DataIOError(
            'Error occurred processing file: ' + filepath, exception)
    # Check type
    if Field.segmentation_type in data:
        if data[Field.segmentation_type] != SegmentationType.linear:
            raise DataIOError('Segmentation type \'{0}\' expected, but encountered \'{1}\' for file: {2}'
                              .format(SegmentationType.linear, data[Field.segmentation_type], filepath))
    else:
        raise DataIOError(
            'The entry \'segmentation_type\' was expected in JSON for file:' + filepath)
    # Duplicate to store other properties
    dataset.properties = data
    # If separated into multiple items for one coder per file
    if Field.items in data:
        data = data[Field.items]
        # Convert item labels into strings
        for item, coder_masses in data.items():
            dataset[item] = dict()
            for coder, masses in coder_masses.items():
                dataset[item][coder] = tuple(masses)
        # Remove from properties
        del dataset.properties[Field.items]
    else:
        raise DataIOError('Expected an entry \'{0}\' that contained segmentation codings for specific individual texts (i.e., items) in file: {1}'
                          .format(Field.items, filepath))
    return dataset
