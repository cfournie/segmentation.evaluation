'''
Window based evaluation metricks package.  Provides window based segmentation
evaluation metrics including:

* Pk 
* WindowDiff and
* WinPR

.. warning:: These are provided for comparison, but are not recommended for \
    segmentation evaluation.  Instead, use  the segmentation similarity
    metric [FournierInkpen2012]_ implemented in
    :func:`segeval.similarity.SegmentationSimilarity.similarity` and the
    associated inter-coder agreement coefficients in
    :mod:`segeval.agreement`.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
#===============================================================================
# Copyright (c) 2011-2012, Chris Fournier
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
from decimal import Decimal
from ..Math import mean, std, var
from .. import convert_positions_to_masses


def load_tests(loader, tests, pattern):
    '''
    A ``load_tests()`` function utilizing the default loader
    :func:`segeval.Utils.default_load_tests`.
    
    .. seealso:: The `load_tests protocol <http://docs.python.org/library/\
    unittest.html#load-tests-protocol>`_.
    '''
    #pylint: disable=W0613
    from ..Utils import default_load_tests
    return default_load_tests(__file__, loader, tests)


def compute_window_size_from_masses(coder_masses, fnc_round=round):
    '''
    Compute a window size from a dict of segment masses.
    
    :param coder_masses: A dict of segment masses.
    :type coder_masses: dict
    '''
    masses = list()
    # Define fnc
    def __list_coder_masses__(inner_coder_masses):
        '''
        Recursively collect all masses.
        
        :param inner_coder_masses: Either a dict of dicts, or dict of a list of
            masses.
        :type inner_coder_masses: dict or list
        '''
        if isinstance(inner_coder_masses, list):
            masses.extend(inner_coder_masses)
        elif isinstance(inner_coder_masses, dict):
            for cur_inner_coder_masses in inner_coder_masses.values():
                __list_coder_masses__(cur_inner_coder_masses)
    # Recurse and list all masses
    __list_coder_masses__(coder_masses)
    # Convert to floats
    masses = [Decimal(mass) for mass in masses]
    # Calculate
    avg = mean(masses) / 2.0
    window_size = int(fnc_round(avg))
    return window_size if window_size > 1 else 2
    

def compute_window_size(reference_segments, fnc_round=round):
    '''
    Compute the window size to use with window_diff from half of the average
    segment length in the reference segmentation.
    
    :param ref_segments: An ordered sequence of which section each unit belongs
        to, e.g., ``[1,1,1,1,1,2,2,2,3,3,3,3,3]`` for 13 units (e.g., sentences,
        paragraphs)
    :param fnc_round: rounding function to use (default: :func:`round`).  
        WinDiff is very sensitive to window size, so to reproduce results from
        another implementation another rounding function may need to be
        specified (e.g. :func:`math.ceil`, :func:`math.floor`, etc.).
    
    :returns: Integer window size to use with win_diff.
    :rtype: int
    '''
    masses = convert_positions_to_masses(reference_segments)
    masses = [Decimal(mass) for mass in masses]
    avg = mean(masses) / Decimal(2)
    window_size = int(fnc_round(avg))
    return window_size if window_size > 1 else 2


def parser_one_minus_support(parser):
    '''
    Add support for the "one minus" parameter to convert penalty metrics into
    reward metrics.
    
    :param parser: Argument parser
    :type parser: argparse.ArgumentParser
    '''
    parser.add_argument('-om', '--oneminus',
                        default=False,
                        action='store_true',
                        help='Calculates 1-metric to make this metric no \
                                longer penalty-based, meaning that 1.0 \
                                represents the best performance and 0.0 the \
                                worst.')
    
    