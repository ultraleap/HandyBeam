## Imports

import sys
sys.path.append("../.")
import numpy as np
import handybeam
import handybeam.world
import handybeam.evaluators
import matplotlib.colors as colors
from matplotlib import pyplot as plt

## Global variables

db_in_spl_50 = 0.006324555
db_in_spl_120 = 20
db_in_spl_148 = 502.377286302
db_in_spl_184 = 31697.863849222
db_in_spl_186 = 39905.246299378
db_in_spl_188 = 50237.728630192
db_in_spl_190 = 63245.553203368
db_in_spl_195 = 112468.26503807
db_in_spl_198 = 158865.646944856
db_in_spl_199 = 178250.187626749
db_in_spl_200 = 200000   
acoustic_impedance = 420
rms_factor = (np.sqrt(2) / 2)


## Class

class TestSamplingField():

    def __init__(self,parent = None):

        self.pressure_field = np.ones((20,20)) * db_in_spl_50
        self.area = 400 * 1e-6
        self.dict_count = None
        self.parent = parent
        
        self.set_pressure_field()
    
        self.area_1 = self.dict_count[db_in_spl_198] + self.dict_count[db_in_spl_199] + self.dict_count[db_in_spl_200]
        self.area_2 = self.dict_count[db_in_spl_195]
        self.area_3 = self.dict_count[db_in_spl_190]        
        self.area_4 = self.dict_count[db_in_spl_188]
        self.area_5 = self.dict_count[db_in_spl_186]
        self.area_6 = self.dict_count[db_in_spl_184]
        self.area_7 = self.dict_count[db_in_spl_120]
        self.area_8 = self.dict_count[db_in_spl_148]
        self.area_9 = self.dict_count[db_in_spl_50]
        
        self.vector_2d_metrics = None
        self.focal_spot_area = None
        self.focal_spot_contrast_connected_margin_area = None
        self.focal_spot_contrast_unconnected_margin_area = None
        self.focal_peak_pressure_to_sidelobe_ratio = None
        self.focal_intensity_to_total_intensity_ratio = None
        self.afi_2d = None
        self.ali_2d = None
        self.ahi_2d = None

    def set_pressure_field(self):    

        self.pressure_field[6:15,6:15] = db_in_spl_195
        self.pressure_field[8:13,8:13] = db_in_spl_198
        self.pressure_field[9:12,9:12] = db_in_spl_199
        self.pressure_field[10,10] = db_in_spl_200
        self.pressure_field[16:20,0:4] = db_in_spl_190
        self.pressure_field[17:20,17:20] = db_in_spl_188
        self.pressure_field[0:3,17:20] = db_in_spl_186
        self.pressure_field[0:2,0:2] = db_in_spl_184
        self.pressure_field[0:6,7:13] = db_in_spl_120
        self.pressure_field[15:20,8:13] = db_in_spl_148

        unique, counts = np.unique(self.pressure_field, return_counts=True)
        self.dict_count = dict(zip(unique, counts))
  

    def visualise(self):

        test_plate_db  = 20 * np.log10(self.pressure_field/ (2*10e-5))

        plt.imshow(test_plate_db,origin = 'lower' )
        plt.show()

    def calculate_metrics(self):

        self.focal_spot_area = self.area_1 * 1e-6
    
        self.focal_spot_contrast_connected_margin_area = self.area_2 * 1e-6

        self.focal_spot_contrast_unconnected_margin_area = self.area_3 * 1e-6
    
        self.focal_peak_pressure_to_sidelobe_ratio = db_in_spl_190 / db_in_spl_200


        focal_intensity = np.power(self.dict_count[db_in_spl_200] * db_in_spl_200 * rms_factor,2)/acoustic_impedance

        for count_1 in range(0,self.dict_count[db_in_spl_199]):

            focal_intensity += np.power(db_in_spl_199 * rms_factor,2)/acoustic_impedance 

        for count_2 in range(0,self.dict_count[db_in_spl_198]):

            focal_intensity += np.power(db_in_spl_198 * rms_factor,2)/acoustic_impedance 

        total_intensity = np.sum(np.power(self.pressure_field * rms_factor,2)/acoustic_impedance)

        self.focal_intensity_to_total_intensity_ratio = focal_intensity/ total_intensity

        self.afi_2d = ( (self.area_1 + self.area_2) * 1e-6) / np.power(self.parent.medium_wavelength,2)

        self.ali_2d = ((self.area_1 + self.area_2 + 
                        self.area_3 + self.area_4 +
                        self.area_5 + self.area_6 +
                        self.area_7 + self.area_8) * 1e-6 ) / np.power(self.parent.medium_wavelength,2)

        self.ahi_2d = ((self.area_1 + self.area_2 + 
                        self.area_3 + self.area_4 +
                        self.area_5 + self.area_6 +
                        self.area_8) * 1e-6 ) / np.power(self.parent.medium_wavelength,2)

        self.vector_2d_metrics = np.array(( 
                                    self.focal_spot_area,
                                    self.focal_spot_contrast_connected_margin_area,
                                    self.focal_spot_contrast_unconnected_margin_area,
                                    self.focal_peak_pressure_to_sidelobe_ratio,
                                    self.focal_intensity_to_total_intensity_ratio,
                                    self.afi_2d,
                                    self.ali_2d,
                                    self.ahi_2d
                                    )) 

                                
    
if __name__ == '__main__':

    # Initialise the world 

    world = handybeam.world.World()

    # Initialise evaluator object.
                                
    evaluator_2d = handybeam.evaluators.Evaluator2D()

    test_sampler = TestSamplingField(world)
    test_sampler.calculate_metrics()

    # Add sampling field.

    evaluator_2d.add_sampling_field(test_sampler)
    
    evaluator_results = evaluator_2d.find_area_metrics()

