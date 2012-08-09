'''
Setup script for installing the segeval package.

.. codeauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
from distutils.core import setup
setup(name='segeval',
      version='1.1 beta',
      
      description='A package and utilities providing a variety of discourse \
segmentation evaluation metrics',
      
      author='Chris Fournier',
      author_email='chris.m.fournier@gmail.com',
      
      maintainer='Chris Fournier',
      maintainer_email='chris.m.fournier@gmail.com',
      
      url='http://pypi.python.org/pypi/segeval/',
      download_url = 'http://pypi.python.org/packages/source/s/segeval/segeval\
-1.1%20beta.tar.gz',
      
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
      
      platforms = ('Any'),
      
      keywords = ('segmentation', 'similarity', 'discourse'),
      
      data_files=[('segeval/data', ['segeval/data/complete_agreement.json',
                                    'segeval/data/hearst1997_positions.csv',
                                    'segeval/data/hearst1997.json',
                                    'segeval/data/hearst1997.tsv',
                                    'segeval/data/large_disagreement.json'])],
      
      packages=['segeval',
                'segeval.agreement',
                'segeval.data',
                'segeval.ml',
                'segeval.similarity',
                'segeval.similarity.distance',
                'segeval.window'])
    
