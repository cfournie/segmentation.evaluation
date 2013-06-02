'''
JSON output module (for general JSON writing operations).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import json
import os
import codecs


FIELD_SEGMENTATION_TYPE   = 'segmentation_type'
TYPE_LINEAR               = 'linear'
FIELD_ITEMS               = 'items'
FIELD_CODINGS             = 'codings'
FIELD_HAS_REFERENCE_CODER = 'has_reference_coder'


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
        

def output_linear_mass_json(filepath, dataset):
    '''
    Compose an output file's fields and output a JSON file.
    '''
    data = {FIELD_SEGMENTATION_TYPE : TYPE_LINEAR}
    if len(dataset) > 0:
        data[FIELD_ITEMS] = dataset
    else:
        data[FIELD_CODINGS] = dataset
    data.update(dataset.properties)
    write_json(filepath, data)
    
    

def input_linear_mass_json(filepath, create_item=False):
    '''
    Load a segment mass JSON file.
    
    :param json_filename: path to the mass file containing segment position
                          codings.
    :type json_filename: str
    
    :returns: Segmentation mass codings.
    :rtype: :func:`dict`
    
    .. seealso:: `JSON (JavaScript Object Notation) <http://www.json.org/>`_.
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
    if FIELD_SEGMENTATION_TYPE in data:
        if data[FIELD_SEGMENTATION_TYPE] != TYPE_LINEAR:
            raise DataIOError(
                'Segmentation type \'%(type)s\' expected, but encountered \
\'%(type_found)s\'' % {'type'       : TYPE_LINEAR,
                   'type_found' : data[FIELD_SEGMENTATION_TYPE]})
    # Duplicate to store other properties
    dataset.properties = data
    # Remove the metadata layer
    # If separated into multiple codings of one item per file
    if FIELD_CODINGS in data:
        data = data[FIELD_CODINGS]
        item = name
        dataset[item] = dict()
        # Convert coder labels into strings
        for coder, masses in data.items():
            dataset[item][coder] = tuple(masses)
        # Undo item
        if not create_item:
            dataset = dataset[item]
        # Remove from properties
        del dataset.properties[FIELD_CODINGS]
    # If separated into multiple items for one coder per file
    elif FIELD_ITEMS in data:
        data = data[FIELD_ITEMS]
        # Convert item labels into strings
        for item, coder_masses in data.items():
            dataset[item] = dict()
            for coder, masses in coder_masses.items():
                dataset[item][coder] = tuple(masses)
        # Remove from properties
        del dataset.properties[FIELD_ITEMS]
    # Return
    return dataset

