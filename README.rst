***************
About HandyBeam
***************

**Do use HandyBeam for:**

* quick visualisation of example acoustic fields
* throw-away checks of what-if scenarios
* development of task-specific research code
* demonstrating that we are nice people (e.g. that we know what we are talking about, and that we are open-sourcing things)
* education, exploration, having fun
* cool animations and pleasant colours for decorating Your room.

**Do not use HandyBeam for:**

* secrets ( instead, clone the repo and do Your development there. Do not push to the public repo. )
* winning a bad argument (there is that saying - if you want to lie, use statistics. This applies here too.)

**Be aware that:**

* HandyBeam model makes **a lot** of assumptions, which might be an oversimplification of the problem that You are facing.

**Things that have been repeatedly asked for, but are waiting in the queue as of now**

These are in their order in the queue:

* time domain propagation simulation
* advanced excitation solvers (bessel beam, sonotweezer)
* reflections, scattering

*****
Links
*****

None at this moment.

******************
Legal & disclaimer
******************

=======
License
=======

Copyright 2019 Ultrahaptics

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at `this location <http://www.apache.org/licenses/LICENSE-2.0>`_

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


==========
Disclaimer
==========

1. If something uncool happens, it's Your fault.
2. If it breaks, you get to keep both pieces.

----

Complying with the license, be notified that **HandyBeam is a descendant of cueBeam** which was developed between 2008-2018 in `University of Strathclyde <https://www.strath.ac.uk/research/subjects/electronicelectricalengineering/instituteforsensorssignalscommunications/centreforultrasonicengineering>`_.
The original source code can be had from `here. <https://github.com/CentreForUltrasonicEngineering/cueBeam_EngD>`_

Although the core technology is based on the same principles, Note that virtually no source code is shared with cueBEAM. For example, the cueBEAM has been written for Matlab, MEX and CUDA. HandyBeam is a complete rewrite in Python and OpenCl.

Note that as of release R1.0, compatibility with cueBEAM has been completely dropped.

----

****************
Acknowledgements
****************

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 737087.



****************
Contributing
****************

Go to the "Contributing Guide" in the documentation.


Note that as of release R1.0, compatibility with cueBEAM has been completely dropped.

----

****************
Zen of HandyBeam
****************

* *"There is no point in getting the wrong answer really, really fast"* -- speed of code matters, but only after it has been shown to operate correctly.

* *"All that we have is a model"* -  using simplifying assumptions is OK, just remember to describe the model in the documentation.

* *"Computer simulations are here to make the overall cost of doing the job cheaper, and not more expensive"*  (Richard O'Leary) -- Do not do time-consuming computations just because You can. Have a reason for spending Your time.

* *"Things should be as simple as possible, but not simpler"* (Albert Einstein)

* *"There are no unnatural things. There are only things that we do not know about nature"*

* *"Everyone knows that something is impossible to do. Then comes that new guy that doesn't know that. And he does it."* -- (Zygmunt Wrona, c.a. 1990). -- It is OK to experiment and have random whacky ideas. Also, it's OK to test the common knowledge and challenge authorities.

* *"Nothing is perfect"* -- it is OK to be wrong, as long as you invite the chance to get corrected.

**Note - all the points have their original authors, whom I sometimes cannot properly attribute. No claim is made to authorship of these.**

----

*************
Documentation
*************

For a first look, see `<http://www.dziewierz.pl/handybeam-core-doc/> here`_. Note that this version might be somewhat outdated.

the sphinx-compilable theory, user manual, and documentation source code is at `<https://github.com/ultrahaptics/HandyBeam/tree/master/doc/source>`_. This will be corrected to the deployed documentation when I get the space to host it.

