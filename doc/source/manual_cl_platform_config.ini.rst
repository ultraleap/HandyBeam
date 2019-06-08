* back to top: :doc:`index`

######################
cl_platform_config.ini
######################

This file stores the setting for the OpenCL subsystem.

Typical content:

.. code-block:: ini

    [what_to_use]
    use_platform = 1
    use_device = 0

see :py:mod:`handybeam.cl_system` module and :py:meth:`handybeam.cl_system.select_cl_platform` method.

.. include:: footer_licence_note.rst
