'''
Segmentation evaluation metric package. Provides evaluation metrics to
evaluate the performance of both human and automatic text (i.e., discourse)
segmenters.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from __future__ import absolute_import
import sys
from types import ModuleType


# Package description
__version_number__ = '2.0.11'
__release__ = None
__version__ = '-'.join((__version_number__, __release__)) if __release__ is not None else __version_number__
__project__ = 'SegEval'
__package__ = 'segeval'
__author__ = 'Chris Fournier'
__author_email__ = 'chris.m.fournier@gmail.com'
__copyright__ = '2012-2013, ' + __author__
__description__ = 'A package providing text segmentation evaluation metrics and utilities'


# The import magic shown here was taken (nearly verbatim) from the Werkzeug
# package; see http://werkzeug.pocoo.org/

# import mapping to objects in other modules
all_by_module = {
    'segeval.agreement':        ['actual_agreement_linear'],
    'segeval.agreement.bias':   ['artstein_poesio_bias_linear'],
    'segeval.agreement.kappa':  ['fleiss_kappa_linear'],
    'segeval.agreement.pi':     ['fleiss_pi_linear'],
    'segeval.data':             ['Dataset', 'load_nested_folders_dict'],
    'segeval.data.jsonutils':   ['Field', 'input_linear_mass_json',
                                 'output_linear_mass_json'],
    'segeval.data.tsv':         ['input_linear_mass_tsv'],
    'segeval.data.samples':     ['KAZANTSEVA2012_G5', 'KAZANTSEVA2012_G2',
                                 'COMPLETE_AGREEMENT', 'LARGE_DISAGREEMENT',
                                 'HEARST_1997_STARGAZER', 'HYPOTHESIS_STARGAZER'],
    'segeval.ml':               ['Average', 'precision', 'recall',
                                 'fmeasure', 'ConfusionMatrix'],
    'segeval.similarity':       ['boundary_confusion_matrix',
                                 'boundary_statistics'],
    'segeval.similarity.boundary':
                                ['boundary_similarity'],
    'segeval.similarity.segmentation':
                                ['segmentation_similarity'],
    'segeval.similarity.distance.multipleboundary':
                                ['boundary_edit_distance'],
    'segeval.similarity.weight':
                                ['weight_a',
                                 'weight_s',
                                 'weight_s_scale',
                                 'weight_t',
                                 'weight_t_scale'],
    'segeval.window':           ['compute_window_size'],
    'segeval.window.pk':        ['pk'],
    'segeval.window.windowdiff':['window_diff'],
    'segeval.compute':          ['summarize'],
    'segeval.format':           ['BoundaryFormat',
                                 'boundary_string_from_masses',
                                 'convert_positions_to_masses',
                                 'convert_masses_to_positions',
                                 'convert_nltk_to_masses'],
}


object_origins = {}
for module, items in all_by_module.items():
    for item in items:
        object_origins[item] = module


class module(ModuleType):
    """Automatically import objects from the modules."""

    def __getattr__(self, name):
        if name in object_origins:
            module = __import__(object_origins[name], None, None, [name])
            for extra_name in all_by_module[module.__name__]:
                setattr(self, extra_name, getattr(module, extra_name))
            return getattr(module, name)
        return ModuleType.__getattribute__(self, name)

    def __dir__(self):
        """Just show what we want to show."""
        result = list(new_module.__all__)
        result.extend(
            ('__file__', '__path__', '__doc__', '__all__',
             '__docformat__', '__name__', '__path__', '__package__',
             '__project__', '__version__'))
        return result


# keep a reference to this module so that it's not garbage collected
old_module = sys.modules['segeval']


# setup the new module and patch it into the dict of loaded modules
new_module = sys.modules['segeval'] = module('segeval')
new_module.__dict__.update({
    '__file__':             __file__,
    '__path__':             __path__,
    '__package__':          __package__,
    '__project__':          __project__,
    '__doc__':              __doc__,
    '__version__':          __version__,
    '__version_number__':   __version_number__,
    '__author__':           __author__,
    '__author_email__':     __author_email__,
    '__copyright__':        __copyright__,
    '__all__':              tuple(object_origins),
    '__docformat__':        'restructuredtext en',
    '__description__':      __description__
})
