// This is the kernel for generating rectilinear sampling grid coordinates.

 __kernel void _hbk_rect_grid_sampler(
          __global float *cl_out_buffer,          // This is the output buffer for the sampling grid coordinates. 
          float x_lim,                            // This is half the number of sampling points in the sampling grid along the x-axis.
          float y_lim,                            // This is half the number of sampling points in the sampling grid along the y-axis.
          float delta,                            // This is the spacing between adjacent points in the sampling grid.
          float x0, float y0, float z0,           // These are the coordinates of the origin.
          float v1x, float v1y, float v1z,        // These are the coordinates specifying the first unit vector.
          float v2x, float v2y, float v2z         // These are the coordinates specifying the second unit vector.
            )

            {

              // Set limits 
              
              float N_x = x_lim * 2;

              // Get thread coordinates in the computational grid. 

              unsigned int idx_x = get_global_id(0);    
              unsigned int idx_y = get_global_id(1);
              
              // Assign grid coordinates.

              float pixel_x_coordinate = (float) v1x*delta*(idx_x-x_lim) + v2x*delta*(idx_y-y_lim) + x0;
              float pixel_y_coordinate = (float) v1y*delta*(idx_x-x_lim) + v2y*delta*(idx_y-y_lim) + y0;
              float pixel_z_coordinate = (float) v1z*delta*(idx_x-x_lim) + v2z*delta*(idx_y-y_lim) + z0;

              // Output these pixel coordinates so that we can double check they match up with the python code. 
              
              unsigned int output_pointer_base = 3 * idx_x + (3 * N_x * idx_y );
                          
              cl_out_buffer[output_pointer_base+0] = pixel_x_coordinate;
              cl_out_buffer[output_pointer_base+1] = pixel_y_coordinate;
              cl_out_buffer[output_pointer_base+2] = pixel_z_coordinate;


            }