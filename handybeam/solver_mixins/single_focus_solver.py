## Imports

from timeit import default_timer as timer
import numpy as np
import pyopencl as cl
import handybeam.tx_array

## Class

class SFSolverMixin():

    '''
    ---------------------------------------------
    SFSolverMixin
    ---------------------------------------------
    
    This is a mixin class for the compiled OpenCL kernel _hbk_sf_solver. It assigns
    the compiled OpenCL kernel to this Python class which can then be called by the appropriate
    solver class. 

    '''
    def __init__(self):

        '''
        ---------------------------------------------
        __init__()
        ---------------------------------------------
        
        This method intialises an instance of the mixin class SFSolverMixin.

        '''

        self._hbk_sf_solver = None        

    
    def _register_single_focus_solver(self):

        '''
        ---------------------------------------------
        _register_single_focus_solver()
        ---------------------------------------------

        This method assigns the compiled OpenCL propagator kernel _hbk_sf_solver to this 
        class and then sets the correct data types for the input to the assigned kernel.

        '''

        self._hbk_sf_solver = self.cl_system.compiled_kernels._hbk_sf_solver

        self._hbk_sf_solver.set_scalar_arg_dtypes([None,None,np.float32,np.float32,np.float32])

    def single_focus_solver(
                            self, 
                            tx_array: handybeam.tx_array.TxArray,
                            xf,yf,zf,
                            local_work_size = None,
                            print_performance_feedback = False):


        '''
        ---------------------------------------------
        single_focus_solver(tx_array, xf,yf,zf, local_work_size, print_performance_feedback)
        ---------------------------------------------

        This method determines the set of activation coefficients required to produce 
        a single focal point a given point in space. 
 
        Parameters
        ----------

        tx_array : handybeam.tx_array.TxArray
                This is a handybeam tx_array class. 
        xf : numpy float
                This is the x-coordinate of the requested focal point position.
        yf : numpy float
                This is the y-coordinate of the requested focal point position.
        zf : numpy float
                This is the z-coordinate of the requested focal point position.              
        local_work_size : tuple
                Tuple containing the local work sizes for the GPU.
        print_performance_feedback : boolean
                Boolean value determining whether or not to output the GPU performance.

        '''

        # Start the timer to measure wall time.

        t_start = timer()

        # Find the no of transducers.

        no_transducers = tx_array.element_count

        # Set global and local work sizes.

        thread_group_count=min(no_transducers, 32) 
        global_work_size = (no_transducers, 1, 1)
        local_work_size = (thread_group_count, 1, 1)
     
        # Create a numpy array, of the correct type, to store the transducer information.

        py_out_buffer = np.zeros(tx_array.tx_array_element_descriptor.shape,dtype = np.float32)

        # Create a buffer on the GPU to store the transducer information.

        cl_out_buffer = cl.Buffer(self.cl_system.context, cl.mem_flags.WRITE_ONLY, py_out_buffer.data.nbytes) 

        # Create a buffer on the GPU to store the transducer data and copy the data from the CPU (tx_array.tx_array_element_descriptor)
        # to the GPU.

        cl_tx_element_array_descriptor = cl.Buffer(self.cl_system.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=tx_array.tx_array_element_descriptor)

        # Create and execute an OpenCL event with the initialised queue, work sizes and data.

        cl_profiling_kernel_event = self._hbk_sf_solver(  self.cl_system.queue,
                                                                global_work_size,
                                                                local_work_size,
                                                                cl_tx_element_array_descriptor,
                                                                cl_out_buffer,
                                                                np.float32(xf),
                                                                np.float32(yf),
                                                                np.float32(zf)
                                                                )

        # Copy the results from the GPU buffer to the associated CPU buffer. 

        cl_profiling_mem_copy_event = cl.enqueue_copy(self.cl_system.queue,py_out_buffer, cl_out_buffer)
        
        # Block until the kernel event has completed and then until the copy event has completed. 

        cl_profiling_kernel_event.wait()   
                     
        cl_profiling_mem_copy_event.wait()

        # End the timer to measure the wall time.

        t_end = timer()

        t_elapsed_wall_time = t_end - t_start

        # If performance feedback requested then print. 

        if print_performance_feedback:
            ray_count = float(tx_array.element_count)
            output_buffer_size = py_out_buffer.data.nbytes
            self.print_performance_feedback(cl_profiling_kernel_event,
                                            cl_profiling_mem_copy_event,
                                            t_elapsed_wall_time,
                                            ray_count,
                                            output_buffer_size)

        return py_out_buffer
   