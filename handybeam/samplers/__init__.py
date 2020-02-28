"""

This module contains submodules for generating the sampling grid
coordinates on which to propagate the acoustic field. 

"""


__all__ = [
            'abstract_sampler',
            'clist_sampler',
            'hexagonal_sampler',
            'lambert_sampler',
            'rectilinear_sampler'
            ]

from . import clist_sampler
