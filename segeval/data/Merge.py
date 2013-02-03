'''
Data merge tools.  Used to merge multiple files into one.

.. seealso:: File format documentation in: `Segmentation Representation \
Specification <http://nlp.chrisfournier.ca/publications/#seg_spec>`_.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2012, Chris Fournier
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#       
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================
from . import load_files, Dataset, DataIOError
from .JSON import output_linear_mass_json
from .. import InputError


OUTPUT_NAME = 'Merge segmentations operation'
SHORT_NAME  = 'Merge'



def parse(args):
    '''
    Parse this module's metric arguments and perform requested actions.
    '''
    # pylint: disable=C0103
    output = None
        
    # Is a TSV requested?
    if args['output'] != None:
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
        raise InputError('No output file specified.')
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

