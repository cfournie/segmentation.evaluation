'''
Window based evaluation methods package.

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
from numpy import mean, std, var, average
from .. import convert_masses_to_segment_pos, convert_segment_pos_to_masses


def load_tests(loader, tests, pattern):
    '''
    A ``load_tests()`` function utilizing the default loader :func:`segeval.Utils.default_load_tests`.
    
    .. seealso:: The `load_tests protocol <http://docs.python.org/library/unittest.html#load-tests-protocol>`_.
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
    # List all masses
    def __list_coder_masses__(inner_coder_masses):
        '''
        Recursively collect all masses.
        
        :param inner_coder_masses: Either a dict of dicts, or dict of a list of masses.
        :type inner_coder_masses: dict or list
        '''
        if isinstance(inner_coder_masses, list):
            masses.extend(inner_coder_masses)
        elif isinstance(inner_coder_masses, dict):
            for cur_inner_coder_masses in inner_coder_masses.values():
                __list_coder_masses__(cur_inner_coder_masses)
    # Convert to floats
    masses = [float(mass) for mass in masses]
    # Calculate
    avg = average(masses) / 2.0
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
    masses = convert_segment_pos_to_masses(reference_segments)
    masses = [float(mass) for mass in masses]
    avg = average(masses) / 2.0
    window_size = int(fnc_round(avg))
    return window_size if window_size > 1 else 2

