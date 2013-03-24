#!/usr/bin/env python
'''
Setup script for installing the segeval package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import sys
import os

try:
    from setuptools import setup
    extra = dict(test_suite="tests.test.suite", include_package_data=True)
except ImportError:
    from distutils.core import setup
    extra = {}

if sys.argv[-1] is 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

from segeval import __version__

requires = ['numpy>=1.6.0']

packages=['segeval',
          'segeval.agreement',
          'segeval.data',
          'segeval.ml',
          'segeval.similarity',
          'segeval.similarity.distance',
          'segeval.window']

setup(
    name='segeval',
    version=__version__,
    long_description=open("./README.rst", "r").read(),
    description='A package and utilities providing a variety of discourse segmentation evaluation metrics',
    license=open('LICENSE').read(),
    author='Chris Fournier',
    author_email='chris.m.fournier@gmail.com',
    url='http://pypi.python.org/pypi/segeval/',
    install_requires = requires,
    zip_safe=True,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'Natural Language :: English',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Scientific/Engineering :: Information Analysis',
                 'Topic :: Text Processing',
                 'Topic :: Utilities',
                 'Programming Language :: Python :: 2.7'],
      platforms = ['Any'],
      keywords = ['segmentation', 'similarity', 'discourse'],
      data_files=[('segeval/data', ['segeval/data/complete_agreement.json',
                                    'segeval/data/hearst1997_positions.csv',
                                    'segeval/data/hearst1997.json',
                                    'segeval/data/hearst1997.tsv',
                                    'segeval/data/large_disagreement.json'])],
      packages=packages,
      **extra)
