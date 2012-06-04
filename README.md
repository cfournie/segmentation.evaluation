SegEval v1.0 beta
=================

This package is a collection of metrics and a [command-line interface](http://packages.python.org/segeval/#commandline-usage) for evaluating segmentation. A variety of metrics are provided, including:

- Segmentation Similarity (S) [(Fournier and Inkpen, 2012)](http://nlp.chrisfournier.ca/publications/#segmentation);
- WindowDiff;
- Pk; and others.

Additionally, inter-coder agreement coefficients that are based upon S for both 2 and more coders are provided, including:

- Kappa; and
- Pi.

For more details, see the manual at http://packages.python.org/segeval/

If you're using this software for research, please cite:

*Chris Fournier and Diana Inkpen. 2012. Segmentation Similarity and Agreement. Proceedings of Human Language Technologies: The 2012 Annual Conference of the North American Chapter of the Association for Computational Linguistics. (HLT '12), pp. 152—161. Association for Computational Linguistics, Stroudsburg, PA, USA.*

If you would like to read the paper, [visit my website](http://nlp.chrisfournier.ca/publications/#segmentation).

```
@inproceedings{FournierInkpen2012,
	author		= {Chris Fournier and Diana Inkpen},
	title		= {Segmentation Similarity and Agreement},
	booktitle	= {Human Language Technologies: The 2012 Annual Conference of the North American Chapter of the Association for Computational Linguistics},
	series		= {HLT '12},
	year		= {2012},
	location	= {Montreal, Quebec, Canada},
	pages		= {152--161},
	numpages	= {10},
	publisher	= {Association for Computational Linguistics},
	address		= {Stroudsburg, PA, USA}
}
```

Requirements
------------
- [Python 2.7+](http://www.python.org/)


Directories
-----------
- /doc/  - Sphinx auto-documentation code
- /src/  - Source code (Python 2.7)