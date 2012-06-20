Segmentation Evaluation using segeval
*************************************

This package is a collection of metrics and a `command-line interface <#commandline-usage>`_ for evaluating segmentation.  A variety of metrics are provided, including:

* Segmentation Similarity (S) [FournierInkpen2012]_;
* WindowDiff;
* Pk; and others.

Additionally, inter-coder agreement coefficients that are based upon S for both 2 and more coders are provided, including:

* Kappa; and
* Pi.

If you have any suggestions, problems, or difficulties, please `log an issue <https://github.com/cfournie/segmentation.evaluation/issues>`_, or `contact me <http://nlp.chrisfournier.ca/about/>`_. For a roadmap of planned features and future work see my `page on SegEval <http://nlp.chrisfournier.ca/software/>`_.

:Release: |version| (beta)
:Date: |today|

If you're using this software for research, please cite:

*Chris Fournier and Diana Inkpen. 2012. Segmentation Similarity and Agreement. Proceedings of Human Language Technologies: The 2012 Annual Conference of the North American Chapter of the Association for Computational Linguistics. (HLT '12), pp. 152—161. Association for Computational Linguistics, Stroudsburg, PA, USA.*

If you would like to read the paper, `visit my website <http://nlp.chrisfournier.ca/publications/#segmentation>`_.

BibTeX::

  @InProceedings{FournierInkpen2012,
    author    = {Fournier, Chris  and  Inkpen, Diana},
    title     = {Segmentation Similarity and Agreement},
    booktitle = {Proceedings of the 2012 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies},
    month     = {June},
    year      = {2012},
    address   = {Montr\'{e}al, Canada},
    publisher = {Association for Computational Linguistics},
    pages     = {152--161},
    url       = {http://www.aclweb.org/anthology/N/N12/N12-1016}
  }


Installation
============

Requirements:

* `Python 2.7 <http://www.python.org/download/>`_
* Recommended: `setuptools0.6c11 <http://pypi.python.org/pypi/setuptools>`_ or `pip <http://pypi.python.org/pypi/pip>`_ (either is required to effortlessly install)


Mac OSX and Linux
-----------------

Verifying Requirements
++++++++++++++++++++++

First let's verify that you have all of the requirements setup. Let's check for the right version of python.  Open up your terminal and enter::

  which python

It should output some string that contains the number ``2.7`` in it, much like::
  
  /Library/Frameworks/Python.framework/Versions/2.7/bin/python

Now type::

  python --version

You should see a version string returned that contains the number ``2.7`` in it, much like::

  Python 2.7.3

Now let's try to see whether ``setuptools`` is installed; type::

  which easy_install

It should return a path that matches (except for the text after ``/bin/``) the output of the earlier call to ``which python``::

  /Library/Frameworks/Python.framework/Versions/2.7/bin/easy_install


Installing
++++++++++

After installing the required packages, open up your terminal and enter::
  
  sudo easy_install segeval

Or, if you are using pip, open up your terminal and enter::
  
  sudo pip segeval

To verify that it worked, type::

  python -m segeval

It should complain by saying::

  usage: segeval [-h] {pi,k,b,f,r,p,pr,s,pk,wd,wpr} ...
  segeval: error: too few arguments

If that worked, then you're done; enjoy!


Windows
-------

Verifying Requirements
++++++++++++++++++++++

First let's verify that you have all of the requirements setup. Let's check for the right version of python.  Open up your terminal and enter::

  python --version

You should see a version string returned that contains the number ``2.7`` in it, much like::

  Python 2.7.3


Installing
++++++++++

Open up a command prompt and run::

  easy_install segeval

Or, if you are using pip, open up your terminal and enter::
  
  sudo pip segeval

To verify that it worked, type::

  python -m segeval

It should complain by saying::

  usage: segeval [-h] {pi,k,b,f,r,p,pr,s,pk,wd,wpr} ...
  segeval: error: too few arguments

If that worked, then you're done; enjoy!


Source Install
--------------

To install from source, `download or clone the source code repository from github <https://github.com/cfournie/segmentation.evaluation>`_, extract it, and navigate to the ``src/python/main`` directory and run::
  
  python setup.py install

To verify that it worked, type::

  python -m segeval

It should complain by saying::

  usage: segeval [-h] {pi,k,b,f,r,p,pr,s,pk,wd,wpr} ...
  segeval: error: too few arguments

If that worked, then you're done; enjoy!


.. _commandline-usage:

Commandline usage
=================

From a terminal, use::

  python -m segeval -h

This will present you with the available options::

  usage: segeval [-h] {pi,k,b,f,r,p,pr,s,pk,wd,wpr} ...

  A discourse segmentation evaluation utility.

  optional arguments:
    -h, --help            show this help message and exit

  metric:
    Calculates a specified segmentation evaluation metric upon provided data

    {pi,k,b,f,r,p,pr,s,pk,wd,wpr}
                          Available metrics
      pi                  S-based Fleiss' Multi Pi
      k                   S-based Fleiss' Multi Kappa
      b                   S-based Artstein and Poesio's (2008) Bias
      f                   Pairwise Mean F_beta Measure
      r                   Pairwise Mean Recall
      p                   Pairwise Mean Precision
      pr                  Pairwise Mean Percentage
      s                   Mean S
      pk                  Mean Pk
      wd                  Mean WindowDiff
      wpr                 Mean WinPR

From here, you can ask for more detailed help for a specific metric, such as ``S``::

  python -m segeval s -h

It's usage has the following options::

  usage: segeval s [-h] [-o OUTPUT] [-f {tsv,json}] [-d DELIMITER] [-n N]
                   [-wt WT] [-ws WS] [-te TE] [-de]
                   input

  positional arguments:
    input                 Input file or directory

  optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                          Output file or directory. If not specified, a summary
                          or results is printed to the console.
    -f {tsv,json}, --format {tsv,json}
                          Input file format; default is json
    -d DELIMITER, --delimiter DELIMITER
                          Delimiting character for input TSV files; ignored if
                          JSON is specified, default is a tab character
    -n N                  The maximum number of PBs that boundaries can span to
                          be considered transpositions (n<2 means no
                          transpositions); default is 2.
    -wt WT                Weight, 0 <= wt <= 1, to scale transposition error by;
                          default is 1 (no scaling).
    -ws WS                Weight, 0 <= wt <= 1, to scale substitution error by;
                          default is 1 (no scaling).
    -te TE                Scale transpositions by their size and the number of
                          boundaries the span; True by default
    -de, --detailed       When specifying an output TSV file, specify this to
                          obtain a detailed error breakdown per edit

There are two modes of output:

* Screen output (default); and
* TSV (Tab Separated Values) file output (enabled by specifying an output file using ``-o OUTPUT``)

Screen outputis very minimal, but will often give you the quick values that you need.  The TSV output is meant for being passed into `R <http://www.r-project.org/>`_, or another statistical package, and contains detailed values per pair of coders/item.

For screen output, if you have some `sample data <https://github.com/cfournie/segmentation.corpora>`_, you can run::

  python -m segeval s hearst1997.json 

Which produces::

  S 
    mean  = 0.7619047619047619047619047619
    std = 0.07055015423823358837798727192
    var = 0.004977324263038548752834467119
    stderr  = 0.01539530581369118988034410932


Input Data Formats
==================

SegEval reads data in JSON (JavaScript Object Notation) or TSV (Tab Separated Values) formats as specified in the `Segmentation Representation Specifcation Version 0.1 <http://nlp.chrisfournier.ca/publications/pdf/fournier_segeval_spec_2012.pdf>`_ (PDF).

For mutliply-coded data examples, see the `Segmentation Corpora <https://github.com/cfournie/segmentation.corpora>`_ repository.


Programmatic usage
==================

Programmatic usage of the module can be done using Python.  The stable set of APIs are listed below in the modules section.

Modules
-------

.. toctree::
   :maxdepth: 1

   segeval
   segeval.data
   segeval.ml
   segeval.agreement
   segeval.similarity
   segeval.similarity.distance
   segeval.window


Licenses
========
This software is licensed under the `BSD 3-Clause free software license <http://www.opensource.org/licenses/BSD-3-Clause>`_::

    Copyright (c) 2011-2012, Chris Fournier
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.
        * Neither the name of the author nor the names of its contributors may
          be used to endorse or promote products derived from this software
          without specific prior written permission.
          
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

All data and documents not in software form are licensed under the `Creative Commons Attribution-ShareAlike 2.5 Canada (CC BY-SA 2.5) <http://creativecommons.org/licenses/by-sa/2.5/ca/>`_ license.


References
==========

.. [ArtsteinPoesio2008] Ron Artstein and Massimo Poesio. 2008. **Inter-coder \
    agreement for computational linguistics**. Computational Linguistics, \
    4(4):555-596. MIT Press.

.. [Baker1990]  David Baker. 1990. **Stargazers look for life**. South \
    Magazine 117, 76–77. South Publications.

.. [BeefermanBerger1999] Doug Beeferman and Adam Berger. 1999. **Statistical \
    models for text segmentation**. Machine learning, 34(1–210. Springer \
    Netherlands.

.. [Cohen1960] Jacob Cohen. 1960. **A Coefficient of Agreement for Nominal \
    Scales**. Educational and Psychological Measurement, 20(1):37-46.

.. [Collins1868] Wilkie Collins. 1868. **The Moonstone**. Tinsley Brothers.
    
.. [DaviesFleiss1982] Mark Davies and Joseph L. Fleiss. 1982. **Measuring \
    agreement for multinomial data**. Biometrics, 38(4):1047-1051.

.. [Fleiss1971] Joseph L. Fleiss. 1971. **Measuring nominal scale agreement \
    among many raters**. Psychological Bulletin, 76(5):378-382.

.. [FournierInkpen2012] Chris Fournier and Diana Inkpen. 2012. **Segmentation \
    Similarity and Agreement**. Proceedings of Human Language Technologies: The \
    2012 Annual Conference of the North American Chapter of the Association for \
    Computational Linguistics. (HLT '12). Association for Computational \
    Linguistics.

.. [Hearst1997] Marti A. Hearst. 1997. **TextTiling: Segmenting Text into \
    Multi-paragraph Subtopic Passages**. Computational Linguistics, 23(1):33-64.

.. [KazantsevaSzpakowicz2012] Kazantseva, A. & Szpakowicz, S. (2012), **Topical\
    segmentation: a study of human performance**. Proceedings of Human Language \
    Technologies: The 2012 Annual Conference of the North American Chapter of the \
    Association for Computational Linguistics. (HLT '12). Association for \
    Computational Linguistics.

.. [LamprierEtAl2007] Sylvain Lamprier, Tassadit Amghar, Bernard Levrat, and \
    Frederic Saubion 2007. **On evaluation methodologies for text \
    segmentation algorithms**. Proceedings of the 19th IEEE International \
    Conference on Tools with Arificial Intelligence, 2:19–26. IEEE \
    Computer Society.

.. [PevznerHearst2002] Lev Pevzner and Marti A. Hearst. 2002. **A critique \
    and improvement of an evaluation metric for text segmentation**. \
    Computational Linguistics, 28(1):19–36. MIT Press, Cambridge, MA, USA.

.. [ScaianoInkpen2012] Martin Scaiano and Diana Inkpen. 2012, **Getting more \
    from segmentation evaluation**, in Proceedings of Human Language \
    Technologies: The 2012 Annual Conference of the North American Chapter of \
    the Association for Computational Linguistics, Association for \
    Computational Linguistics.

.. [Scott1955] William A. Scott. 1955. **Reliability of content analysis: The \
    case of nominal scale coding**. Public Opinion Quarterly, 19(3):321-325.

.. [SiegelCastellan1988] Sidney Siegel and N. John Castellan, Jr. 1988. \
    **Non-parametric Statistics for the Behavioral Sciences**. 2nd Edition, \
    Castellanhapter 9.8. McGraw-Hill.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

