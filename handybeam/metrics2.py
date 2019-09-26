"""
.. _metrics2:
.. ----------------------------------
   Module :code:`handybeam_surfaces.metrics2`
   ----------------------------------
This class includes metrics to evaluate the quality of a rendered haptic shape.

This particular implementation is based on Salvador's "SurfaceEvaluator" class, but thinned and programmed in a different way.

"""

import numpy as np


class SurfaceMetrics2:

    def __init__(self,
                 sampler=None,
                 desired_field=None,
                 surface_indices=None):
        """
        Start the object based on an existing sampler, desired field and surface_indices data:

        Parameters
        ----------

        sampler : handybeam_surfaces.samplers.*
            an instance that descends from :py:class:`handybeam.samplers.AbstractSampler`
        desired_field : complex ndarray
            A complex numpy array of dimension (m x n ) representing the desired surface. Same format as the surface beam former solver
        surface_indices :  Boolean ndarray
                    For a sampling grid of dimension n x m, this will be an n x m Boolean numpy array
                    which indicates the points in the set S (inside the shape) and the points the set
                    S_n (outside the shape).
        """

        self.sampler = sampler
        self.desired_field = desired_field
        self.surface_indices = surface_indices

        if not hasattr(sampler, 'pressure_field'):
            raise Exception('sampler has no pressure_field ? cannot continue.')
        self.propagated_field  = self.sampler.pressure_field

        if not self.propagated_field.shape == self.desired_field.shape:
            raise Exception(f'desired field shape={self.desired_field.shape}, sampler.pressure_field.shape = {self.sampler.pressure_field.shape}; These must be equal.')

        if surface_indices is not None:
            if not self.surface_indices.shape == self.propagated_field.shape:
                raise Exception(f'surface_indices.shape = {self.surface_indices.shape}; surface_indices.shape={self.surface_indices.shape}; These must be equal.')

    @property
    def null_surface_indices(self):
        return np.invert(self.surface_indices)

    @property
    def shape_rms_power(self):
        shape_values = self.propagated_field.ravel()[self.surface_indices.ravel()]
        shape_rms_power = np.mean(np.abs(shape_values * np.conj(shape_values)))
        return shape_rms_power

    @property
    def null_shape_rms_power(self):
        null_shape_values = self.propagated_field.ravel()[self.null_surface_indices.ravel()]
        null_shape_rms_power = np.mean(np.abs(null_shape_values * np.conj(null_shape_values)))
        return null_shape_rms_power

    @property
    def surface_contrast_ratio(self):
        return self.shape_rms_power/self.null_shape_rms_power

    @property
    def surface_contrast_db(self):
        return 20.0*np.log10(self.surface_contrast_ratio)

    @property
    def shape_rms_pressure(self):
        return np.sqrt(self.shape_mean_power)

    @property
    def metrics_vector(self):
        return np.array([
            self.shape_rms_pressure,
            self.surface_contrast_db,
        ])

    def __repr__(self):
        return f'contrast: {self.surface_contrast_db:7.4}dB'

    def __str__(self):
        return self.__repr__()



