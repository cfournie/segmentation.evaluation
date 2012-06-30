'''
Display and output related utility functions.

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


def values_to_str(mean, std, var, stderr, n):
    '''
    Create a text representation of a metric's mean.
    '''
    # pylint: disable=C0103
    return ('\tmean\t= %(mean)s\t(macro)\n'+\
            '\tstd\t= %(std)s\n'+\
            '\tvar\t= %(var)s\n'+\
            '\tstderr\t= %(stderr)s\t(n=%(n)s)') % \
            {'mean'   : mean,
             'std'    : std,
             'var'    : var,
             'stderr' : stderr,
             'n'      : n}

def pairs_to_str(pairs):
    '''
    Create a text representation of a metric's mean.
    '''
    # pylint: disable=C0103
    values = list()
    for name, value in pairs.items():
        values.append('\t%(name)s\t= %(value)s' % \
                      {'name'  : name,
                       'value' : value})
    return '\n'.join(values)


def render_mean_values(name, mean, std, var, stderr, n):
    '''
    Render text representing means of a metric.
    '''
    # pylint: disable=C0103,R0913
    return render_value(name, values_to_str(mean, std, var, stderr, n),
                        operator='\n')


def render_mean_micro_values(name, mean):
    '''
    Render text representing means of a metric.
    '''
    return render_value(name, '\tmean\t= %s\t(micro)' % mean,
                        operator='\n')


def render_agreement_coefficients(name, pairs):
    '''
    Render text representing means of a metric.
    '''
    # pylint: disable=C0103,R0913
    return render_value(name, pairs_to_str(pairs),
                        operator='\n')


def render_value(name, value, operator='='):
    '''
    Render text representing the value of a metric.
    '''
    return '%(name)s %(operator)s %(value)s' % {'name' : name,
                                                'value' : value,
                                                'operator' : operator}

def render_permuted(name, permuted):
    '''
    Render text to indicate that permutation is performed.
    
    :param name:      Name of a method
    :param permuted:  Whether permutation is performed or not
    :type name:     str
    :type permuted: bool
    
    '''
    output = name
    if permuted:
        output = '%s (permuted)' % name
    return output




    