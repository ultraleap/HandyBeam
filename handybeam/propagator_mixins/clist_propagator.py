# # Imports

from timeit import default_timer as timer
import numpy as np
import pyopencl as cl
import handybeam .tx_array

# # Class


class ClistPropMixin():
    """This is a mixin class for the compiled OpenCL kernel _hbk_clist_propagator. It assigns
    the compiled OpenCL kernel to this Python class which can then be called by the appropriate
    sampler class. 

    """

    def __init__(self):
        """This method intialises an instance of the mixin class ClistPropMixin.

        """

        self._hbk_clist_propagator = None

    def _register_clist_propagator(self):
        """This method assigns the compiled OpenCL propagator kernel _hbk_clist_propagator to this
        class and then sets the correct data types for the input to the assigned kernel.

        """
        self._hbk_clist_propagator = self.cl_system.compiled_kernels._hbk_clist_propagator
        self._hbk_clist_propagator.set_scalar_arg_dtypes([None, None, None, np.uint32, np.uint32])

    def clist_propagator(self,
                         tx_array: handybeam.tx_array.TxArray,
                         sampling_point_list=np.zeros((0, 3), dtype=np.float32),
                         local_work_size=(2, 1, 1),
                         print_performance_feedback=False
                         ):

        """This method simulates the acoustic pressure field on a set of provided sampling points. It does this by
        initialising a pressure field buffer on the CPU. It then passes the required information 
        to the appropriate OpenCl kernel and executes the computation of the pressure field on the GPU. This
        data is then copied over to the pressure field buffer on the CPU.

        Parameters
        ----------

        tx_array : handybeam.tx_array.TxArray
                This is a handybeam tx_array class. 
        sampling_point_list : numpy array
                Numpy array containing the list of requested sampling point coordinates.
        local_work_size : tuple
                Tuple containing the local work sizes for the GPU.
        print_performance_feedback : boolean
                Boolean value determining whether or not to output the GPU performance.

        """



        # Start the timer to measure wall time.

        t_start = timer()

        # make sure the point list is of the right shape and size
        assert sampling_point_list.shape[1] == 3
        assert sampling_point_list.dtype == np.float32

        # Determine the number of requested sampling points.

        sampling_point_count = sampling_point_list.shape[0]
        
        # Create a numpy array, of the correct type, to store the pressure values for
        # acoustic field.

        py_out_buffer = np.zeros((sampling_point_count,2),dtype = np.float32)

        # Create a buffer on the GPU to store the pressure values for the acoustic field.
        
        cl_field = cl.Buffer(self.cl_system.context, cl.mem_flags.WRITE_ONLY, py_out_buffer.data.nbytes) 

        # Create a buffer on the GPU to store the transducer data and copy the data from the CPU (tx_array.tx_array_element_descriptor)
        # to the GPU.
        py_tx_array_element_descriptor = np.float32(tx_array.tx_array_element_descriptor)
        cl_tx_element_array_descriptor = cl.Buffer(self.cl_system.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=py_tx_array_element_descriptor)
        
        # Create a buffer on the GPU to store the sampling point data and copy the data from the CPU (sampling_point_list)
        # to the GPU.

        cl_sampling_point_list = cl.Buffer(self.cl_system.context,cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=sampling_point_list)
        
        # Set the global work size for the GPU. 

        global_work_size_x = np.int32(np.ceil((sampling_point_count/local_work_size[0]))*local_work_size[0])

        if print_performance_feedback:
            print('sampling_point_count={}'.format(sampling_point_count))
            print('global_work_size_x={}'.format(global_work_size_x))

        global_work_size_y = 1
        global_work_size_z = 1

        global_work_size = [global_work_size_x, global_work_size_y, global_work_size_z]

        # Create and execute an OpenCL event with the initialised queue, work sizes and data.

        cl_profiling_kernel_event = self._hbk_clist_propagator(     self.cl_system.queue,  
                                                                    global_work_size,  
                                                                    local_work_size,  
                                                                    cl_tx_element_array_descriptor,
                                                                    cl_sampling_point_list,
                                                                    cl_field,
                                                                    tx_array.element_count,
                                                                    sampling_point_count                                                                       
                                                                )

        # Copy the results from the GPU buffer to the associated CPU buffer. 

        cl_profiling_mem_copy_event = cl.enqueue_copy(self.cl_system.queue, py_out_buffer, cl_field)


        # Block until the kernel event has completed and then until the copy event has completed. 

        cl_profiling_kernel_event.wait()     

        cl_profiling_mem_copy_event.wait()

        # End the timer to measure the wall time.

        t_end = timer()

        t_elapsed_wall_time = t_end - t_start
         
        # If performance feedback requested then print. 
        
        if print_performance_feedback:
            ray_count = float(tx_array.element_count * sampling_point_count)
            output_buffer_size = py_out_buffer.data.nbytes
            self.print_performance_feedback(cl_profiling_kernel_event,
                                            cl_profiling_mem_copy_event,
                                            t_elapsed_wall_time,
                                            ray_count,
                                            output_buffer_size)

        return py_out_buffer

