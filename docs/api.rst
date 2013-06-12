.. _api:

.. module:: segeval

Developer Interface
===================
The APIs for most metrics can be provided either two segmentations to compare or a dataset to perform pairwise comparisons upon.
There are a variety of parameters that can be specified other than that which is compared, but all have defaults specified.


Boundary-Edit-Distance-based Metrics
------------------------------------
These segmentation comparison metrics are those that have been introduced in [Fournier2013]_.

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

	:param segmentation_*: Segmentation of a particular format; see :class:`BoundaryFormat`
	:type segmentation_*: segmentation

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

	See :func:`boundary_similarity`

.. function:: segmentation_similarity(dataset, **kwargs)

	See :func:`boundary_similarity`

.. function:: segmentation_similarity

	See :func:`boundary_similarity`


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

.. function:: boundary_similarity(hypothesis, reference, **kwargs)

	:param segmentation_*: Segmentation of a particular format; see :class:`BoundaryFormat`
	:type segmentation_*: segmentation

.. function:: boundary_similarity(dataset, **kwargs)

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
Proposed in [BeefermanBerger1999]_, this

.. warning:: Prefer :func:`boundary_similarity` instead; see [Fournier2013]_.

.. function:: pk(hypothesis, reference, **kwargs)

	:param hypothesis: Hypothetical, or automatically-generated, segmentation of a particular format; see :class:`BoundaryFormat`
	:param reference: Reference, or manually-created, segmentation of a particular format; see :class:`BoundaryFormat`
	:type hypothesis: segmentation
	:type reference: segmentation

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
Proposed in [PevznerHearst2002]_, this

.. warning:: Prefer :func:`boundary_similarity` instead; see [Fournier2013]_.

.. autofunction:: window_diff


Inter-coderAgreement Coefficients
---------------------------------

.. autofunction:: actual_agreement_linear
.. autofunction:: fleiss_pi_linear
.. autofunction:: fleiss_kappa_linear
.. autofunction:: artstein_poesio_bias_linear


Format Conversion
-----------------

.. autofunction:: boundary_string_from_masses
.. autofunction:: convert_positions_to_masses
.. autofunction:: convert_masses_to_positions


Data Input/Output
-----------------

.. autoclass:: Dataset
.. autoclass:: Field
.. autofunction:: input_linear_mass_tsv
.. autofunction:: input_linear_mass_json
.. autofunction:: output_linear_mass_json
.. autofunction:: load_nested_folders_dict


ML-related statistics
---------------------

.. autofunction:: precision
.. autofunction:: recall
.. autofunction:: fmeasure
.. autoclass:: Average
.. autoclass:: ConfusionMatrix
.. autofunction:: summarize

