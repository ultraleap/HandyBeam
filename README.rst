######
Readme
######


Readme file for gitlab repository root.

Note that the links in this particular document are compatible with gitlab.

*************
Documentation
*************

There is a user manual and a sphinx-compiled documentation in `<handybeam/doc/build/index.html>`_. Most methods are documented fairly well. If anything is unclear, contact me on [slack](https://ultrahaptics.slack.com/team/UB0RDJ24B) using [@jurek](https://ultrahaptics.slack.com/team/UB0RDJ24B)

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

=======
Support
=======

Primary developer is Dr Jerzy Dziewierz. Contact me on [slack](https://ultrahaptics.slack.com/team/UB0RDJ24B) using [@jurek](https://ultrahaptics.slack.com/team/UB0RDJ24B)

============
Contributors
============

in no particular order:

* `Tom Carter <https://www.linkedin.com/in/tom-carter/>`_ - project sponsor
* `Jerzy Dziewierz <https://www.linkedin.com/in/jerzy-dziewierz-156b3138/>`_ - primary developer and maintainer
* `Orestis Georgiou <https://www.linkedin.com/in/orestisgeorgiou/>`_ - legacy project sponsor
* `Salvador Catsis <https://www.linkedin.com/in/salvador-catsis-b91956161/>`_ - code contributor
* `Rob Malkin <https://www.linkedin.com/in/rob-malkin-84486843/>`_ - legacy code contributor
* `Hugh Hopper <https://www.linkedin.com/in/hugh-hopper-26b37957/>`_ , `Joe Spilman <https://www.linkedin.com/in/joe-spilman-6b5618a0/>`_, `Adam Price <https://www.linkedin.com/in/adam-price-ba015877/>`_ - calibration data, legacy code (Acoustic Renderer), helpful discussions
* `Brian Kappus <https://www.linkedin.com/in/brian-kappus-9359135b/>`_ - helpful discussions
* `LEVITATE project <https://www.levitateproject.org/>`_ calibration data, helpful discussions
* `Ben Long <https://www.linkedin.com/in/benjamin-long-1b455ba5/>`_ - helpful discussions
* `University of Strathclyde <https://www.linkedin.com/school/university-of-strathclyde/>`_ - legacy code contributor

============
Contributing
============

Note that as of release R1.0, compatibility with cueBEAM has been completely dropped.

Unless there are some UH rules that I do not know about, I'd say:

* For version number, use `semantic versioning 2.0.0 <https://semver.org>`_
* For new features and bugfixes, use `GitHub Flow model <https://guides.github.com/introduction/flow/>`_
    * ~~For branching workflow, use this: `<http://nvie.com/posts/a-successful-git-branching-model>`_.~~
    * ~~For new features, start a new folder, then a new submodule, and then use this: `<http://tom.preston-werner.com/2010/08/23/readme-driven-development.html>`_.~~
* For documentation, use this: `<http://www.writethedocs.org/guide/writing/beginners-guide-to-docs>`_
* For anything else, ask `Jerzy Dziewierz<https://ultrahaptics.slack.com/team/UB0RDJ24B>`_

----

================
Zen of HandyBeam
================

* *"There is no point in getting the wrong answer really, really fast"* -- speed of code matters, but only after it has been shown to operate correctly.

* *"All that we have is a model"* -  using simplifying assumptions is OK, just remember to describe the model in the documentation.

* *"Computer simulations are here to make the overall cost of doing the job cheaper, and not more expensive"*  (Richard O'Leary) -- Do not do time-consuming computations just because You can. Have a reason for spending Your time.

* *"Things should be as simple as possible, but not simpler"* (Albert Einstein)

* *"There are no unnatural things. There are only things that we do not know about nature"*

* *"Everyone knows that something is impossible to do. Then comes that new guy that doesn't know that. And he does it."* -- (Zygmunt Wrona, c.a. 1990). -- It is OK to experiment and have random whacky ideas. Also, it's OK to test the common knowledge and challenge authorities.

* *"Nothing is perfect"* -- it is OK to be wrong, as long as you invite the chance to get corrected.

**Note - all the points have their original authors, whom I sometimes cannot properly attribute. No claim is made to authorship of these.**

----


=============
LEGACY README
=============

`https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/`_ says I need one, but nothing to write here yet.

