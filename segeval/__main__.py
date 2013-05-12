#!/usr/bin/env python
'''
Console interface to the overall segeval package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import print_function
import argparse
import sys


def main(argv=None):
    '''
    Main method for command line parsing and actions.
    '''
    parser = argparse.ArgumentParser(prog='segeval',
                                     description='A discourse segmentation '+\
                                            'evaluation utility.')
    # Eval
    subparsers = parser.add_subparsers(title='metric', 
                                       description='Calculates a specified '+\
                                            'segmentation evaluation '+\
                                            'statistics/performs an '+\
                                            'operation upon provided data.',
                                       help='Available metrics/operations',
                                       dest='subparser_name')
    # Parse arguments
    args = None
    if argv:
        args = parser.parse_args(argv)
    else:
        args = parser.parse_args()
    
    return args.func(vars(args))


if __name__ is '__main__':
    # pylint: disable=C0103,W0703
    
    output = main()
    if output is not None:
        print(output)
    sys.exit(0)

