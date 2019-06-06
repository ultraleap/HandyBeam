## Imports

import sys
sys.path.append("../../.")

import numpy as np
import handybeam_core
import handybeam_core.world
import handybeam_core.evaluators
import matplotlib.colors as colors
from matplotlib import pyplot as plt

## Global variables

db_in_spl_50 = 0.006324555
db_in_spl_120 = 20
db_in_spl_148 = 502.377286302
db_in_spl_198 = 158865.646944856
db_in_spl_199 = 178250.187626749
db_in_spl_200 = 200000   
acoustic_impedance = 420
rms_factor = (np.sqrt(2) / 2)


## Class

class TestSamplingField():

    def __init__(self,parent = None):

        self.pressure_field = np.ones((100,100,100)) * db_in_spl_50
        self.volume = 100*100*100 * 1e-9
        self.dict_count = None
        self.parent = parent
        
        self.set_pressure_field()
    
        self.volume_1 = self.dict_count[db_in_spl_198] + self.dict_count[db_in_spl_199] + self.dict_count[db_in_spl_200]
        self.volume_2 = self.dict_count[db_in_spl_148]
        self.volume_3 = self.dict_count[db_in_spl_120]        
        self.volume_4 = self.dict_count[db_in_spl_50]

        
        self.vector_3d_metrics = None
        self.afi_3d = None
        self.ali_3d = None
        self.ahi_3d = None
    
    def set_pressure_field(self):    

        self.pressure_field[45:47,45:47,45:47] = db_in_spl_198
        self.pressure_field[49:51,49:51,49:51] = db_in_spl_200
        self.pressure_field[47:49,47:49,47:49] = db_in_spl_199
        self.pressure_field[3:6,3:6,3:6] = db_in_spl_120
        self.pressure_field[80:86,80:86,80:86] = db_in_spl_148

        unique, counts = np.unique(self.pressure_field, return_counts=True)
        self.dict_count = dict(zip(unique, counts))

    def calculate_metrics(self):
    
        self.afi_3d = self.volume_1 * 1e-9 / np.power(self.parent.medium_wavelength,3)

        self.ali_3d = ((self.volume_1 + self.volume_2 + self.volume_3) * 1e-9) / np.power(self.parent.medium_wavelength,3)
        self.ahi_3d = ((self.volume_1 + self.volume_2) * 1e-9) / np.power(self.parent.medium_wavelength,3)

        self.vector_3d_metrics = np.array(( 
                                    self.afi_3d,
                                    self.ali_3d,
                   
                                   self.ahi_3d
                                    )) 

if __name__ == '__main__':

    # Initialise the world 

    world = handybeam_core.world.World()

    # Initialise evaluator object.
                                
    evaluator_3d = handybeam_core.evaluators.Evaluator3D()

    test_sampler = TestSamplingField(world)

    test_sampler.calculate_metrics()

    # Add sampling field.

    evaluator_3d.add_sampling_field(test_sampler)
    
    evaluator_results = evaluator_3d.find_volume_metrics()

    