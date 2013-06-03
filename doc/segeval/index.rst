Segmentation Evaluation using SegEval
*************************************

This package is a collection of metrics and a `command-line interface <usage>`_ for evaluating segmentation.  A variety of metrics are provided, including: **Segmentation Similarity (S)** [FournierInkpen2012]_; **WindowDiff**; **Pk**; and others.

Additionally, inter-coder agreement coefficients that are based upon S for both 2 and more coders are provided, including: **Kappa**; and **Pi**.

:Release: |release|
:Date: |today|

Additional manual entries include:

.. toctree::
   :maxdepth: 1

   usage
   install


Installation
============

Install for `Python 2.7 <http://www.python.org/download/>`_ using `distutils <http://pypi.python.org/pypi/setuptools>`_ (``easy_install segeval``) `pip <http://pypi.python.org/pypi/pip>`_ (``pip install segeval``). Alternatively, clone the repository from::

  git clone git://github.com/cfournie/segmentation.evaluation.git

If you encounter any issues, view the `detailed installation instructions <install>`_.


Usage
=====

To begin to use the module as a utility, from a terminal, enter::

  python -m segeval -h

Ouput is given either as TSV files or to the screen::

  python -m segeval s hearst1997.json 

  S 
    mean    = 0.7619047619047619047619047619  (macro)
    std     = 0.07055015423823358837798727192
    var     = 0.004977324263038548752834467119
    stderr  = 0.01539530581369118988034410932 (n=21)

For more usage (via command line and programmatically), see the `detailed usage examples <usage>`_.


Publications
============

If you're using this software for research, please cite `the paper <http://nlp.chrisfournier.ca/publications/#segmentation>`_:

  Chris Fournier and Diana Inkpen. 2012. **Segmentation Similarity and Agreement**. Proceedings of Human Language Technologies: The 2012 Annual Conference of the North American Chapter of the Association for Computational Linguistics. (HLT '12), pp. 152—161. Association for Computational Linguistics, Stroudsburg, PA, USA.


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


Support
=======

If you have any suggestions, problems, or difficulties, please `log an issue <https://github.com/cfournie/segmentation.evaluation/issues>`_, or `contact me <http://nlp.chrisfournier.ca/about/>`_.


Roadmap
=======

For a roadmap of planned features and future work see the `SegEval overview page <http://nlp.chrisfournier.ca/software/segeval/>`_.


Input Data Formats
==================

SegEval reads data in JSON (JavaScript Object Notation) or TSV (Tab Separated Values) formats as specified in the `Segmentation Representation Specification Version 1.1 <http://nlp.chrisfournier.ca/publications/pdf/fournier_segeval_spec_2012.pdf>`_ (PDF).

For mutliply-coded data examples, see the `Segmentation Corpora github repository <https://github.com/cfournie/segmentation.corpora>`_.


Licenses
========
This software is licensed under the `BSD 3-Clause free software license <http://www.opensource.org/licenses/BSD-3-Clause>`_.

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

