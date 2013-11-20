'''
TSV output module (for general TSV writing operations).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import csv
from segeval.format import convert_positions_to_masses


DEFAULT_DELIMITER = '\t'


def input_linear_mass_tsv(filepath, delimiter=DEFAULT_DELIMITER):
    '''
    Takes a file path.  Returns segmentation mass codings as a :class:`Dataset`.

    :param filepath: path to the mass file containing segment mass codings.
    :param delimiter:    the delimiter used when reading a TSV file (by default,
                         a tab, but it can also be a comma, whitespace, etc.
    :type filepath: str
    :type delimiter: str
    '''

    from segeval.data import Dataset, name_from_filepath
    # List version of file
    header = []
    dataset = Dataset()
    item = name_from_filepath(filepath)
    dataset[item] = dict()
    # Open file
    with open(filepath, 'rU') as csv_file:
        # Read in file
        reader = csv.reader(csv_file, delimiter=delimiter)
        for i, row in enumerate(reader):
            # Read annotators from header
            if i is 0:
                for col_name in row[1:]:
                    header.append(col_name)
            # Read data
            else:
                coder = None
                for j, col in enumerate(row):
                    # Skip the first col
                    if j is 0:
                        coder = str(col)
                        dataset[item][coder] = list()
                    else:
                        dataset[item][coder].append(int(col))
                dataset[item][coder] = tuple(dataset[item][coder])

    return dataset


def input_linear_positions_tsv(filepath, delimiter=DEFAULT_DELIMITER):
    '''
    Takes a file path.  Returns segmentation mass codings as a :class:`Dataset`.

    :param filepath: path to the mass file containing segment position
                         codings.
    :param delimiter:    the delimiter used when reading a TSV file (by default,
                         a tab, but it can also be a comma, whitespace, etc.
    :type filepath: str
    :type delimiter: str

    .. deprecated:: 1.0

    .. warning:: This I/O function is for legacy files only and will be removed
        in later versions.
    '''
    dataset = input_linear_mass_tsv(filepath, delimiter)
    # Convert each segment position to masses
    for item, coder_positions in dataset.items():
        for coder, positions in coder_positions.items():
            dataset[item][coder] = convert_positions_to_masses(positions)
    # Return
    return dataset
