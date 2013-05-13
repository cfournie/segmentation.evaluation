'''
TSV output module (for general TSV writing operations).

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import csv
import os
from ..format import convert_positions_to_masses


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
    with csv.writer(open(filepath, 'wb'), delimiter='\t', quotechar='"',
                     quoting=csv.QUOTE_MINIMAL) as tsv:
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
    # pylint: disable=R0914
    from . import Dataset, name_from_filepath
    # List version of file
    header = []
    dataset = Dataset()
    item = name_from_filepath(tsv_filename)
    dataset[item] = dict()
    # Open file
    with open(tsv_filename, 'rU') as csv_file:
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
                    elif j > 0:
                        dataset[item][coder].append(int(col))
        # pylint: disable=C0103
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

