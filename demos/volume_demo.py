## Imports

import sys
import numpy as np
import warnings
warnings.filterwarnings("ignore")

sys.path.append("../.")

import handybeam_core
import handybeam_core.world
import handybeam_core.tx_array_library
import handybeam_core.visualise
import handybeam_core.samplers.clist_sampler as clist_sampler
from handybeam_core.solver import Solver



# Initialise the world 

world = handybeam_core.world.World()

# Initialise a solver

solver = Solver(parent = world)

# Add a transmitter array to the world

world.tx_array = handybeam_core.tx_array_library.rectilinear(parent = world)

# Instruct the solver to solve for the activation coefficients

solver.single_focus_solver(x_focus = 0, y_focus = 0, z_focus = 100e-3)

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

# Visualise the result

volume_sampler.visualise_3D(threshold = 50,colour_map = 'viridis')