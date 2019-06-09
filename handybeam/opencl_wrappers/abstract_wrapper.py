## Imports

import handybeam

## Class

class Wrapper():

    '''This is a template wrapper class for the OpenCL wrapper classes Propagator, Solver and
    Translator.

    '''

    def __init__(self):

        '''This method intialises an instance of the template wrapper class Wrapper.

        '''

        pass

    def print_performance_feedback(self,
                                   cl_profiling_kernel_event,
                                   cl_profiling_mem_copy_event,
                                   t_elapsed_wall_time,
                                   ray_count,
                                   output_buffer_size
                                   ):

        '''  This method ...

        .. ToDo::

             Jurek wrote this stuff so it's up to him to comment.

        Parameters
        ----------

        cl_profiling_kernel_event : TYPE
                            DESCRIPTION
        cl_profiling_mem_copy_event : TYPE
                            DESCRIPTION
        t_elapsed_Wall_time : TYPE
                            DESCRIPTION
        ray_count : TYPE
                            DESCRIPTION
        output_buffer_size : TYPE
                            DESCRIPTION

        '''


        measured_kernel_time = (cl_profiling_kernel_event.profile.end - cl_profiling_kernel_event.profile.start)  
        measured_kernel_fps = 1.0 / (measured_kernel_time * 1e-9)
        measured_mem_copy_time = cl_profiling_mem_copy_event.profile.end - cl_profiling_mem_copy_event.profile.start
        measured_mem_copy_fps = 1.0 / (measured_mem_copy_time * 1e-9)
        measured_command_enqueue_time = cl_profiling_mem_copy_event.profile.start - cl_profiling_kernel_event.profile.end
        measured_memory_copy_bandwidth_GBPS = (float(output_buffer_size) / 1024.0 / 1024.0 / 1024.0) / (measured_mem_copy_time * 1e-9)
        measured_command_bandwidth = 1.0 / (measured_command_enqueue_time * 1e-9)
        measured_compute_performance = ray_count / (measured_kernel_time * 1e-9)

        print('profiling: info:')
        print('profiling: wall time: {:0.4f}[sec] == {:0.1f}[FPS]'.format(t_elapsed_wall_time, 1.0 / t_elapsed_wall_time))
        print('profiling: kernel time : {:0.1f}[us] == {:0.1f}[FPS]'.format(measured_kernel_time * 1e-3,
                                                                            measured_kernel_fps))
        print('profiling: compute performance: {:0.1f}[MRays/sec]'.format(measured_compute_performance * 1e-6))
        print('profiling: memcopy time: {:0.1f}[us] == {:0.1f}[FPS]'.format(measured_mem_copy_time * 1e-3,
                                                                            measured_mem_copy_fps))
        print('profiling: memcopy bandwidth: {:0.1f}[GB/sec]'.format(measured_memory_copy_bandwidth_GBPS))
        print('profiling: command bandwidth: {:0.1f}[CPS]'.format(measured_command_bandwidth))
