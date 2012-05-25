'''
Segmentation version of Arstein and Poesio's inter-coder agreement bias
[ArtsteinPoesio2008]_ that has been adapted to use Segmentation 
Similarity [FournierInkpen2012]_.

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
from .Kappa import fleiss_kappa
from .Pi import fleiss_pi
from .. import compute_mean


def artstein_poesio_bias(dataset_masses):
    '''
    Artstein and Poesio's annotator bias, or B [ArtsteinPoesio2008]_
    (p. 572):
    
    .. math::
        B = A^{\pi^*}_e - A^{\kappa^*}_e
    
    :param items_masses: Segmentation masses for a collection of items where \
                        each item is multiply coded (all coders code all items).
    :type items_masses: dict
    
    :returns: B, or Bias
    :rtype: :class:`decimal.Decimal`
    
    .. seealso:: :func:`segeval.agreement.observed_agreement` for an example of\
     ``items_masses``.
    '''
    # pylint: disable=C0103
    A_pi_e     = fleiss_pi(   dataset_masses, return_parts=True)[1]
    A_fleiss_e = fleiss_kappa(dataset_masses, return_parts=True)[1]
    return A_pi_e - A_fleiss_e


def mean_artstein_poesio_bias(dataset_masses):
    '''
    Calculate mean segmentation bias.
    
    .. seealso:: :func:`artstein_poesio_bias`, :func:`segeval.compute_mean`
    
    :param dataset_masses: Segmentation mass dataset (including multiple \
                           codings).
    :type dataset_masses: dict
    
    :returns: Mean, standard deviation, and variance.
    :rtype: :class:`decimal.Decimal`, :class:`decimal.Decimal`, :class:`decimal.Decimal`
    '''
    return compute_mean(dataset_masses, artstein_poesio_bias)

