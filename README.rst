SegEval v2.0
============

.. image:: https://travis-ci.org/cfournie/segmentation.evaluation.png?branch=experimental
        :target: https://travis-ci.org/cfournie/segmentation.evaluation

Text segmentation is the task of splitting up any amount of text into segments by placing boundaries between some atomic unit (e.g., morphemes, words, lines, sentences, paragraphs, sections, etc.).

This package is a collection of metrics and for comparing text segmentations and evaluating automatic text segmenters.  Both new (**Boundary Similarity**, **Segmentation Similarity**) and traditional (**WindowDiff**, **Pk**) are included, as well as inter-coder agreement coefficients and confusion matrices based upon a boundary edit distance.


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

* Fleiss' :math:`\pi` [Fleiss1971]_ (i.e., Siegel and Castellan's :math:`K` [SiegelCastellan1988]_)
* Fleiss' :math:`\kappa` [DaviesFleiss1982]_


Installation
------------

To install SegEval, simply:

.. code-block:: bash

    $ pip install segeval


Documentation
-------------

Documentation is available at http://segeval.readthedocs.org/.


Citing
------
If you're using this software for research, please cite `the ACL paper <(http://nlp.chrisfournier.ca/publications/>`_ and, if you need to go into details, the `thesis <http://nlp.chrisfournier.ca/publications/#mascthesis>`_ describing this work:

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
