SegEval v2.0
============

.. image:: https://badge.fury.io/py/segeval.png
    :target: https://preview-pypi.python.org/project/segeval/
.. image:: https://travis-ci.org/cfournie/segmentation.evaluation.png?branch=master
	:target: https://travis-ci.org/cfournie/segmentation.evaluation
.. image:: https://coveralls.io/repos/cfournie/segmentation.evaluation/badge.png?branch=master
	:target: https://coveralls.io/r/cfournie/segmentation.evaluation?branch=master

|

Text segmentation is the task of splitting up any amount of text into segments by placing boundaries between some atomic unit (e.g., morphemes, words, lines, sentences, paragraphs, sections, etc.).  It's a common pre-processing step in many `Natural Language Processing (NLP) <http://en.wikipedia.org/wiki/Natural_language_processing>`_ tasks.

This package is a collection of metrics and for comparing text segmentations and evaluating automatic text segmenters.  Both new (**Boundary Similarity**, **Segmentation Similarity**) and traditional (**WindowDiff**, **Pk**) are included, as well as inter-coder agreement coefficients and confusion matrices based upon a boundary edit distance.

To see some examples of its usage, `read the docs <http://segeval.readthedocs.org/>`_.


Feature Support
---------------
Included is a variety of segmentation comparison metrics, including:

* Boundary Edit Distance (BED)
* Boundary Similarity (B)
* BED-based confusion matrices (and precision/recall/F1)
* Segmentation Similarity (S)
* WindowDiff
* Pk

Additionally, B-based inter-coder agreement coefficients for segmentation that are suitable for 2 or more coders are provided, including:

* Fleiss' Pi (i.e., Siegel and Castellan's K)
* Fleiss' Kappa


Installation
------------

To install SegEval, simply run:

.. code-block:: bash

    $ pip install segeval


Documentation
-------------

Documentation is available at http://segeval.readthedocs.org/.


Citing SegEval
--------------
If you're using this software for research, please cite the `ACL paper <http://nlp.chrisfournier.ca/publications/pdf/fournier_2013a.pdf>`_ [PDF] and, if you need to go into details, the `thesis <http://nlp.chrisfournier.ca/publications/pdf/fournier_masc_thesis.pdf>`_ [PDF] describing this work:

- *Chris Fournier. 2013. Evaluating Text Segmentation using Boundary Edit Distance. Proceedings of 51st Annual Meeting of the Association for Computational Linguistics. (ACL 2013), to appear. Association for Computational Linguistics, Stroudsburg, PA, USA.*

- *Chris Fournier. 2013. Evaluating Text Segmentation. (Master's thesis). University of Ottawa.*

BibTeX:

.. code-block:: latex

	@inproceedings{Fournier2013a,
		author		= {Fournier, Chris},
		year		= {2013},
		title		= {{Evaluating Text Segmentation using Boundary Edit Distance}},
		booktitle	= {Proceedings of 51st Annual Meeting of the Association for Computational Linguistics},
		publisher	= {Association for Computational Linguistics},
		location	= {Sophia, Bulgaria},
		pages		= {to appear},
		address		= {Stroudsburg, PA, USA}
	}

	@mastersthesis{Fournier2013b,
		author		= {Fournier, Chris},
		title		= {Evaluating Text Segmentation},
		school		= {University of Ottawa},
		year		= {2013}
	}
