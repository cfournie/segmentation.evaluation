'''
Data I/O package.  Used to import and export data to and from TSV and JSON
files.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import os
import copy
from collections import defaultdict
from segeval.data.tsv import input_linear_mass_tsv
from segeval.data.jsonutils import input_linear_mass_json
from segeval.format import BoundaryFormat

FILETYPE_TSV = 'tsv'
FILETYPE_JSON = 'json'

EXT = 'ext'
FNC = 'fnc'
FILETYPES = {FILETYPE_TSV: {EXT: ['.tsv', '.csv'],
                            FNC: input_linear_mass_tsv},
             FILETYPE_JSON: {EXT: ['.json', '.jsn'],
                             FNC: input_linear_mass_json}}
FILETYPES_DEFAULT = FILETYPE_JSON


class Dataset(defaultdict):

    '''
    Represents a set of texts (i.e., items) that have been segmentations by coders.
    '''

    def __init__(self, item_coder_data=None, properties=None,
                 boundary_types=None, boundary_format=BoundaryFormat.mass):
        '''
        Initialize a dataset.
        '''
        defaultdict.__init__(self, dict)
        self.properties = dict()
        self.boundary_format = boundary_format
        # Masses
        if item_coder_data is not None and item_coder_data is not dict:
            defaultdict.update(self, item_coder_data)
        # Properties
        if properties is not None:
            self.properties.update(properties)
        # Boundary types
        if boundary_types is not None:
            self.boundary_types = set(boundary_types)
        else:
            self.boundary_types = set([1])
        # Coders
        self.coders = set()
        # Populate coders
        for coder_masses in defaultdict.values(self):
            for coder in coder_masses.keys():
                self.coders.add(coder)

    def __iadd__(self, other, prepend_item=None):
        '''
        Add one dataset's data to this dataset.
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
%(coder)s found for item %(item)s' % {'coder': coder, 'item': item})
        return self

    def __add__(self, other):
        '''
        Copy this dataset and add the other dataset to it.
        '''
        dataset = self.copy()
        dataset += other
        return dataset

    def copy(self):
        '''
        Create a deep copy of the entire dataset object and properties.
        '''
        dataset = copy.deepcopy(self)
        dataset.coders = copy.deepcopy(self.coders)
        dataset.properties = copy.deepcopy(self.properties)
        dataset.boundary_types = copy.deepcopy(self.boundary_types)
        dataset.boundary_format = copy.deepcopy(self.boundary_format)
        return dataset


def get_coders(container):
    if isinstance(container, Dataset):
        return container.coders
    else:
        coders = set()
        for value in container.values():
            coders = coders.union(value.keys())
        return coders


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

    '''

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
        else:
            name, ext = os.path.splitext(name)
            if len(ext) > 0 and ext.lower() in allowable_extensions:
                files[name] = path
                datafile_found = True
    # If a data file was found
    if datafile_found:
        # If TSV files were found, load
        for name, filepath in files.items():
            other = fnc_load(filepath)
            dataset.__iadd__(other, prepend_item=prepend_item)
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
