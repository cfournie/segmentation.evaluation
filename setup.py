#!/usr/bin/env python
'''
Setup script for installing the segeval package.

.. moduleauthor:: Chris Fournier <chris.m.fournier@gmail.com>
'''
import sys
import os

try:
    from setuptools import setup
    extra = dict(test_suite="segeval", include_package_data=True)
except ImportError:
    from distutils.core import setup
    extra = {}

from segeval import __package__, __version__, __author__, __author_email__, __description__

packages=['segeval',
          'segeval.agreement',
          'segeval.data',
          'segeval.ml',
          'segeval.similarity',
          'segeval.similarity.distance',
          'segeval.util',
          'segeval.window']

setup(
    name=__package__,
    version=__version__,
    long_description=open('README.rst').read(),
    description=__description__,
    license=open('LICENSE').read(),
    author=__author__,
    author_email=__author_email__,
    url='http://segeval.readthedocs.org/',
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Development Status :: 5 - Production/Stable',
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
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3'],
      platforms = ['Any'],
      keywords = ['segmentation', 'similarity', 'discourse'],
      packages=packages,
      **extra)
