'''
Segmentation versions of Scott's and Fleiss' Pi.

References:
    Chris Fournier and Diana Inkpen. 2012. Segmentation Similarity and
    Agreement. Submitted manuscript.
    
    Ron Artstein and Massimo Poesio. 2008. Inter-coder agreement for
    computational linguistics. Computational Linguistics, 34(4):555-596. MIT
    Press.
    
    Marti A. Hearst. 1997. TextTiling: Segmenting Text into Multi-paragraph
    Subtopic Passages. Computational Linguistics, 23(1):33-64.
    
    William A. Scott. 1955. Reliability of content analysis: The case of nominal
    scale coding. Public Opinion Quarterly, 19(3):321-325.
    
    Joseph L. Fleiss. 1971. Measuring nominal scale agreement among many raters.
    Psychological Bulletin, 76(5):378-382.

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
from decimal import Decimal
from .Kappa import observed_agreement


def scotts_pi(segs_set_all, return_parts=False):
    '''
    Calculates Scott's Pi, originally proposed in Scott (1995), for
    segmentations.  Adapted from the formulations provided in
    Hearst (1997, pp. 53) and Artstein and Poesio (2008).
    
    Arguments:
    segs_set_a -- List of segmentations (same coder, different documents, in
                  the same order as segs_set_b).
    segs_set_b -- List of segmentations (see segs_set_a).
    
    Returns:
    Segmentation version of Scott's Pi as a Decimal.
    '''
    # Check that there are no more than 2 coders
    if len([True for coder_segs in segs_set_all.values() \
            if len(coder_segs.keys()) > 2]) > 0:
        raise Exception('Unequal number of items specified.')
    # Check that there are an identical number of items
    num_items = len(segs_set_all.values()[0].keys())
    if len([True for coder_segs in segs_set_all.values() \
            if len(coder_segs.values()) != num_items]) > 0:
        raise Exception('Unequal number of items contained.')
    # Return
    return fleiss_pi(segs_set_all, return_parts)


def fleiss_pi(segs_set_all, return_parts=False):
    '''
    Calculates Fleiss' Pi (or multi-Pi), originally proposed in Fleiss (1971),
    for segmentations (and described in Siegel and Castellan (1988) as K).
    Adapted from the formulations provided in Hearst (1997, pp. 53) and Artstein
    and Poesio (2008).
    
    Arguments:
    segs_set_a -- List of segmentations (same coder, different documents, in
                  the same order as segs_set_b).
    segs_set_b -- List of segmentations (see segs_set_a).
    
    Arguments:
    segs_set_all -- A list of document segments for each coder (each in the
                    same item order), e.g.: [an1, an2, an3], where an1 = 
                    [d1, d2, d3], where d1 = segmass_d1.
    
    Returns:
    Segmentation version of Fleiss's Pi as a Decimal.
    '''
    # pylint: disable=C0103,R0914
    # Check that there are an equal number of items for each coder
    num_items = len(segs_set_all.values()[0].keys())
    if len([True for coder_segs in segs_set_all.values() \
            if len(coder_segs.values()) != num_items]) > 0:
        raise Exception('Unequal number of items contained.')
    # Initialize totals
    unmoved_masses, total_masses, coders_boundaries_totalboundaries = \
        observed_agreement(segs_set_all)
    # Calculate Aa
    A_o = sum(unmoved_masses) / sum(total_masses)
    # Calculate Ae
    p_e_segs   = list()
    #p_e_unsegs = list()
    for boundaries_info in coders_boundaries_totalboundaries.values():
        for item in boundaries_info:
            boundaries, total_boundaries = item
            p_e_seg = boundaries / total_boundaries
            p_e_segs.append(p_e_seg)
            #p_e_unsegs.append((Decimal(1) - p_e_seg))
    # Calculate P_e_seg
    P_e_seg   = sum(p_e_segs)   / len(p_e_segs)
    #P_e_unseg = sum(p_e_unsegs) / len(p_e_unsegs)
    A_e = (P_e_seg ** 2) #+ (P_e_unseg ** 2)
    # Calculate pi
    pi = (A_o - A_e) / (Decimal('1.0') - A_e)
    # Return
    if return_parts:
        return A_o, A_e
    else:
        return pi

