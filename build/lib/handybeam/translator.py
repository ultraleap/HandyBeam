## Imports

import handybeam.opencl_wrappers.translator_wrappers as hb_translator_wrappers

## Class

class Translator():

    '''
    ---------------------------------------------
    Translator
    ---------------------------------------------
    
    This class calls the OpenCL wrapper for the translator functions.

    '''

    def __init__(self,parent = None):


        '''
        ---------------------------------------------
        __init__(parent)
        ---------------------------------------------
        
        This method intialises an instance of class Translator.

        Parameters
        ----------

        parent : handybeam world
                This is an instance of the handybeam world class.
        
        '''
        
        self.parent = parent
        self.translator = hb_translator_wrappers.Translator(parent = self.parent)

    
    def xy_translate(self,x_translate,y_translate,plane_height,local_work_size = (1,1,1),print_performance_feedback= False):

        '''
        ---------------------------------------------
        xy_translate(x_translate,y_translate,plane_height,local_work_size,print_performance_feedback)
        ---------------------------------------------
        
        This method calls the OpenCL wrapper mixin class xy_translator which translates 
        a given focal point, created at a height plane_height,by a distance x_translate
        along the x-axis and y_translate along the y-axis.

        Parameters
        ----------

        x_translate : numpy float
                This is the desired distance to translate the focal point along the x-axis. 
        y_translate : numpy float
                This is the desired distance to translate the focal point along the y-axis. 
        plane_height : numpy float
                This is the z-coordinate of the focal point position.              
        local_work_size : tuple
                Tuple containing the local work sizes for the GPU.
        print_performance_feedback : boolean
                Boolean value determining whether or not to output the GPU performance.

        '''

        kernel_output = self.translator.xy_translator(    
                                                            self.parent.tx_array,
                                                            x_translate,y_translate,plane_height,
                                                            local_work_size = local_work_size,
                                                            print_performance_feedback = print_performance_feedback
                                                        )

        self.parent.tx_array.tx_array_element_descriptor = kernel_output

    def xyz_translate(self,x_focus,y_focus,z_focus,x_translate,y_translate,z_translate,
                    local_work_size = (1,1,1),print_performance_feedback = False):

        '''
        ---------------------------------------------
        xyz_translate(x_focus,y_focus,z_focus,x_translate,y_translate,z_translate,local_work_size,print_performance_feedback)
        ---------------------------------------------
        
        This method calls the OpenCL wrapper mixin class xyz_translator which translates a given focal point, created at a height plane_height,
        by a distance x_translate along the x-axis and y_translate along the y-axis.

        Parameters
        ----------

        x_focus : numpy float
                This is the x-coordinate of the original focal point position. 
        y_focus : numpy float
                This is the y-coordinate of the original focal point position. 
        z_focus : numpy float
                This is the z-coordinate of the original focal point position. 
        x_translate : numpy float
                This is the desired distance to translate the focal point along the x-axis. 
        y_translate : numpy float
                This is the desired distance to translate the focal point along the y-axis. 
        z_translate : numpy float
                This is the desired distance to translate the focal point along the z-axis. 
        local_work_size : tuple
                Tuple containing the local work sizes for the GPU.
        print_performance_feedback : boolean
                Boolean value determining whether or not to output the GPU performance.

        '''
        kernel_output = self.translator.xyz_translator(    
                                                            self.parent.tx_array,
                                                            x_focus,y_focus,z_focus,
                                                            x_translate,y_translate,z_translate,
                                                            local_work_size = local_work_size,
                                                            print_performance_feedback = print_performance_feedback
                                                        )

        self.parent.tx_array.tx_array_element_descriptor = kernel_output

     
    def set_parent(self, new_parent):
        
        '''
        ---------------------------------------------
        set_parent(parent)
        ---------------------------------------------
        
        This method changes the parent of an instance of the class Translator.

        Parameters
        ----------

        parent : handybeam world
                This is an instance of the handybeam world class.
        
        '''

        self.parent = new_parent


    
