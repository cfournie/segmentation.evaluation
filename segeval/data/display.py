'''
Display and output related utility functions.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''


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

    