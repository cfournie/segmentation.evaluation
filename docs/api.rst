.. _api:

.. module:: segeval

Developer Interface
===================
The APIs for most metrics can be provided either two segmentations to compare or a dataset to perform pairwise comparisons upon.
There are a variety of parameters that can be specified other than that which is compared, but all have defaults specified.


Boundary-Edit-Distance-based Metrics
------------------------------------
These segmentation comparison metrics were introduced in [Fournier2013]_.

.. autofunction:: boundary_statistics

    Computes a large number of BED-based and other segmentation statistics, returning a :func:`dict` that includes:
        * ``count_edits``, a count of BED edits;
        * ``additions``, a list of BED addition edits;
        * ``substitutions``, a list of BED substitution edits;
        * ``transpositions``, a list of BED transposition edits;
        * ``full_misses``, a list of fully-missed boundaries (regardless of edits);
        * ``boundaries_all``, a count of boundaries compared;
        * ``matches``, a list of matching boundaries;
        * ``pbs``, a count of potential boundary types.

.. class:: BoundaryFormat()

	An ``enum`` with options that include:
		* ``sets``, a boundary set string; see :func:`boundary_string_from_masses`
		* ``mass``, a tuple of segment masses; see :func:`convert_positions_to_masses`
		* ``position``, a tuple of position segment labels; see :func:`convert_masses_to_positions`


Boundary Similarity (B)
***********************
This metric compares the correctness of boundary pairs between segmentations [Fournier2013]_.

.. note:: This is a recommended segmentation comparison metric for situations when there is no reference segmentation to compare against; see [Fournier2013]_.

.. function:: boundary_similarity(segmentation_a, segmentation_b, **kwargs)

	:param segmentation_*: Segmentation or dataset containing segmentations of a particular format; see :class:`BoundaryFormat`
	:type segmentation_*: segmentation or :class:`Dataset`

.. function:: boundary_similarity(dataset, **kwargs)

	:param dataset: Dataset of segmentations
	:type dataset: :class:`Dataset`

.. function:: boundary_similarity

    :param boundary_format: Segmentation format; default ``BoundaryFormat.mass``
    :param permuted: Use pairwise permutations v.s. combinations; default ``False``
    :param one_minus: Return :math:`1-value`; default ``False``
    :param return_parts: Return tuples of numerators, demoninators, or other values comprising a metric; default ``False``
    :param n_t: See :func:`boundary_edit_distance`
    :param boundary_types: Set of allowewable boundary types; default ``set([1])``
    :param weight: Tuple of weighting functions, see :ref:`weightfunctions`; default is scaling of substitution and transposition but not addition edits (:func:`weight_a`, :func:`weight_s_scale`, :func:`weight_t_scale`)
    :type boundary_format: :class:`BoundaryFormat` enum
    :type permuted: bool
    :type one_minus: bool
    :type return_parts: bool
    :type n_t: int
    :type boundary_types: set
    :type weight: tuple


Segmentation Similarity (S)
***************************
Originally introduced in [FournierInkpen2012]_, this metric uses the revised boundary edit distance in [Fournier2013]_ and compares segmentations to provide the proportion of unedited potential boundary positions.

.. warning:: Prefer :func:`boundary_similarity` instead; see [Fournier2013]_.

.. function:: segmentation_similarity(segmentation_a, segmentation_b, **kwargs)

	For parameters see :func:`boundary_similarity`

.. function:: segmentation_similarity(dataset, **kwargs)

	For parameters see :func:`boundary_similarity`

.. function:: segmentation_similarity

	For parameters see :func:`boundary_similarity`


Boundary Edit Distance (BED)
****************************

An edit distance proposed in [Fournier2013]_ that operates upon boundaries to produce:
	
	* Additions/deletion edits to model full misses,
	* Transposition edits to model near misses, and 
	* Substitution edits to model boundary-type confusion.

For more details, see Section 3.1 of [Fournier2013b]_.

.. autofunction:: boundary_edit_distance


BED-based Confusion Matrix (BED-CM)
***********************************

A confusion-matrix-formulation proposed in [Fournier2013]_ that uses BED to populate a matrix by using matches and scaled transpositions as correct classifications for boundary types, substitutions as confusion between boundary types, and additions/deletions as missing boundary types.

.. note:: This is a recommended segmentation comparison metric, when summarized by an information-retrieval metric such as :func:`precision`, :func:`recall`, :func:`fmeasure`, etc., for situations when there is a reference segmentation to compare against; see [Fournier2013]_.

.. function:: boundary_confusion_matrix(hypothesis, reference, **kwargs)

	:param segmentation_*: Segmentation of a particular format; see :class:`BoundaryFormat`
	:type segmentation_*: segmentation

.. function:: boundary_confusion_matrix(dataset, **kwargs)

	:param dataset: Dataset of segmentations
	:type dataset: :class:`Dataset`

.. autofunction:: boundary_confusion_matrix


.. _weightfunctions:

Weighting Functions
*******************

These functions are used by BED-based metrics to weight edit operations.  

.. autofunction:: weight_a

.. autofunction:: weight_s

.. autofunction:: weight_s_scale

.. autofunction:: weight_t

.. autofunction:: weight_t_scale



Traditional Metrics
-------------------

.. autofunction:: compute_window_size


Pk
**
Proposed in [BeefermanBerger1999]_, this segmentation comparison metric runs a window over a hypothesis and reference segmentation and counts those hypothesis windows whose ends are in differing segmentations that do not agree with the reference window as being in error.  These errors are then summed over all windows.

.. warning:: Prefer :func:`boundary_similarity` instead; see [Fournier2013]_.

.. function:: pk(hypothesis, reference, **kwargs)

	:param hypothesis: Hypothetical, or automatically-generated, segmentation (or dataset of segmentations) of a particular format; see :class:`BoundaryFormat`
	:param reference: Reference, or manually-created, segmentation (or dataset of segmentations) of a particular format; see :class:`BoundaryFormat`
	:type hypothesis: segmentation or :class:`Dataset`
	:type reference: segmentation or :class:`Dataset`

.. function:: pk(dataset, **kwargs)

	:param dataset: Dataset of segmentations
	:type dataset: :class:`Dataset`

.. function:: pk

    :param boundary_format: Segmentation format; default ``BoundaryFormat.mass``
    :param permuted: Use pairwise permutations v.s. combinations; default ``True``
    :param one_minus: Return :math:`1-value`; default ``False``
    :param return_parts: Return tuples of numerators, demoninators, or other values comprising a metric; default ``False``
    :param window_size: Overriding window size -- if not ``None``, this replaces the per-comparison window size computed using :func:`compute_window_size` as the window size used; default ``None``
    :param fnc_round: Rounding function used when computing window size, see :func:`compute_window_size`; default :func:`round`
    :type boundary_format: :class:`BoundaryFormat` enum
    :type permuted: bool
    :type one_minus: bool
    :type return_parts: bool
    :type window_size: int
    :type fnc_round: `function`


WindowDiff
**********
Proposed in [PevznerHearst2002]_, this segmentation comparison metric is an adaptation of Pk which runs a window over a hypothesis and reference segmentation and counts those hypothesis windows with differing numbers of contained boundaries that do not agree with the reference window as being in error.  These errors are then summed over all windows.

.. warning:: Prefer :func:`boundary_similarity` instead; see [Fournier2013]_.

.. function:: window_diff(hypothesis, reference, **kwargs)

    For parameters see :func:`pk`

.. function:: window_diff(dataset, **kwargs)

    For parameters see :func:`pk`

.. function:: window_diff

    For parameters see :func:`pk`


Inter-coderAgreement Coefficients
---------------------------------
Originally adapted in [FournierInkpen2012]_ from formulations provided by [ArtsteinPoesio2008]_, these have inter-coder agreement have been modified by [Fournier2013]_ to better suite the measurement of inter-coder agreement of segmentation boundaries   using :func:`boundary_similarity` for actual agreement.

.. function:: actual_agreement_linear
    
    Calculate actual (i.e., observed or :math:`\\text{A}_a`), boundary agreement without accounting for chance, using [ArtsteinPoesio2008]_'s formulation as adapted by [Fournier2013]_.
    
    :param fnc_compare: Segmentation comparison metric function to use; default :func:`boundary_similarity`
    :param boundary_format: Segmentation format; default ``BoundaryFormat.mass``
    :param permuted: Use pairwise permutations v.s. combinations; default ``False``
    :param one_minus: Return :math:`1-value`; default ``False``
    :param return_parts: Return tuples of numerators, demoninators, or other values comprising a metric; default ``False``
    :param n_t: See :func:`boundary_edit_distance`
    :param boundary_types: Set of allowewable boundary types; default ``set([1])``
    :param weight: Tuple of weighting functions, see :ref:`weightfunctions`; default is scaling of substitution and transposition but not addition edits (:func:`weight_a`, :func:`weight_s_scale`, :func:`weight_t_scale`)
    :type fnc_compare: function
    :type boundary_format: :class:`BoundaryFormat` enum
    :type permuted: bool
    :type one_minus: bool
    :type return_parts: bool
    :type n_t: int
    :type boundary_types: set
    :type weight: tuple

.. autofunction:: fleiss_pi_linear

    For parameters see :func:`actual_agreement_linear`

.. autofunction:: fleiss_kappa_linear

    For parameters see :func:`actual_agreement_linear`

.. autofunction:: artstein_poesio_bias_linear

    For parameters see :func:`actual_agreement_linear`


Format Conversion
-----------------
These utility functions are used internally and provided to allow for the conversion between the supported segmentation formats (see :class:`BoundaryFormat`).

.. autofunction:: boundary_string_from_masses
.. autofunction:: convert_positions_to_masses
.. autofunction:: convert_masses_to_positions


Data
----
These classes and functions deal with segmentation data representation and manipuation.

Model
*****
These classes are used to model and store text (i.e., item) segmentations (i.e., codings).

.. autoclass:: Dataset
    :members:

.. class:: Field()

    An ``enum`` with options representing json fields when storing segmentations which include:
        * ``segmentation_type``, the type if segmentation; default is ``SegmentationType.linear``
        * ``items``, items with annotators and codings stored within
        * ``codings``, annotators and codings stored within

.. class:: SegmentationType()

    An ``enum`` with options representing segmentation structure types including:
        * ``linear``, linear segmentation

Input/Output
************
These functions serialization and de-serialization segmentation datasets.
The recommended serialization format is ``JSON``.

.. seealso:: `JSON (JavaScript Object Notation) <http://www.json.org/>`_

.. autofunction:: input_linear_mass_tsv

.. autofunction:: input_linear_mass_json

.. autofunction:: output_linear_mass_json

.. autofunction:: load_nested_folders_dict


Information-Retrieval-related Statistics
----------------------------------------

.. autofunction:: precision

.. autofunction:: recall

.. autofunction:: fmeasure

.. autofunction:: summarize


Model
*****
Classes used to model segmentation comparisons so that they can be summarized by information retrieval related statistics (e.g., :func:`precision`).

.. class:: Average

    An ``enum`` with options representing the methods of computing averages:
        * ``micro``, micro-average
        * ``macro``, macro-average
    For more details, see the `Stanford IR Book <http://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-text-classification-1.html>`_.

.. autoclass:: ConfusionMatrix
    :members:


