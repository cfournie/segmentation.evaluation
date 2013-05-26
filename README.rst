SegEval v2.0
============

.. image:: https://travis-ci.org/cfournie/segmentation.evaluation.png?branch=experimental
        :target: https://travis-ci.org/cfournie/segmentation.evaluation


SegEval is a BSD Licensed library for evaluating text segmentation.
Text segmentation is the task of splitting up text by placing boundaries within it according to some subjective criterion.
SegEval provides a variety of comparison methods and inter-coder agreement coefficients for segmentation as both APIs and a `CLI <http://packages.python.org/segeval/#commandline-usage>`_.

Some metrics provided include: **Boundary Similarity (B)** `(Fournier, 2013) <http://nlp.chrisfournier.ca/publications/#mascthesis>`_; **Segmentation Similarity (S)** `(Fournier and Inkpen, 2012) <http://arxiv.org/abs/1204.2847>`_; **WindowDiff**; **Pk**; and others.

Additionally, inter-coder agreement coefficients that are based upon B for both 2 and more coders are provided, including: **Kappa**; and **Pi**.

For more details, see the `manual <http://packages.python.org/segeval/>`_.


Installation
------------

Requires `Python 2.7+ <http://www.python.org/download/releases/2.7/>`_; to install segeval, use:

.. code-block:: bash

    $ pip install segeval

Or, run ``git clone`` and ``make install``.



Testing
-------

To compile and test, use:

.. code-block:: bash

    $ make test

Or, for output of test coverage, use:

.. code-block:: bash

    $ make coverage



Support
-------

If you have any suggestions, problems, or difficulties, please `log an issue <https://github.com/cfournie/segmentation.evaluation/issues>`_, or `contact me <http://nlp.chrisfournier.ca/about/>`_.


Citing
------
If you're using this software for research, please cite `the ACL paper <(http://nlp.chrisfournier.ca/publications/>`_ and `thesis <http://nlp.chrisfournier.ca/publications/#mascthesis>`_ describing this work:

- *Chris Fournier. 2013. Evaluating Text Segmentation using Boundary Edit Distance. Proceedings of 51st Annual Meeting of the Association for Computational Linguistics. (ACL 2013), to appear. Association for Computational Linguistics, Stroudsburg, PA, USA.*

- *Chris Fournier. 2013. Evaluating Text Segmentation. (Master's thesis). University of Ottawa.*

- *Chris Fournier and Diana Inkpen. 2012. Segmentation Similarity and Agreement. Proceedings of Human Language Technologies: The 2012 Annual Conference of the North American Chapter of the Association for Computational Linguistics. (HLT '12), pp. 152—161. Association for Computational Linguistics, Stroudsburg, PA, USA.*


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

	@inproceedings{FournierInkpen2012,
		author		= {Fournier, Chris and Inkpen, Diana},
		title		= {{Segmentation Similarity and Agreement}},
		booktitle	= {Human Language Technologies: The 2012 Annual Conference of the North American Chapter of the Association for Computational Linguistics},
		series		= {HLT '12},
		year		= {2012},
		location	= {Montr\'eal, Quebec, Canada},
		pages		= {152--161},
		numpages	= {10},
		publisher	= {Association for Computational Linguistics},
		address		= {Stroudsburg, PA, USA}
	}
