# Change log and devel blog

## 2019-05-24 Documentation rush

* Jurek picks up development of the HandyBeam core
* This version has multiple contributions from Salvador Catsis
* Updating the Readme to prepare for open-source release 


## 2019-01-21 Documentation rush

* Lots of updates to documentation
    * the docstrings now have 100% coverage
* Trims to source code and minor refactorings
* Tests have not ran for a while now, I expect many things to be broken
* Starting to split the public code from add-on-development-only code. New domain: UH



## 2019-01-07 Development restart

* Lots of updates to documentation
	* Moving obsolete parts of the documentation to the [obsolete] folder
* Small trims of the source code as I work through documenting it
* New concept: higher performance, and more flexible TxArray objects
	* there will be many TxArray types, one for each special case
	* TxArray instance holds all the data about it's transducers, in a uniform float-typed memory block,  no need for list of TxElement objects. This should make the operations on the elements significantly faster. 
	* The TxElement becomes a 'viewer' onto the flat memory block of the TxArray
	* I can begin introducing this by simply making another TxArray Class - with new features
	* The propagators need a better architecture . . . .
* New concept: reference propagators
	* should make it easier to write tests
	* should make it easier to demonstrate equivalence and correctness
	* should be good for education


## 2018-10-04

* sampling point list sampler and core - debugging
* Studying User Stories with Simon

## 2018-10-03

* bugfix in the propagator.py
* sampling point list sampler and core - first implementation

## 2018-10-02

Bump version number to 1.0.5

* Learning about software engineering with Simon
  * The production process
  * The tests & coverage
  * Capturing the requirements - user stories
  * the V-model
* Refactoring field* and parent* to sampler*
* adding named parameters instead of positional parameters everywhere possible
* watching https://www.youtube.com/watch?v=OSGv2VnC0go - a way towards more beautiful python
  * lot's of advice there, I will want to use it, here are the more relevant ones:
    04:47 -- Looping over a collection
    06:51 -- Looping over a collection of indicies
    07:36 -- Looping over two collections
    21:10 -- Looping over dictionary keys and values
    31:10 -- Clarify function calls with keyword arguments
    32:17 -- Clarify multiple return values with named tuples
    33:13 -- Unpacking sequences
    34:01 -- Updating multiple state variables
    36:15 -- Simultaneous state updates
    38:24 -- Concatenating strings
    39:57 -- Using decorators to factor-out administrative logic
    41:19 -- Factor-out temporary contexts for decimal
    42:25 -- How to use locks
    46:04 -- Concise expressive one-liners

## 2018-10-01

* Created abstract_sampler_ortho and separated from abstract_sampler
* began renaming field* to sampler*:
  * handybeam.xy_plane.XYPlane is now handybeam.sampler_plane_xy.PlaneXY
  * handybeam.yz_plane.YZPlane is now handybeam.sampler_plane_yz.PlaneYZ
  * handybeam.world.add_plane is now handybeam.world.add_sampler
  * et cetera

## 2018-09-30

Added a documentation for the kernel cxyz.cl

Attempt to convert the documentation from markdown to ReStructuredText

## 2018-09-24

Improved bugcatcher version reporting. It will now report latest tag as version, and git repo commit SHA as the metadata.

HN-97 : the default phase directivity slope updated to zero to reflect the latest findings about how the phase behaves (Slack discussion from 2018-09-21)

HN-100 : example how to create a volume of data for display in Voreen

## 2018-09-19 branch: doc_generated, author: Jurek

creating the "moved subaperture" and "rotated subapertures" demo in `demo_rectilinear_hexa_sunflower_arrays.ipynb`

Added a new handy method : `handybeam.visualize.visualize_xy_and_array()` - to serve the needs of the demo above

## 2018-09-18 HandyBeam R1.0.0 release event

The first release.