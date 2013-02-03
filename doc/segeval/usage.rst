Using SegEval
*************

SegEval can be used via the command line, or programmatically.


Command-line usage
==================

From a terminal, SegEval can be used by calling the python executable with the ``-m`` option and specifying the ``segeval`` module using::

  python -m segeval


There are two modes of output:

* Screen output (default); and
* TSV file output (enabled by specifying an output file using ``-o OUTPUT``)

Screen output is very minimal, but will often give you the quick values that you need.  The TSV output is meant for being passed into `R <http://www.r-project.org/>`_, or another statistical package, and contains detailed values per pair of coders/item.


Help
----

From a terminal, use::

  python -m segeval -h


This will present you with the available options::

  usage: segeval [-h] {pi,k,b,f,r,p,pr,s,s-ml,pk,wd,wpr,merge} ...

  A discourse segmentation evaluation utility.

  optional arguments:
    -h, --help            show this help message and exit

  metric:
    Calculates a specified segmentation evaluation statistics/performs an
    operation upon provided data.

    {pi,k,b,f,r,p,pr,s,s-ml,pk,wd,wpr,merge}
                          Available metrics/operations
      pi                  S-based Fleiss' Multi Pi coefficient
      k                   S-based Fleiss' Multi Kappa coefficient
      b                   S-based Artstein and Poesio's (2008) Bias value
      f                   Pairwise Mean F_beta measure (permuted)
      r                   Pairwise Mean Recall value (permuted)
      p                   Pairwise Mean Precision value (permuted)
      pr                  Pairwise Mean Percentage metric
      s                   Mean S metric
      s-ml                S-based information retrieval metrics including:
                          precision, recall, and F_beta measure
      pk                  Mean Pk value (permuted)
      wd                  Mean WindowDiff value (permuted)
      wpr                 Mean WinPR value
      merge               Merge segmentations operation


From here, you can ask for more detailed help for a specific metric, such as ``S``::

  python -m segeval s -h

It's usage has the following options::

  usage: segeval s [-h] [-f {tsv,json}] [-d DELIMITER] [-o OUTPUT] [-n N]
                 [-wt WT] [-ws WS] [-te TE] [-m] [-de]
                 input

  positional arguments:
    input                 Input file or directory

  optional arguments:
    -h, --help            show this help message and exit
    -f {tsv,json}, --format {tsv,json}
                          Input file format; default is json
    -d DELIMITER, --delimiter DELIMITER
                          Delimiting character for input TSV files; ignored if
                          JSON is specified, default is a tab character
    -o OUTPUT, --output OUTPUT
                          Output file or directory. If not specified, a summary
                          or results is printed to the console.
    -n N                  The maximum number of PBs that boundaries can span to
                          be considered transpositions (n<2 means no
                          transpositions); default is 2.
    -wt WT                Weight, 0 <= wt <= 1, to scale transposition error by;
                          default is 1 (no scaling).
    -ws WS                Weight, 0 <= wt <= 1, to scale substitution error by;
                          default is 1 (no scaling).
    -te TE                Scale transpositions by their size and the number of
                          boundaries the span; True by default
    -m, --micro           Specifies that a micro mean is to be returned; default
                          is macro mean.
    -de, --detailed       When specifying an output TSV file, specify this to
                          obtain a detailed error breakdown per edit


Screen Output
-------------

For screen output, if you have some `sample data <https://github.com/cfournie/segmentation.corpora>`_, you can run::

  python -m segeval s hearst1997.json 

  S 
    mean    = 0.7619047619047619047619047619  (macro)
    std     = 0.07055015423823358837798727192
    var     = 0.004977324263038548752834467119
    stderr  = 0.01539530581369118988034410932 (n=21)


For a micro average, run::

  python -m segeval s -m hearst1997.json 

  S 
    mean  = 0.7619047619047619047619047619  (micro)


TSV Output
----------

When producing TSV output, run::

  python -m segeval s -o output.tsv hearst1997.json 


Which roduces a file called ``output.tsv``::

  label coder1  coder2  pbs_unedited  pbs_total sub_edits transp_edits  S
  stargazer 3 2 14  20  5 1 0.7
  stargazer 3 5 14  20  5 1 0.7
  stargazer 3 4 16  20  3 1 0.8
  stargazer 3 7 17  20  2 1 0.85
  stargazer 3 6 15  20  4 1 0.75
  stargazer 1 3 16  20  4 0 0.8
  stargazer 1 2 16  20  3 1 0.8
  stargazer 5 4 14  20  6 0 0.7
  stargazer 1 7 17  20  2 1 0.85
  stargazer 1 6 17  20  2 1 0.85
  stargazer 1 5 17  20  1 2 0.85
  stargazer 1 4 14  20  5 1 0.7
  stargazer 5 7 15  20  3 2 0.75
  stargazer 7 6 17  20  2 1 0.85
  stargazer 5 6 16  20  1 3 0.8
  stargazer 4 6 13  20  5 2 0.65
  stargazer 4 7 14  20  5 1 0.7
  stargazer 2 4 12  20  6 2 0.6
  stargazer 2 5 15  20  2 3 0.75
  stargazer 2 6 15  20  3 2 0.75
  stargazer 2 7 16  20  3 1 0.8


The columns are:

================  ===========
Column            Description
================  ===========
``label``         Item (i.e., document or group of coders) described.
``coder1``        One of two coders compared.
``coder2``        Other one of two coders compared.
``pbs_unedited``  Number of unedited potential boundary positions.
``pbs_total``     Number of total potential boundary positions.
``sub_edits``     Number of substitution edits performed.
``transp_edits``  Number of transposition edits performed.
``S``             Segmentation Similarity (S) value.
================  ===========


Programmatic usage
==================

The `Python 2.7 <http://www.python.org/download/>`_ source code is available on `github <http://cfournie.github.com/segmentation.evaluation/>`_ and documentation for a fariety of the stable APIs is described in for these modules:

.. toctree::
   :maxdepth: 1

   segeval
   segeval.data
   segeval.ml
   segeval.agreement
   segeval.similarity
   segeval.similarity.distance
   segeval.window
