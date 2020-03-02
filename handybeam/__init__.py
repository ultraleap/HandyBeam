from .misc import HandyDict as dict
from . import world
from . import beamformer
from . import samplers

"""

This module contains all the submodules for the handybeam software package.

"""

"""
shortcut to make it easier to use HandyDict as the primary data structure
"""


name = "handybeam"

__all__ = [
    'bugcatcher',
    'cl_system',
    'evaluators',
    'misc',
    'solver',
    'translator',
    'tx_array',
    'tx_array_library',
    'visualise',
    'world',
    'cl',
    'cl_py_ref_code',
    'opencl_wrappers',
    'propagator_mixins',
    'samplers',
    'solver_mixins',
    'translator_mixins'
]




