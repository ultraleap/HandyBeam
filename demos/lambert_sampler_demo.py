## Imports

import sys
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore")
sys.path.append("../.")  


import handybeam
import handybeam.world
import handybeam.tx_array_library
import handybeam.tx_array
import handybeam.samplers.lambert_sampler as lambert_sampler
from handybeam.solver import Solver

# Initialise the world 

world = handybeam.world.World()

# Initialise a solver

solver = Solver(parent = world)

# Add a transmitter array to the world

world.tx_array = handybeam.tx_array_library.rectilinear(parent = world)

# Instruct the solver to solve for the activation coefficients

solver.single_focus_solver(x_focus = 0 , y_focus = 0, z_focus = 100e-3)


# Set the grid point spacing before lambert projection

required_resolution = 0.008

# Set the radius of the hemisphere 

radius = 0.11


# Add a rectilinear sampling grid to the world

lamb_sampler = world.add_sampler(lambert_sampler.LambertSampler(parent = world,
                                                                origin = np.array((0,0,0)),
                                                                radius = radius,
                                                                required_resolution = required_resolution))

# Propagate the acoustic field

world.propagate()

# Visualise the result

lamb_sampler.visualise_sampling_grid_and_array()

