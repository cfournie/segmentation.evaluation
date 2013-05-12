'''
Arstein Poesio's annotator bias.

References:
    
    Ron Artstein and Massimo Poesio. 2008. Inter-coder agreement for
    computational linguistics. Computational Linguistics, 34(4):555-596. MIT
    Press.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from . import DEFAULT_N_T
from .kappa import fleiss_kappa_linear
from .pi import fleiss_pi_linear
from ..similarity.boundary import boundary_similarity


def artstein_poesio_bias_linear(dataset, fnc_compare=boundary_similarity,
                                n_t=DEFAULT_N_T):
    '''
    Artstein and Poesio's annotator bias, or B (Artstein and Poesio, 2008,
    pp. 572).
    
    Arguments:
    segs_set_all -- A list of document segments for each coder (each in the
                    same item order), e.g.: [an1, an2, an3], where an1 = 
                    [d1, d2, d3], where d1 = segmass_d1.
    
    Returns:
    B as a Decimal object.
    '''
    # pylint: disable=C0103
    A_pi_e     =    fleiss_pi_linear(dataset, fnc_compare=fnc_compare,
                                     return_parts=True, n_t=n_t)[1]
    A_fleiss_e = fleiss_kappa_linear(dataset, fnc_compare=fnc_compare,
                                     return_parts=True, n_t=n_t)[1]
    return A_pi_e - A_fleiss_e

