'''
Console interface to the overall segeval package.

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
import argparse
import sys
from segeval.agreement.Pi import create_parser as create_parser_pi
from segeval.agreement.Kappa import create_parser as create_parser_kappa
from segeval.agreement.Bias import create_parser as create_parser_bias
from segeval.ml.FbMeasure import create_parser as create_parser_fmeasure
from segeval.ml.Percentage import create_parser as create_parser_percentage
from segeval.similarity.SegmentationSimilarity import create_parser as \
    create_parser_similarity
from segeval.similarity.ML import create_parser as create_parser_ml_similarity
from segeval.window.Pk import create_parser as create_parser_pk
from segeval.window.WindowDiff import create_parser as create_parser_windowdiff
from segeval.window.WinPR import create_parser as create_parser_winpr
from segeval.data.Merge import create_parser as create_parser_merge


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
    create_parser_ml_similarity(subparsers)
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


if __name__ == '__main__':
    # pylint: disable=C0103,W0703
    
    output = main()
    if output != None:
        print output
    sys.exit(0)

