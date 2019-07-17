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


These are explained later in the walk through:

* pyopencl
* matplotlib
* pyqtgraph
* bugsnag
* numpy
* scipy
* cmocean
* appdirs  -- :code:`pip install appdirs`



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

for Mac, the command may be:

.. code-block:: bash

    source activate handybeam


for Windows, the command may be:

.. code-block:: bash

    activate handybeam

for other platforms, consult Conda documentation.

08. Install jupyter and spyder **in this environment**. Note that even tough jupyter and spyder would normally launch without this, they might confuse which environment to run in. So we have to remind them by installing them again here.

.. code-block:: bash

    conda install ipykernel jupyter spyder


09. Install remaining dependencies

.. code-block:: bash

    pip install bugsnag appdirs vispy pyquaternion pyopengl
    conda install nb_conda_kernels matplotlib pyqtgraph numpy scipy pandas
    conda install -c conda-forge cmocean


10. Install pyopencl. At this point, there might be some errors, depending on how is Your laptop set up. If they occur, you will have to somehow debug it and then come back here. In any case, make sure that pyopencl is installed correctly and you can run some examples.

.. code-block:: bash

    conda install -c conda-forge pyopencl


Note that the common problem here is that the 'fully featured' drivers for either the CPU or GPU are not installed on Your system.

You might want to bing for OpenCL drivers for Your hardware, e.g. `like this <https://www.bing.com/search?q=opencl+intel+drivers>`_

11. Clone the repository from github, or download it.

.. code-block:: bash

    git clone https://github.com/ultrahaptics/HandyBeam.git handybeam_core_repo

12. Select the OpenCl compute device

.. Warning:

    This section is important. Do not skip the understanding of it.

.. ToDo::

    This section might be outdated -- please take care. I will update and verify asap!

HandyBeam uses OpenCL to accelerate the compute-intensive parts of the code.

Since there can be many parallel computing devices in Your machine, one needs to be selected.

At this time, there is no automatic selector implemented. You have to do this manually.

.. code-block:: bash

    import handybeam.propagator
    handybeam.propagator.print_cl_platforms()
    handybeam.propagator.select_cl_platform(use_platform=0,use_device=0)


Your selection is stored in :code:`cl_platform_config.ini`.

For the Ultrahaptics standard issue Macbook Pro (2019) it will typically be:

.. code-block:: ini

    [what_to_use]
    use_platform = 0
    use_device = 2

For a Windows platform with a high-power GPU, it will typically be:

.. code-block:: ini

    [what_to_use]
    use_platform = 0
    use_device = 0

For other machines (Linux, Android e.t.c.) you need to be able to figure it for yourself.

14. Next time You start Your terminal, be reminded that You need to 'activate the handybeam envinroment' first.

for Mac, the command may be:

.. code-block:: bash

    source activate handybeam


for Windows, the command may be:

.. code-block:: bash

    activate handybeam

for other platforms, consult Conda documentation.


14. Try the :code:`demos\basic_flat_field_.py`

15. Try the :code:`demos\demo_mouse_control_field.py`


.. include:: footer_licence_note.rst
