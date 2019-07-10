:doc:`index`

=================
Code organisation
=================

It is recognized that a scientific research package like this is to be used in an environment
that is very fluid: Fluid in that every day, a different question is being asked. The code structure needs to follow this usage pattern.

Based on some years of experience, the following structure of folders is recommended.

The root folder contains several sub-folders, which are in turn primarily root git repositories. The concept is that each repository contains a package that can be reasonably maintained by a single person or at most, a small team.

Each of these folders has a different development 'time scale' and a different size of audience.


.. code-block:: rest

    ----\2018_05_science_work                   [root document folder] -- the date helps with archiving and back-ups, and later, managing Your archives and versions
        |
        |--#\handybeam_core                     [public git root] -- code that you are least likely to edit, but likely to download updates. This code is useful for a wide community. Size of audience: 5-500
        |   |   \                               [folder root] - readme, licence, e.t.c.
        |   |---\handybeam                      [python package root] this is what you get when you say "import handybeam.*"
        |       |---\***                        [modules of the handybeam package]
        |
        |--#\handybeam_core_doc                 [public git] -- code that you are least likely to edit, but likely to download updates
        |   |---\                               [folder root] - readme, licence, configuration for the compiler e.t.c.
        |   |---\source                         [sphinx documentation root]
        |   |   |---\static
        |   |---\build                          [.git ignored] - do not include compiled version of the files into git repository.
        |       |---\***
        |
        |--#\handybeam_extension1               [public git] -- Your primary long-term contributions to the community go here. This code is fairly general and useful for a wider (specialized) community. After a fervent development, you update it every month. Size of audience: 2-15
        |    |-->\handybeam_extension1          [python package root]
        |        |-->\***
        |--#\handybeam_extension1_doc           [public git] -- Your primary long-term contributions to the community go here. You update it over long periods of time, as bugs and applications emerge.
        |   |-->\source                         [sphinx documentation root] - note that the documentation could go into a separate git repository than the code.
        |   |-->\build
        |
        |--#\handybeam_extension2               [private git] -- Your newest contributions go here. You are actively adding new methods as soon as they look like you would want to use them more than once. Size of audience: 1-3
        |   |-->\handybeam_extension2           [python package root]
        |       |-->\doc                        [sphinx documentation root]
        |
        |--#\2018_05_03_problem_1                 [private git] -- The source code files for the current problem at hand. You edit this multiple times per day.
        |   |-->\
        |   |-->\**
        |
        |---\2018_05_03_problem_1_subresults    [no git!] -- the "generated" files e.g. figures, generated datasets, temporary files, subresults, previews, e.t.c.
        |--#\2018_05_03_problem_1_final_results [private git] -- the "publishable" results, e.g. final data sets, figures, notes, example code uses.
        |
        |---\2018_06_14_problem_2
        |---\2018_06_14_problem_2_subresults    [no git!]
        |--#\2018_06_14_problem_2_final_results [private git] -- the "publishable" results
        |
        |---\2018_06_16_problem_3
        |---\2018_06_16_problem_3_subresults    [no git!]
        |--#\2018_06_16_problem_3_final_results [private git] -- the "publishable" results
        |
        |
        |--#\another_editable_package           [git]
        |
        |--#\misc                               [git]
        |--\tmp                                 [git]


At first, it looks like this is "more work" - compared to just keeping everything in a single folder. If you think that, then please recall that science is only valuable if it is shared, effectively. In order to share Your work and results effectively, a consistent and maintainable structure is needed.

The concept for the structure above is that each 'major module' should be small enough to be maintainable by a single person.

As to the implementation and programming philosophy, see :ref:`023_api_principles:Api principles`

Where to use Git?
-----------------

As a rule of thumb, treat Your personal time as expensive, and treat computer time as cheap. Use Git to secure the expensive things.

==============
API principles
==============

Programming principles
----------------------

HandyBeam system is expressed using 3 fundamental kinds of things:

* Data structures
* Procedures
* Objects


Data Structures
~~~~~~~~~~~~~~~

* Describes what the bits and bytes are supposed to mean in both human and machine readable language
* Enables somewhat-meaningful data to exist
* Can be serialized and de-serialized, no surprises on the way
* Many copies can exist in a single session -- under different names or in an array
* Many versions can exist in single session - under different names or in an array
* The data structure does not know and doesn't care too much if the data is correct
* The data can be incomplete in sense that some more data is needed to do something or make complete sense out of it. The data structure does not make assumption that this extra data exists, nor that the extra data is compatible
* Data structure is well documented. It has the highest priority for documentation quality
* Data structures are fairly specialized for the purpose; their transferability is due to the good documentation only.
* it can be serialized, but preferably with some meta-data or objects so that it can be interpreted correctly later on.
* In block diagram, the color is light yellow



Procedures
~~~~~~~~~~

* Procedure is there to transform data
* Procedures take in data, only in data structures, and output data in data structures
* Procedures assume that the data is correct and complete, and are not required to do much checking.
* Procedures are only expected to work if the data structures and the data is correct and complete
* Procedures do not care if the data is correct. They work well if it is, and can fail silently if it is not
* Procedures do not store any data for themselves beyond it's life time. They avoid the need to have a persistent state.
* Procedures do not alter any external data, nor require any more data than provided in the explicit input
* Procedures do not need to be pretty nor easy to use
* Procedures are documented with theory of operation, fairly dry description of data structures they take, and some details on implementation. They generally take second priority for documentation quality
* There can be only one procedure under specific name, all names are unique, and uniquely identify specific procedure that, once written, only does that specific thing
* Procedures that do even slightly different things are named with unique names.
* Procedures are not required to be particularly universal. They are allowed to work with limited ranges of data only.
* Implementation of the procedures desirably can be, but does not necessarily have to be transferable to other uses and platforms
* Procedures are in principle usable without objects, as they do not depend on any other environment than the one supplied with the input arguments
* in block diagram, the color is light green


Objects
~~~~~~~

* Objects organize data and procedures, can hold them together under single name
* Objects take care for the data to be correct and complete, as far as practicable
* Objects can be optionally serialisable, but not necessarily. They can contain non-serialisable items.
* Objects keep procedures and use them to manipulate data in data structures
* Objects take care for allowing procedures to only run if the data is OK, but due to how nature works, they might sometimes be wrong
* Objects generally only carry one version of data (single 'opinion about state of the world') in it's data structure
* Objects can hold multiple procedures but tend to only expose the ones that are appropriate to the data at hand
* Objects make effort to take care of errors and suggest action by the user
* Objects make effort to be compatible with other objects as needed, and can have glue code
* They can contain extra methods and state data to do housekeeping
* They can use it's internal state to make shortcuts to typical uses of procedures, or even select procedures silently
* Objects strive to be easy to use, and can even look nice in demos
* Over time, objects can have different/evolving functionality under the same brand name. The old versions of the objects and their functionality remains with git
* Objects support in-line help/hints (e.g. method and field lists with short docstrings)
* Other than above, they receive third priority for documentation
* In block diagram, color is white


Remarks
-------

.. Warning::

    The above principles are guiding only.

PEP8 short summary
------------------

1. Modules should have short, all-lowercase names. Underscores can be used in the module name if it improves readability. Python packages should also have short, all-lowercase names, although the use of underscores is discouraged.
2. When an extension module written in C or C++ has an accompanying Python module that provides a higher level (e.g. more object oriented) interface, the C/C++ module has a leading underscore (e.g. _socket)
3. Class names should normally use the CapWords convention.
4. [with regards to class name] The naming convention for functions may be used instead in cases where the interface is documented and used primarily as a callable.
5. Function names should be lowercase, with words separated by underscores as necessary to improve readability.
6. Variable names follow the same convention as function names.
7. If a function argument's name clashes with a reserved keyword, it is generally better to append a single trailing underscore rather than use an abbreviation or spelling corruption. Thus ``class_`` is better than ``clss``. (Perhaps better is to avoid such clashes by using a synonym.)
8. method names: Use the function naming rules: lowercase with words separated by underscores as necessary to improve readability.
9. method names: Use one leading underscore only for non-public methods and instance variables.

see `the full PEP8 text here. <https://www.python.org/dev/peps/pep-0008/>`_

.. include:: footer_licence_note.rst

