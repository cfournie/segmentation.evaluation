'''
Data merge tools.  Used to merge multiple files into one.

.. seealso:: File format documentation in: `Segmentation Representation \
Specification <http://nlp.chrisfournier.ca/publications/#seg_spec>`_.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from . import load_files, Dataset, DataIOError
from .jsonutils import output_linear_mass_json


OUTPUT_NAME = 'Merge segmentations operation'
SHORT_NAME  = 'Merge'


def parse(args):
    '''
    Parse this module's metric arguments and perform requested actions.
    '''
    # pylint: disable=C0103
    output = None
        
    # Is a TSV requested?
    if args['output'] is not None:
        # Create a TSV
        output_file = args['output'][0]
        values = load_files(args)
        dataset = Dataset()
        
        for other in values:
            dataset.add(other)
        
        # Output
        output = 'Merged:\n\tFiles:\t%(files)i\n\tCoders:\t%(coders)i\n\t\
Items:\t%(items)i' % {'files'  : len(values),
                      'coders' : len(dataset.coders),
                      'items'  : len(dataset)}
        output_linear_mass_json(output_file,
                                dataset)
    else:
        raise DataIOError('No output file specified.')
    return output


def create_parser(subparsers):
    '''
    Setup a command line parser for this module's metric.
    '''
    parser = subparsers.add_parser('merge',
                                   help=OUTPUT_NAME)
    parser_add_merge_support(parser)
    parser.set_defaults(func=parse)


def parser_add_merge_support(parser):
    '''
    Add support for file input and output parameters to an argument parser.
    
    :param parser: Argument parser
    :type parser: argparse.ArgumentParser
    '''
    from ..data import parser_add_format_support
    
    parser.add_argument('input',
                        type=str,
                        nargs='+',
                        action='store',
                        help='Input files or directories')
    
    parser_add_format_support(parser)

