'''
Converts morphological segmentation input into segmentation masses to be
evaluated.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import csv
from .. import Dataset, DataIOError, name_from_filepath
from ..JSON import FIELD_HAS_REFERENCE_CODER
from ..TSV import DEFAULT_DELIMITER


CODER_REFERENCE = 'reference'


def input_morphemes(tsv_filename, reference_coder=False,
                    delimiter=DEFAULT_DELIMITER):
    '''
    Load a morphological segmentation TSV file for a single coder representing
    many items.
    
    :param tsv_filename: path to the mass file containing words and morphological
                         segmentations.
    :param delimiter:    the delimiter used when reading a TSV file (by default,
                         a tab, but it can also be a comma, whitespace, etc.
    :type tsv_filename: str
    :type delimiter: str
    
    :returns: Segmentation mass codings.
    :rtype: :func:`dict`
    '''
    # pylint: disable=R0914
    # List version of file
    dataset = Dataset()
    coder = CODER_REFERENCE if reference_coder else \
        name_from_filepath(tsv_filename)
    if reference_coder:
        dataset.properties[FIELD_HAS_REFERENCE_CODER] = True
        
    # Open file
    csv_file = open(tsv_filename, 'rU')
    # Read in file
    try:
        reader = csv.reader(csv_file, delimiter=delimiter)
        for row in reader:
            # Read data
            item = None
            for j, col in enumerate(row):
                if j == 0:
                    # First col is the word (i.e., item)
                    item = str(col)
                elif j == 1:
                    # First col is the morphological segmentation (i.e., masses)
                    options = [option.strip() for option in col.split(',')]
                    for i, option in enumerate(options):
                        current_coder = coder if i == 0 else coder + str(i + 1)
                        # Create coder if it does not exist
                        if item not in dataset:
                            dataset[item] = dict()
                        # Convert into segment mass
                        dataset[item][current_coder] = \
                            [len(morpheme) for morpheme in option.split(' ')]
    # pylint: disable=C0103
    except Exception as exception:
        raise DataIOError('Error occurred processing file: %s' \
                                      % tsv_filename, exception)
    finally:
        csv_file.close()
    return dataset

