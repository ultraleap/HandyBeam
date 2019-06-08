"""

.. _evaluators:

=====================================
module: :code:`handybeam.evaluators`
=====================================

Contains methods to measure various things about the acoustic field.

Typically applied AFTER the acoustic field calculation is complete.

Could be used for numerical optimisation runs.


"""
## Imports

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import handybeam.samplers.clist_sampler as clist_sampler


# Global variables

acoustic_impedance = 420.0
""" constant for evaluations. default: air=420.0
"""

rms_factor = (np.sqrt(2) / 2)
""" constant. 
"""

# Please use this as reference for opencv thresholding functions. 
#  https://docs.opencv.org/3.4/d7/d1b/group__imgproc__misc.html#ggaa9e58d2860d4afa658ef70a9b1115576a147222a96556ebc1d948b372bcd7ac59

# Class


#### TODO - Need to change the intensity stuff to match up with what is in now in the surface metrics stuff

class Evaluator3D():
    '''
    ---------------------------------------------
    Evaluator3D
    ---------------------------------------------
    
    DESCRIPTION HERE

    '''

    def __init__(self):

        '''
        ---------------------------------------------
        __init__()
        ---------------------------------------------
            
        DESCRIPTION HERE

        '''
        self.volume_sampling_field = None
        self.afi_3d = None
        self.ali_3d = None
        self.ahi_3d = None
        self.vector_3d_metrics = None

    def add_sampling_field(self, volume_sampling_field):
        

        '''
        ---------------------------------------------
        add_sampling_field(volume_sampling_field)
        ---------------------------------------------
            
        DESCRIPTION HERE

        Parameters
        ----------

        volume_sampling_field : DESCRIPTION HERE
                DESCRIPTION HERE

        '''
        self.volume_sampling_field = volume_sampling_field

    def find_volume_metrics(self):

        '''
        ---------------------------------------------
        find_volume_metrics()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''

        self.find_afi_3d()
        self.find_ali_3d()
        self.find_ahi_3d()

        self.vector_3d_metrics = np.array((self.afi_3d, self.ali_3d, self.ahi_3d))

        return self.vector_3d_metrics

    def find_afi_3d(self):

        '''
        ---------------------------------------------
        find_afi_3d()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        volume_pressure_field = self.volume_sampling_field.pressure_field

        # Find the peak pressure in the sampled field.

        peak_pressure  = np.max(volume_pressure_field)

        # Find the pressure that is -6dB from the peak. 

        neg_six_dB_value = peak_pressure * np.power(10, -6/20)

        # Set bounds.

        lower_bound = np.float((neg_six_dB_value))
        upper_bound = np.float((peak_pressure))

        # Find no focal points above -6dB from the peak.

        no_focal_points = len(volume_pressure_field[volume_pressure_field > lower_bound].ravel())

        # Find total number of points.

        total_points = len(volume_pressure_field.ravel())

        # Find fraction of volume greater than -6dB.

        fraction_of_volume = no_focal_points / total_points

        # Find the volume greater than -6dB.

        self.afi_3d = (fraction_of_volume * self.volume_sampling_field.volume) \
                / np.power(self.volume_sampling_field.parent.medium_wavelength, 3)

    def find_ali_3d(self):
        
        '''
        ---------------------------------------------
        find_ali_3d()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        volume_pressure_field = self.volume_sampling_field.pressure_field

        # Find the peak pressure in the sampled field.

        peak_pressure  = np.max(volume_pressure_field)

        # Find the lenor threshold pressure. 

        lenor_threshold = 2 * np.power(float(10), -5) * np.power(10, 110/20)

        # Set the bounds. 

        lower_bound = np.float((lenor_threshold))
        upper_bound = np.float((peak_pressure))

        # Find no points above the lenor threshold limit. 

        no_focal_points = len(volume_pressure_field[volume_pressure_field > lower_bound].ravel())

        # Find total no of points. 

        total_points = len(volume_pressure_field.ravel())

        # Find the fraction of the volume greater than lenor threshold.

        fraction_of_volume = no_focal_points / total_points

        # Find the normalised volume greater than lenor threshod.  

        self.ali_3d = (fraction_of_volume * self.volume_sampling_field.volume) \
                / np.power(self.volume_sampling_field.parent.medium_wavelength, 3)
               
    def find_ahi_3d(self):

        '''
        ---------------------------------------------
        find_ahi_3d()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        volume_pressure_field = self.volume_sampling_field.pressure_field

        # Find the peak pressure in the sampled field.

        peak_pressure  = np.max(volume_pressure_field)

        # Find the haptic threshold pressure. 

        haptic_threshold = 2 * np.power(float(10), -5) * np.power(10, 146/20)

        # Set the bounds. 

        lower_bound = np.float((haptic_threshold))
        upper_bound = np.float((peak_pressure))

        # Find no points above the lenor threshold limit. 

        no_focal_points = len(volume_pressure_field[volume_pressure_field > lower_bound].ravel())

        # Find total no of points. 

        total_points = len(volume_pressure_field.ravel())

        # Find the fraction of the volume greater than lenor threshold.

        fraction_of_volume = no_focal_points / total_points

        # Find the normalised volume greater than lenor threshod.  

        self.ahi_3d = (fraction_of_volume * self.volume_sampling_field.volume) \
                / np.power(self.volume_sampling_field.parent.medium_wavelength, 3)
               
    
class Evaluator2D():

    '''
    ---------------------------------------------
    Evaluator2D
    ---------------------------------------------
    
    DESCRIPTION HERE

    '''


    def __init__(self):

        '''
        ---------------------------------------------
        __init__()
        ---------------------------------------------
            
        DESCRIPTION HERE

        '''

        self.plane_sampling_field = None
        self.focal_spot_area = None
        self.focal_spot_contrast_connected_margin_area = None
        self.focal_spot_contrast_unconnected_margin_area = None
        self.focal_peak_pressure_to_sidelobe_ratio = None
        self.focal_intensity_to_total_intensity_ratio = None
        self.afi_2d = None
        self.ali_2d = None
        self.ahi_2d = None
        self.vector_2d_metrics = None

    def add_sampling_field(self, plane_sampling_field):
        
        '''
        ---------------------------------------------
        add_sampling_field(plane_sampling_field)
        ---------------------------------------------
            
        DESCRIPTION HERE

        Parameters
        ----------

        plane_sampling_field : DESCRIPTION HERE
                DESCRIPTION HERE

        '''
        self.plane_sampling_field = plane_sampling_field
   
    def find_area_metrics(self):

        '''
        ---------------------------------------------
        find_area_metrics()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        self.find_focal_spot_area()
        self.find_focal_spot_contrast_connected_margin_area()
        self.find_focal_spot_contrast_unconnected_margin_area()
        self.find_focal_intensity_to_total_intensity_ratio()
        self.find_focal_peak_pressure_to_peak_sidelobe_ratio()
        self.find_afi_2d()
        self.find_ali_2d()
        self.find_ahi_2d()

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

        return self.vector_2d_metrics

    def find_focal_spot_area(self):

        '''
        ---------------------------------------------
        find_focal_spot_area()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        plane_pressure_field = np.abs(self.plane_sampling_field.pressure_field)

        # Find the peak pressure in the sampled field.

        peak_pressure = np.max(plane_pressure_field)

        # Find the pressure that is -3dB from the peak.

        neg_three_dB_value = peak_pressure * np.power(10, -3/20)
        
        # This mask sets everything less than 3dB to zero and everything above 3dB to 1.

        ret ,thresh_3dB = cv.threshold(plane_pressure_field, neg_three_dB_value, 1, cv.THRESH_BINARY)

        ret = None

        # Find the total number of sampling points.

        total_pixels = len(thresh_3dB.ravel())

        # Find the number of sampling points above -3dB threshold.

        no_3dB_pixels = np.sum(thresh_3dB)

        # Calculate fraction of pixels above -3dB threshold.

        pixel_3dB_area = no_3dB_pixels / total_pixels

        # Find area that is above -3dB

        self.focal_spot_area = pixel_3dB_area * self.plane_sampling_field.area

    def find_focal_spot_contrast_connected_margin_area(self):
        
        '''
        ---------------------------------------------
        find_focal_spot_contrast_connected_margin_area()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        plane_pressure_field = np.abs(self.plane_sampling_field.pressure_field)

        # Find the peak pressure in the sampled field.

        peak_pressure = np.max(plane_pressure_field)

        # Find the pressure that is -3dB from the peak.

        neg_three_dB_value = peak_pressure * np.power(10, -3/20)

        # Find the pressure that is -6dB from the peak.

        neg_six_dB_value = peak_pressure * np.power(10, -6/20)

        # This mask sets everything less than -3dB to zero and everything above 3dB to 1.

        ret,  thresh_3dB = cv.threshold(plane_pressure_field, neg_three_dB_value, 1,  cv.THRESH_BINARY)

        ret = None

        # This mask sets everything greater than -3dB to zero and everything above 3dB to 1.

        ret,  thresh_3dB_inv = cv.threshold(plane_pressure_field, neg_three_dB_value,  1, cv.THRESH_TOZERO_INV)

        ret = None

        # This mask sets everything less than -6dB to zero and 
        # everything above -6dB and less than -3dB to 1.

        ret,  thresh_6dB = cv.threshold(thresh_3dB_inv,  neg_six_dB_value, 1, cv.THRESH_BINARY)

        ret = None

        # Find the total number of sampling points.

        total_pixels = len(thresh_3dB.ravel())

        # Calculate fraction of pixels above -3dB threshold.

        no_3dB_pixels = np.sum(thresh_3dB)

        # Calculate fraction of pixels above -6dB and less than -3dB threshold.

        no_6dB_pixels = np.sum(thresh_6dB)
    

        pixel_6dB_annulus_area = no_6dB_pixels / total_pixels

        # Calculate area above -6dB and less than -3dB threshold.

        self.focal_spot_contrast_connected_margin_area = pixel_6dB_annulus_area * self.plane_sampling_field.area

    def find_focal_peak_pressure_to_peak_sidelobe_ratio(self):

        '''
        ---------------------------------------------
        find_focal_peak_pressure_to_peak_sidelobe_ratio()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        plane_pressure_field = np.abs(self.plane_sampling_field.pressure_field)

        # Find the peak pressure in the sampled field.

        peak_pressure  = np.max(plane_pressure_field)

        # Cut out -6db from the peak.

        neg_six_dB_value = peak_pressure * np.power(10, -6/20)

        # Set all pixel values greater than -3dB drop from peak pressure to 0.

        ret,  thresh_6dB_inv = cv.threshold(plane_pressure_field, neg_six_dB_value, 1, cv.THRESH_TOZERO_INV)

        ret = None
        
        # Calculate peak sidelobe pressure.

        peak_sidelobe_pressure = np.max(thresh_6dB_inv)

        # Calculate ratio.

        self.focal_peak_pressure_to_sidelobe_ratio = peak_sidelobe_pressure / peak_pressure
    
    def find_focal_intensity_to_total_intensity_ratio(self):

        '''
        ---------------------------------------------
        find_focal_intensity_to_total_intensity_ratio()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        plane_pressure_field = np.abs(self.plane_sampling_field.pressure_field)

        # Find the peak pressure in the sampled field.

        peak_pressure  = np.max(plane_pressure_field)

        # Find the pressure that is -3dB from the peak.

        neg_three_dB_value = peak_pressure * np.power(10, -3/20)

        # Set all pixel values less than -3dB drop from peak pressure to 0

        ret,  thresh_3dB = cv.threshold(plane_pressure_field, neg_three_dB_value, 1, cv.THRESH_TOZERO)

        ret = None

        # Calculate rms pressure in the focal region.

        rms_thresh_pressure = rms_factor * thresh_3dB

        # Calculate focal region intensity.
        
        focal_intensity = np.sum( np.power(rms_thresh_pressure, 2) / acoustic_impedance )

        # Calculate rms pressure in entire sampling field.
        
        rms_total_pressure = rms_factor * plane_pressure_field

        # Calculate total intensity in entire sampling field.

        total_intensity = np.sum( np.power(rms_total_pressure, 2) / acoustic_impedance )

        # Calculate ratio. 

        self.focal_intensity_to_total_intensity_ratio = focal_intensity / total_intensity

    def find_focal_spot_contrast_unconnected_margin_area(self):

        '''
        ---------------------------------------------
        find_focal_spot_contrast_unconnected_margin_area()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''

        plane_pressure_field = np.abs(self.plane_sampling_field.pressure_field)

        # Find the total number of sampling points.

        total_pixels = len(plane_pressure_field.ravel())
        
        # Find the peak pressure in the sampled field.

        peak_pressure  = np.max(plane_pressure_field)

        # Find the pressure that is -18dB from the peak. (had to use this to seperate the blobs)

        neg_18_dB_value = peak_pressure * np.power(10, -18/20)
        
        lower_bound = np.float((neg_18_dB_value))
        upper_bound = np.float((peak_pressure))

        # Mask everything outside the range of the bounds.

        plane_pressure_field = cv.copyMakeBorder(plane_pressure_field, top=1, bottom=1, left=1, right=1,
                         borderType= cv.BORDER_CONSTANT, value=[1,1,1] )

        mask = cv.inRange(plane_pressure_field, lower_bound, upper_bound)     

        # Find contours of the blobs within the bounds.

        im2,  contours,  hierarchy = cv.findContours(mask,  cv.RETR_TREE,  cv.CHAIN_APPROX_SIMPLE)


        # Sort contours by area

        contours.sort(key = lambda s: cv.contourArea(s))

        # Fill the largest contour area for plotting purposes.

        cv.fillPoly(mask,  pts =[contours[-1]],  color=(0, 0, 0))

        # Remove the focal spot contour from the list of contours ( assuming it has the largest area).

        contours = contours[0:len(contours)-1]

        # Draw contours for debug purposes. 

        contour_image_red = cv.drawContours(mask,  contours,  -1, (0, 255, 0))

        if contours == []:

            self.focal_spot_contrast_unconnected_margin_area = 0

            return 

        else:

            ### CHECK THIS WITH JUREK 

            # Cannot calculate the blob size exactly - counts -1 on the side length

            # Calculate the size of the largest remaining blobs 

            no_blob_pixels = cv.contourArea(contours[-1])

            no_blob_pixels = np.power(np.sqrt(no_blob_pixels) + 1,2)

            # Determine fraction of pixels in largest unconnected noise area.

            pixel_unconnected_noise_area = no_blob_pixels / total_pixels

            self.focal_spot_contrast_unconnected_margin_area = pixel_unconnected_noise_area * self.plane_sampling_field.area
        
    def find_afi_2d(self):

        '''
        ---------------------------------------------
        find_afi_2d()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        plane_pressure_field = np.abs(self.plane_sampling_field.pressure_field)

        # Find the peak pressure in the sampled field.

        peak_pressure = np.max(plane_pressure_field)

        # Find the pressure that is -6dB from the peak. 

        neg_six_dB_value = peak_pressure * np.power(10, -6/20)

        # This mask sets everything less than 6dB to zero and everything above 6dB to 1.

        ret ,thresh_6dB = cv.threshold(plane_pressure_field, neg_six_dB_value, 1, cv.THRESH_BINARY)

        ret = None

        # Find the total number of sampling points.

        total_pixels = len(thresh_6dB.ravel())

        # Find the number of sampling points above -6dB threshold.

        no_6dB_pixels = np.sum(thresh_6dB)
        
        # Calculate fraction of pixels above -6dB threshold.

        pixel_6dB_area = no_6dB_pixels / total_pixels

        # Find area that is above -6dB

        focal_area = pixel_6dB_area * self.plane_sampling_field.area

        # Find normalised area.

        self.afi_2d = (focal_area) \
                / np.power(self.plane_sampling_field.parent.medium_wavelength, 2)
       
    def find_ali_2d(self):

        '''
        ---------------------------------------------
        find_ali_2d()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        plane_pressure_field = np.abs(self.plane_sampling_field.pressure_field)

        # Find the peak pressure in the sampled field.

        peak_pressure  = np.max(plane_pressure_field)

        # Find the lenor threshold pressure. 

        lenor_threshold = 2 * np.power(float(10), -5) * np.power(10, 110/20)

        # This mask sets everything less than lenor threshold to zero and everything above 6dB to 1.

        ret ,thresh_lenor = cv.threshold(plane_pressure_field, lenor_threshold, 1, cv.THRESH_BINARY)

        ret = None

        # Find the total number of sampling points.

        total_pixels = len(thresh_lenor.ravel())

        # Find the number of sampling points above lenor threshold.

        no_lenor_pixels = np.sum(thresh_lenor)
        
        # Calculate fraction of pixels above lenor threshold.

        pixel_lenor_area = no_lenor_pixels / total_pixels

        # Find area that is above lenor threshold.

        lenor_area = pixel_lenor_area * self.plane_sampling_field.area

        # Find normalised area.

        self.ali_2d = (lenor_area) \
                / np.power(self.plane_sampling_field.parent.medium_wavelength, 2)

    def find_ahi_2d(self):

        '''
        ---------------------------------------------
        find_ahi_2d()
        ---------------------------------------------
            
        DESCRIPTION HERE
                
        '''
        plane_pressure_field = np.abs(self.plane_sampling_field.pressure_field)

        # Find the peak pressure in the sampled field.

        peak_pressure  = np.max(plane_pressure_field)

        # Find the haptic threshold pressure.  (this needs editing)

        haptic_threshold = 2 * np.power(float(10), -5) * np.power(10, 146/20)

        # This mask sets everything less than haptic threshold to zero and everything above 6dB to 1.

        ret ,thresh_haptic = cv.threshold(plane_pressure_field, haptic_threshold, 1, cv.THRESH_BINARY)

        ret = None

        # Find the total number of sampling points.

        total_pixels = len(thresh_haptic.ravel())

        # Find the number of sampling points above haptic threshold.

        no_haptic_pixels = np.sum(thresh_haptic)
        
        # Calculate fraction of pixels above lenor threshold.

        pixel_haptic_area = no_haptic_pixels / total_pixels

        # Find area that is above haptic threshold.

        haptic_area = pixel_haptic_area * self.plane_sampling_field.area

        # Find normalised area.

        self.ahi_2d = (haptic_area) \
                / np.power(self.plane_sampling_field.parent.medium_wavelength, 2)
