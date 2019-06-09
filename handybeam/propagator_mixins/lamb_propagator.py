## Imports

from timeit import default_timer as timer
import numpy as np
import pyopencl as cl
import handybeam.tx_array

## Class

class LambPropMixin():

    '''
    ---------------------------------------------
    LambPropMixin
    ---------------------------------------------
    
    This is a mixin class for the compiled OpenCL kernel _hbk_lamb_propagator. It assigns
    the compiled OpenCL kernel to this Python class which can then be called by the appropriate
    sampler class. 

    '''

    def __init__(self):

        '''
        ---------------------------------------------
        __init__()
        ---------------------------------------------
        
        This method intialises an instance of the mixin class LambPropMixin.

        '''

        self._hbk_lamb_propagator = None        

    def _register_lamb_propagator(self):

        '''
        ---------------------------------------------
        _register_lamb_propagator()
        ---------------------------------------------

        This method assigns the compiled OpenCL propagator kernel _hbk_lamb_propagator to this 
        class and then sets the correct data types for the input to the assigned kernel.

        '''

        self._hbk_lamb_propagator = self.cl_system.compiled_kernels._hbk_lamb_propagator

        self._hbk_lamb_propagator.set_scalar_arg_dtypes([None,None,
                                                        np.float32,np.float32,np.float32,
                                                        np.float32,np.float32,np.float32,
                                                        np.int32])
                                                    

    def lamb_propagator(self,
                        tx_array: handybeam.tx_array.TxArray,
                        radius,
                        N,
                        delta,
                        x0, y0, z0,
                        local_work_size = (1,1,1),
                        print_performance_feedback = None
                        ):

        '''
        --------------------------------------------------------------------------------------------------------
        lamb_propagator( tx_array, radius, N, delta, x0, y0, z0, local_work_size,print_performance_feedback)
        --------------------------------------------------------------------------------------------------------

        This method simulates the acoustic pressure field on a lambert sampling grid. It does this by
        initialising a pressure field buffer on the CPU. It then passes the required information 
        to the appropriate OpenCl kernel and executes the computation of the pressure field on the GPU. This
        data is then copied over to the pressure field buffer on the CPU.
        
        Parameters
        ----------  

        tx_array : handybeam.tx_array.TxArray
                This is a handybeam tx_array class. 
        radius : numpy float / numpy int  
                This assigns the radius of the hemisphere sampling grid.
        N : numpy float / numpy int 
                This assigns 
        delta : numpy float
                Distance between adjacent sampling grid points.
        x0 : numpy float
                The x-coordinate of the origin of the sampling grid.
        y0 : numpy float
                The y-coordinate of the origin of the sampling grid.
        z0 : numpy float
                The z-coordinate of the origin of the sampling grid.         
        local_work_size : tuple
                Tuple containing the local work sizes for the GPU.
        print_performance_feedback : boolean
                Boolean value determining whether or not to output the GPU performance.

        '''

        # Set the types correctly.

        N = int(N)

        # Start the timer to measure wall time.

        t_start = timer()

        # Set the global work size for the GPU. 

        global_work_size = (N,N,1)

        # Number of transducers 

        tx_count = np.int(tx_array.element_count)
        
        # Create a numpy array, of the correct type, to store the real and imaginary pressure values for
        # the acoustic field. The format is:
        #  ( x,y,z,Real(p),Imag(p) ) 

        py_out_buffer = np.zeros((N,N,5),dtype = np.float32)
       
        # Create a buffer on the GPU to store the pressure values for the acoustic field.

        cl_field = cl.Buffer(self.cl_system.context, cl.mem_flags.WRITE_ONLY, py_out_buffer.data.nbytes) 

        # Create a buffer on the GPU to store the transducer data and copy the data from the CPU (tx_array.tx_array_element_descriptor)
        # to the GPU.

        cl_tx_element_array_descriptor = cl.Buffer(self.cl_system.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=tx_array.tx_array_element_descriptor)
        
        # Create and execute an OpenCL event with the initialised queue, work sizes and data.
        
        cl_profiling_kernel_event = self._hbk_lamb_propagator(  self.cl_system.queue,
                                                                global_work_size,
                                                                local_work_size,
                                                                cl_field,
                                                                cl_tx_element_array_descriptor,
                                                                np.float32(radius),
                                                                np.float32(N),
                                                                np.float32(delta),
                                                                np.float32(x0),
                                                                np.float32(y0),
                                                                np.float32(z0),
                                                                np.int(tx_count)
                                                            
                                                            )

        # Copy the results from the GPU buffer to the associated CPU buffer. 

        cl_profiling_mem_copy_event = cl.enqueue_copy(self.cl_system.queue,py_out_buffer, cl_field)
        
        # Block until the kernel event has completed and then until the copy event has completed. 

        cl_profiling_kernel_event.wait()                
        
        cl_profiling_mem_copy_event.wait()

        # End the timer to measure the wall time.

        t_end = timer()

        t_elapsed_wall_time = t_end - t_start

        # If performance feedback requested then print. 

        if print_performance_feedback:
            ray_count = float(tx_array.element_count * N * N)
            output_buffer_size = py_out_buffer.data.nbytes
            self.print_performance_feedback(cl_profiling_kernel_event,
                                            cl_profiling_mem_copy_event,
                                            t_elapsed_wall_time,
                                            ray_count,
                                            output_buffer_size)

        return py_out_buffer
   