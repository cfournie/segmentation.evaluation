'''
Window based evaluation methods package.

@author: Chris Fournier
@contact: chris.m.fournier@gmail.com
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
from .. import convert_masses_to_segments, convert_segments_to_masses


def load_tests(loader, tests, pattern):
    '''
    A load_tests functions utilizing the default loader.
    '''
    from ..Utils import default_load_tests
    return default_load_tests(__file__, loader, tests, pattern)



def compute_window_size_from_masses(segs_dict_all, fnc_round=round):
    masses = list()
    # List all masses
    for segs_dict_all_g in segs_dict_all.values():
        for coder_segs in segs_dict_all_g.values():
            for coder_seg in coder_segs.values():
                masses.extend(coder_seg)
    masses = [float(mass) for mass in masses]
    # Calculate
    avg = average(masses) / 2.0
    window_size = int(fnc_round(avg))
    return window_size if window_size > 1 else 2
    

def compute_window_size(ref_segments, fnc_round=round):
    '''
    Compute the window size to use with window_diff from half of the average
    segment length in the reference segmentation.
    
    Arguments:
    ref_segments -- An ordered sequence of which section each unit belongs to,
                    e.g.: [1,1,1,1,1,2,2,2,3,3,3,3,3], for 13 units (e.g.
                    sentences, paragraphs)
    fnc_round    -- rounding function to use (default: Python's default).  
                    WinDiff is very sensitive to window size, so to reproduce
                    results from another implementation another rounding
                    function may need to be specified (e.g. ceil, floor, etc.).
    
    Returns:
    Integer window size to use with win_diff.
    '''
    masses = convert_segments_to_masses(ref_segments)
    masses = [float(mass) for mass in masses]
    avg = average(masses) / 2.0
    window_size = int(fnc_round(avg))
    return window_size if window_size > 1 else 2

