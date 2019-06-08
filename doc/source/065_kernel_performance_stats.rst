:doc:`index`

########################
Kernel performance stats
########################

Date: 2018-10-12
Version : 1.0.9

Device @ clock frequency: performance for script ``demos\basic_flat_field_.py``


Jurek's Windows laptop, MSI GS65 Stealth Thin 8RF:
--------------------------------------------------

Intel(R) UHD Graphics 630 @ 1100MHz : 1479.0[MRays/sec]

Intel(R) Core(TM) i7-8750H CPU @ 2.20GHz , 12 threads: 254.6[MRays/sec]

GeForce GTX 1070 with Max-Q Design @ 1265MHz : ~14'000[MRays/sec] - some work shapes fail, this is to be investigated further
(note: work shape not optimised)

Jurek's Macbook Pro 2017 model A1707
------------------------------------

AMD Radeon Pro 560 Compute Engine @ 300MHz: 6875.2[MRays/sec] (note: work shape not optimised)

Intel(R) HD Graphics 630 @ 1100MHz: 1155.4[MRays/sec] - requires ugly hacks to make the #defines work

Intel(R) Core(TM) i7-7820HQ CPU @ 2.90GHz: 121.9[MRays/sec] -- Requires work_group_size of (1,1,1).


Sal's Macbook Pro June 2018 model A1990
---------------------------------------

AMD Radeon Pro 560X Compute Engine @ 1024MHz : 1670.1[MRays/sec] -- something is wrong with this -- i think it might be using the Intel graphics, not the AMD Radeon

.. include:: footer_licence_note.rst

