:doc:`index`

############
User stories
############

.. admonition:: Disclamer

    This is my attempt to use the "SCRUM Method" of software engineering.
    You will find that much of that is either incomplete or plain wrong.
    If you have a good idea on how to help out, please do!

    I currently draw the basics from "Scrum product ownership" by Robert Galen.



************
Introduction
************

This document is to aid the design of the HandyBeam.
Here, example user stories (as per design, not actual stories) will be listed.

use https://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html for headings

*******************
User story template
*******************

Template
--------

    As a <role>

    I want <system behaviour>

    So that I realise <some business value>

    And that I can see that it does <example>

Story characteristics
---------------------

desirable, but not necessary :

* Independent
* Negotiable
* Valuable
* Estimate-able
* Small 
* Testable 

***********
The stories
***********

1. Open Source Scientist story 1
--------------------------------

< front side : the story >

As a beginner scientist in an open source world, wishing to learn and contribute,

I want an OpenCL code to take transducer outputs as input, integrate them for given space, and output the pressure,

and the code is well documented and testable

so that I can learn and contribute to that code

and I can see that my contributions are being accepted into the main repository.

< back side: requirements list >

* [ ] There exists a documentation page for each of the OpenCL kernels
* [ ] The code is split into steps, and the steps are numbered, so that they can be matched with the more detailed explanation in the documentation
* [ ] There is a demo script that specifically demonstrates how to use kernel only, with nothing else enabled
    * [ ] this implies that the current implementation of the kernel launcher must get simplified a bit - it is too dependent on the TxArray and TxElement objects. the TxArray must take the responsibility for preparing the TxElement data into the right format.


********
Personas
********

Personas are example types of people that will use HandyBeam.

Persona A: Array layout design student
--------------------------------------

Student Alex is a beginner into the phased array layout business.
He has some fresh, exciting ideas that are going to change the world and he merely needs to prove it. 

He knows python, and has briefly seen some reserach papers on phased array design.
He did some work with python for an undergraduate course or hobby project. 

He knows where to find examples on how to use Jupyter, but his default envinroment is Matlab.

He has found HandyBeam on github or someone recommended it to him.

> 

Persona B: Advanced phased array engineer
-----------------------------------------

Engineer Barry knows quite a bit about phased array layout and typical interactions between the input parameters.
He needs to check some numbers about specific design, or run an optimizer to find what inputs satisfy specific conditions that are known to be achievable.
He also needs to see how some change (e.g. a new transducer type) influences existing designs. 
He needs his work done fast and can't afford the results to be wrong.
His default envinroment is Matlab, but he'll take whatever it is that finishes his job before 5pm. 
He will often appreciate that Python is free. 

>

Persona C: Signal processing scientist
--------------------------------------

A signal processing scientist Clark has spent half of his life looking for a solvable problem to solve. 
He finally got it.
The new problem requires something unusual to be computed. The unusual bit is fairly small and would be a nice addition to an existing open software package.
He is willing to do the work pro publico bono, but he also might need some help when he is stuck or else the world will continue to decay.

He appreciates the beauty of the code base and detailed explanations, and he will learn a lot in the process.
He is trained in Matlab, but prefers python for it's beauty and open source philosophy.

>

Persona D: Salesperson
----------------------

Salesperson Derek needs some images to wow the clients with how advanced given product is.
He cares little about what means what, but he needs flashy keywords to fire just in case if someones asks him a question that he can't really answer.

> 


Persona E: User Experience superstar
------------------------------------

An UX developer Eddy is looking to see how different haptic sensations look like.
He has some idea on how the phased array works, and a fairly good idea on what the final user would like to feel.

He wants some visuals to aid his understanding on how do the two relate.

>

**********
User story
**********

Certain Advanced Phased Array Engineer (Barry) needs . . . . 

************************
Story to feature mapping
************************


.. Note:

    Nothing here yet?


.. include:: footer_licence_note.rst