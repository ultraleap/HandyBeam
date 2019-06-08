:doc:`index`

============
Installation
============

Introduction
------------

At the time of this writing, there is no handybeam package ready for automated installation. There might be one in the future.

Hence, one has to install all the files and dependencies by hand.

Notable dependencies
--------------------


These are explained later in the walkthrough:

* pyopencl
  * There is no plan to have pure python implementation, do not ask.
* matplotlib
* pyqtgraph
* bugsnag
* numpy
* scipy
* cmocean


Instructions
------------

MacOS
~~~~~

These are instructions for mac:

01. install git from `https://git-scm.com/download <https://git-scm.com/download>`_

02. install anaconda, python 3.6 version, from `https://www.anaconda.com/download <https://www.anaconda.com/download>`_

03. go to the mac console. You might need two tabs.

04. in the console, go to the folder where You intend to store the copy of HandBeam software

05. create a new environment with Python 3.6.5:

.. code-block:: bash

    conda create -n handybeam python=3.6.5


06. Wait for the installation to progress

07. Activate the new environment:

.. code-block:: bash

    source activate handybeam


08. Install jupyter and spyder **in this environment**. Note that even tough jupyter and spyder would normally launch without this, they might confuse which environment to run in. So we have to remind them by installing them again here.

.. code-block:: bash

    conda install ipykernel jupyter spyder


09. Install remaining dependencies

.. code-block:: bash

    pip install bugsnag
    conda install nb_conda_kernels matplotlib pyqtgraph numpy scipy pandas
    conda install -c conda-forge cmocean


10. Install pyopencl. At this point, there might be some errors, depending on how is Your laptop set up. If they occur, please make a screenshot and send them to me.

.. code-block:: bash

    conda install -c conda-forge pyopencl


Note that the common problem here is that the 'fully featured' drivers for either the CPU or GPU are not installed on Your system.
You might want to bing for OpenCL drivers for Your hardware, e.g. `like this <https://www.bing.com/search?q=opencl+intel+drivers>`_

11. Clone the repository from gitlab, or download it.

This assumes that Your machine is properly registered for using gitlab. If it is not (SSH keys et cetera) - ask relevant person to help You to set up gitlab first.
As of 2018-09, that person is `Lawrence Chan  @lawrence.chan <https://ultrahaptics.slack.com/team/U69GMSCKD>`_

.. code-block:: bash

    git clone git@gitlab.ultrahaptics.com:arc/HandyBeam.git handybeam


If Your machine is not set-up to use the company's gitlab, you can still download the handybeam from other sources.

Ask me on slack and I'll send You a link or a zip file.


12. Select the Opencl compute device

.. Warning:

    This section is important. Do not skip the understanding of it.

HandyBeam uses OpenCL to accelerate the compute-intensive parts of the code.

Since there can be many parallel computing devices in Your machine, one needs to be selected.

At this time, there is no automatic selector implemented. You have to do this manually.

.. code-block:: bash

    import handybeam.propagator
    handybeam.propagator.print_cl_platforms()
    handybeam.propagator.select_cl_platform(use_platform=0,use_device=0)


Your selection is stored in :code:`cl_platform_config.ini`.

For the Ultrahaptics standard issue Macbook Pro (2018) it will typically be:

.. code-block:: ini

    [what_to_use]
    use_platform = 0
    use_device = 2


14. Try the :code:`demos\basic_flat_field_.py`

15. Try the :code:`demos\demo_mouse_control_field.py`

Any problems - let me know, preferably with slack `@Jurek <https://ultrahaptics.slack.com/team/UB0RDJ24B>`_

.. include:: footer_licence_note.rst
