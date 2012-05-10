'''
Setup script for installing the segeval package.

.. codeauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from distutils.core import setup
setup(name='segeval',
      version='1.0.0',
      description='Segmentation Evaluation Metrics',
      author='Chris Fournier',
      author_email='chris.m.fournier@gmail.com',
      url='http://nlp.chrisfournier.ca/software/',
      download_url = 'https://github.com/cfournie/segmentation.evaluation',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering :: Artificial Intelligence',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                   'Topic :: Text Processing',
                   'Topic :: Utilities'],
      packages=['segeval',
                'segeval.data',
                'segeval.ml',
                'segeval.agreement',
                'segeval.similarity',
                'segeval.similarity.distance',
                'segeval.window']
      )
    