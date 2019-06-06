## Imports 

import sys
import numpy as np
import warnings
warnings.filterwarnings("ignore")

sys.path.append("../")  

import handybeam
import handybeam.world
import handybeam.tx_array_library
import handybeam.visualise
import handybeam.samplers.clist_sampler as clist_sampler
from handybeam.translator import Translator
from handybeam.solver import Solver


# Create world.

world = handybeam.world.World()

# Add a transmitter array to the world.

world.tx_array = handybeam.tx_array_library.rectilinear(parent=world)

# Instantiate translator and solver objects.

translator = Translator(parent = world)

solver = Solver(parent = world)

# Instruct the solver to solve for the activation coefficients.

solver.single_focus_solver(x_focus = 0,y_focus = 0,z_focus = 100e-3)

# Add clist sampler object to the world

volume_sampler = world.add_sampler(clist_sampler.ClistSampler( parent=world ))

# Specify points in the volume to sample the acoustic field on

no_points = 150

x = np.linspace(-500e-3,500e-3,no_points)
y = np.linspace(-500e-3,500e-3,no_points)
z = np.linspace(10e-3,500e-3,no_points)

x_mesh,y_mesh,z_mesh = np.meshgrid(x,y,z)

x_list = x_mesh.ravel()
y_list = y_mesh.ravel()
z_list = z_mesh.ravel()

# Add these sample points to the sampler

volume_sampler.add_sampling_points(x_list,y_list,z_list)

# Propagate the field

world.propagate()

# Save original pressure field.

original_field = np.copy(volume_sampler.pressure_field)

# Translate array.

translator.xyz_translate(x_focus = 0,y_focus = 0, z_focus = 100e-3,
                         x_translate = 0,y_translate = 50e-3, z_translate =50e-3)

# Propagate the acoustic field.

world.propagate()

# Visualise the acoustic field.
print('pre vis')
handybeam.visualise.visualise_translation_3D(world, original_pressure_field = original_field,
                                             sampler = volume_sampler, threshold = 50)
print('post vis')
