:doc:`index`

==============
API principles
==============

Programming principles
----------------------

HandyBeam system expressed using 3 fundamental kinds of things:

* Data structures
* Procedures
* Objects


Data Structure
~~~~~~~~~~~~~~

* Describes what the bits and bytes are supposed to mean in both human and machine readable language
* Enables somewhat-meaningful data to exist
* Can be serialized and de-serialized, no surprises on the way
* Many copies can exist in a single session -- under different names or in an array
* Many versions can exist in single session - under different names or in an array
* The data structure does not know and doesn't care too much if the data is correct
* The data can be incomplete in sense that some more data is needed to do something or make complete sense out of it. The data structure does not make assumption that this extra data exists, nor that the extra data is compatible
* Data structure is well documented. It has the highest priority for documentation quality
* Data structures are fairly specialized for the purpose; their transferability is due to the good documentation only.
* In block diagram, the color is light yellow


Procedure
~~~~~~~~~

* Procedure is there to transform data
* Procedures take in data, only in data structures, and output data in data structures
* Procedures assume that the data is correct and complete, and are not required to do much checking.
* Procedures are only expected to work if the data structures and the data is correct and complete
* Procedures do not care if the data is correct. They work if it is, and can fail silently if it is not
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
* Objects take care for the data to be correct and complete
* Objects can be optionally serialisable, but not necessarily. They can contain non-serialisable items.
* Objects keep procedures and use them to manipulate data in data structures
* Objects take care for allowing procedures to only run if the data is OK
* Objects generally only carry one version of data in it's data structure
* Objects can hold multiple procedures but only expose the one that is appropriate to the data at hand
* Objects take care of errors and suggest action
* They can contain extra methods and state data to do housekeeping
* They can use it's internal state to make shortcuts to typical uses of procedures
* Objects are easy to use, and can even look nice in demos
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
4. The naming convention for functions may be used instead in cases where the interface is documented and used primarily as a callable.
5. Function names should be lowercase, with words separated by underscores as necessary to improve readability.
6. Variable names follow the same convention as function names.
7. If a function argument's name clashes with a reserved keyword, it is generally better to append a single trailing underscore rather than use an abbreviation or spelling corruption. Thus ``class_`` is better than ``clss``. (Perhaps better is to avoid such clashes by using a synonym.)
8. method names: Use the function naming rules: lowercase with words separated by underscores as necessary to improve readability.
9. method names: Use one leading underscore only for non-public methods and instance variables.

see `the full PEP8 text here. <https://www.python.org/dev/peps/pep-0008/>`_

.. include:: footer_licence_note.rst

