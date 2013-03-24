#!/usr/bin/env python
'''
Console interface to the overall segeval package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import print_function
import argparse
import sys
from segeval.agreement.pi import create_parser as create_parser_pi
from segeval.agreement.kappa import create_parser as create_parser_kappa
from segeval.agreement.bias import create_parser as create_parser_bias
from segeval.ml.fbmeasure import create_parser as create_parser_fmeasure
from segeval.ml.percentage import create_parser as create_parser_percentage
from segeval.similarity.Linear import (
    create_parser as create_parser_similarity)
from segeval.window.pk import create_parser as create_parser_pk
from segeval.window.windowdiff import create_parser as create_parser_windowdiff
from segeval.window.winpr import create_parser as create_parser_winpr
from segeval.data.merge import create_parser as create_parser_merge


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
    create_parser_pi(subparsers)
    create_parser_kappa(subparsers)
    create_parser_bias(subparsers)
    create_parser_fmeasure(subparsers)
    create_parser_percentage(subparsers)
    create_parser_similarity(subparsers)
    create_parser_pk(subparsers)
    create_parser_windowdiff(subparsers)
    create_parser_winpr(subparsers)    
    # Util
    create_parser_merge(subparsers)
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

