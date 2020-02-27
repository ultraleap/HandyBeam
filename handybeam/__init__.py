"""

This module contains all the submodules for the handybeam software package.

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
    'visiualize',
    'world',
    'cl',
    'cl_py_ref_code',
    'opencl_wrappers',
    'propagator_mixins',
    'samplers',
    'solver_mixins',
    'translator_mixins'
]


"""
shortcut to make it easier to use HandyDict as the primary data structure
"""
from .misc import HandyDict as dict


