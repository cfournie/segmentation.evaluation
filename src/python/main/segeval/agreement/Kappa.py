'''
Segmentation versions of Cohen's and Fleiss' Kappa.

References:
    Chris Fournier and Diana Inkpen. 2012. Segmentation Similarity and
    Agreement. Submitted manuscript.
    
    Ron Artstein and Massimo Poesio. 2008. Inter-coder agreement for
    computational linguistics. Computational Linguistics, 34(4):555-596. MIT
    Press.
    
    Marti A. Hearst. 1997. TextTiling: Segmenting Text into Multi-paragraph
    Subtopic Passages. Computational Linguistics, 23(1):33-64.

    Jacob Cohen. 1960. A Coefficient of Agreement for Nominal Scales.
    Educational and Psychological Measurement, 20(1):37-46.
    
    Mark Davies and Joseph L. Fleiss. 1982. Measuring agreement for multinomial
    data. Biometrics, 38(4):1047-1051.

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
from ..similarity.SegmentationSimilarity import similarity as similarity_linear


def observed_agreement(segs_set_all):
    '''
    Calculate observed segmentation agreement without accounting for chance.
    
    Arguments:
    segs_set_all -- A list of document segments for each coder (each in the
                    same item order), e.g.: [an1, an2, an3], where an1 = 
                    [d1, d2, d3], where d1 = segmass_d1
    
    Returns:
    unmoved_masses    -- Number of pb unmoved
    total_masses      -- Number of pb total
    coders_boundaries -- Dict of boundaries per coder
    '''
    # pylint: disable=C0103
    all_pbs_unedited = list()
    all_pbs          = list()
    coders_boundaries = dict()
    coders = segs_set_all.values()[0].keys()
    # FOr each permutation of coders
    for m in range(0, len(coders) - 1):
        for n in range(m+1, len(coders)):
            for item in segs_set_all.keys():
                segs_a = segs_set_all[item][coders[m]]
                segs_b = segs_set_all[item][coders[n]]
                pbs_unedited, total_pbs = \
                    similarity_linear(segs_a, segs_b, return_parts=True)[0:2]
                all_pbs_unedited.append(pbs_unedited)
                all_pbs.append(total_pbs)
                # Create in dicts if not present
                if coders[m] not in coders_boundaries:
                    coders_boundaries[coders[m]] = list()
                if coders[n] not in coders_boundaries:
                    coders_boundaries[coders[n]] = list()
                # Add per-coder values to dicts
                coders_boundaries[coders[m]].append(
                    [Decimal(len(segs_a)),
                     total_pbs])
                coders_boundaries[coders[n]].append(
                    [Decimal(len(segs_b)),
                     total_pbs])
    return all_pbs_unedited, all_pbs, coders_boundaries


def cohen_kappa(segs_set_all, return_parts=False):
    '''
    Calculates Cohen's Kappa, originally proposed in Cohen (1960), for
    segmentations.  Adapted from the formulations provided in Hearst (1997) and
    Artstein and Poesio (2008).
    
    Arguments:
    segs_set_all -- A list of document segments for each coder (each in the
                    same item order), e.g.: [an1, an2, an3], where an1 = 
                    [d1, d2, d3], where d1 = segmass_d1
    return_parts -- If true, return the numerator and denominator 
    
    Returns:
    Cohen's Kappa as a Decimal object.
    '''
    # Check that there are exactly 2 coders
    if len([True for coder_segs in segs_set_all.values() \
            if len(coder_segs.keys()) != 2]) > 0:
        raise Exception('Unequal number of items specified.')
    # Check that there are an identical number of items
    num_items = len(segs_set_all.values()[0].keys())
    if len([True for coder_segs in segs_set_all.values() \
            if len(coder_segs.values()) != num_items]) > 0:
        raise Exception('Unequal number of items contained.')
    # Return
    return fleiss_kappa(segs_set_all, return_parts)


def fleiss_kappa(segs_set_all, return_parts=False):
    '''
    Calculates Fleiss' Kappa (or multi-Kappa), originally proposed in Davies and
    Fleiss (1982), for segmentations.  Adapted from the formulations provided in
    Hearst (1997, pp. 53) and Artstein and Poesio (2008).
    
    Arguments:
    segs_set_all -- A list of document segments for each coder (each in the
                    same item order), e.g.: [an1, an2, an3], where an1 = 
                    [d1, d2, d3], where d1 = segmass_d1
    return_parts -- If true, return the numerator and denominator 
    
    Returns:
    Fleiss' Kappa as a Decimal object.
    '''
    # pylint: disable=C0103,R0914
    # Check that there are more than 2 coders
    if len([True for coder_segs in segs_set_all.values() \
            if len(coder_segs.keys()) < 2]) > 0:
        raise Exception('Less than 2 coders specified.')
    # Check that there are an identical number of items
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
    coders = coders_boundaries_totalboundaries.keys()
    P_segs   = list()
    for m in range(0, len(coders) - 1):
        for n in range(m+1, len(coders)):
            boundaries_m       = sum(info [0] for info in \
                                 coders_boundaries_totalboundaries[coders[m]])
            total_boundaries_m = sum(info [1] for info in \
                                 coders_boundaries_totalboundaries[coders[m]])
            boundaries_n       = sum(info [0] for info in \
                                 coders_boundaries_totalboundaries[coders[n]])
            total_boundaries_n = sum(info [1] for info in \
                                 coders_boundaries_totalboundaries[coders[n]])
            P_segs.append((boundaries_m / total_boundaries_m) * \
                          (boundaries_n / total_boundaries_n))
    P_seg   = sum(P_segs)   / len(P_segs)
    A_e = P_seg
    # Calculate pi
    kappa = (A_o - A_e) / (Decimal('1.0') - A_e)
    # Return
    if return_parts:
        return A_o, A_e
    else:
        return kappa

