##############################
handybeam.propagators
##############################

.. Warning::

    All the user-visible code for propagators got absorbed into :ref:`handybeam_samplers`. See that documentation first.

.. code-block:: rst

     Production
    =============

    The following propagators are well tested and OK to use in production code.

    "c" stands for complex-valued output

    "xyz" stands for the sampling grid being defined as regular XYZ-axes aligned sampling grid.

    "list" stands for sampling points defined from a flat list of XYZ coordinates.

    cxyz
    ==========================

    see also: :doc:`OpenCL kernel : "cxyz" <051__handybeam1kernel_cxyz.cl>`

    .. note::

        Use this module as 1st preferred propagator.

    .. automodule:: handybeam.propagators.cxyz
        :members:

    clist
    ===========================

    see also: :doc:`OpenCL kernel : "clist" <051__handybeam1kernel_clist.cl>`

    .. note::

        Use this module as 2nd preferred propagator.

    .. automodule:: handybeam.propagators.clist
        :members:


    == Development
    ==============

    The following propagators are either experimental, in development, or partially broken.

    :code:`Do not use unless you really know what you are doing`.


    calculator_py_yz
    ===========================

    .. automodule:: handybeam.propagators.calculator_py_yz
        :members:

    devel_calculator_py_yz
    ============================================

    .. automodule:: handybeam.propagators.devel_calculator_py_yz
        :members:


    legacy_calculate_xy_frequency_domain_py
    =============================================================


    .. automodule:: handybeam.propagators.legacy_calculate_xy_frequency_domain_py
        :members:


    legacy_calculator_XYPlane_frequencyDomain_cl
    ========================================================


    .. automodule:: handybeam.propagators.legacy_calculator_XYPlane_frequencyDomain_cl
        :members:


    legacy_calculator_YZPlane_frequencyDomain_cl
    ========================================================


    .. automodule:: handybeam.propagators.legacy_calculator_YZPlane_frequencyDomain_cl
        :members:


.. include:: footer_licence_note.rst