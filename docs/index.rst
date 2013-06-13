Segmentation Evaluation using SegEval
=====================================

Text segmentation is the task of splitting up any amount of text into segments by placing boundaries between some atomic unit (e.g., morphemes, words, lines, sentences, paragraphs, sections, etc.).

This package is a collection of metrics and for comparing text segmentations and evaluating automatic text segmenters.  Both new (**Boundary Similarity**, **Segmentation Similarity**) and traditional (**WindowDiff**, **Pk**) are included, as well as inter-coder agreement coefficients and confusion matrices based upon a boundary edit distance.

:Release: |release|
:Date: |today|

Feature Support
---------------
Included is a variety of segmentation comparison metrics, including:

* Boundary Edit Distance (BED; [Fournier2013]_)
* Boundary Similarity (B; [Fournier2013]_)
* BED-based confusion matrices (and precision/recall/F1; [Fournier2013]_)
* Segmentation Similarity (S; [FournierInkpen2012]_)
* WindowDiff [PevznerHearst2002]_
* Pk [BeefermanBerger1999]_

Additionally, B-based inter-coder agreement coefficients for segmentation that are suitable for 2 or more coders are provided, including:

* Fleiss' :math:`\pi` [Fleiss1971]_ (i.e., Siegel and Castellan's :math:`K` [SiegelCastellan1988]_)
* Fleiss' :math:`\kappa` [DaviesFleiss1982]_


User Guide
----------

This part of the documentation, which is mostly prose, begins with some
background information about Requests, then focuses on step-by-step
instructions for getting the most out of Requests.

.. toctree::
   :maxdepth: 2

   user/intro
   user/install
   user/quickstart


API Documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api


Support
-------
If you have any suggestions, problems, or difficulties, please `log an issue <https://github.com/cfournie/segmentation.evaluation/issues>`_, or `contact me <http://nlp.chrisfournier.ca/about/>`_.



Citing
------
If you're using this software for research, please cite `the ACL paper [Fournier2013]_ and, if you need to go into details, the thesis [Fournier2013b]_ describing this work.

BibTeX:

.. code-block:: latex

    @inproceedings{Fournier2013a,
        author      = {Fournier, Chris},
        year        = {2013},
        title       = {{Evaluating Text Segmentation using Boundary Edit Distance}},
        booktitle   = {Proceedings of 51st Annual Meeting of the Association for Computational Linguistics},
        publisher   = {Association for Computational Linguistics},
        location    = {Sophia, Bulgaria},
        pages       = {to appear},
        address     = {Stroudsburg, PA, USA}
    }

    @mastersthesis{Fournier2013b,
        author      = {Fournier, Chris},
        title       = {Evaluating Text Segmentation},
        school      = {University of Ottawa},
        year        = {2013}
    }


References
----------

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


.. [Fournier2013] Chris Fournier. 2013. **Evaluating Text Segmentation using \
    Boundary Edit Distance**. Proceedings of the 51st Annual Meeting of the \
    Association for Computational Linguistics. Association for Computational \
    Linguistics. **To appear**.


.. [Fournier2013b] Chris Fournier. 2013. **Evaluating Text Segmentation**. Master's Thesis.  University of Ottawa.


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

.. [Scott1955] William A. Scott. 1955. **Reliability of content analysis: The \
    case of nominal scale coding**. Public Opinion Quarterly, 19(3):321-325.

.. [SiegelCastellan1988] Sidney Siegel and N. John Castellan, Jr. 1988. \
    **Non-parametric Statistics for the Behavioral Sciences**. 2nd Edition, \
    Castellanhapter 9.8. McGraw-Hill.

