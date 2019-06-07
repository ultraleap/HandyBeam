// This is the kernel for generating hexagonal sampling grid coordinates.

__kernel void _hbk_hex_grid_sampler(
            __global float *cl_field,               // This is the output buffer for the sampling grid coordinates. 
            float side_length,                      // This is the number of sampling points in the sampling grid along one side of the hexagon.
            float delta,                            // This is the spacing between adjacent points in the sampling grid.
            float x0, float y0, float z0,           // These are the coordinates of the origin.
            float v1x, float v1y, float v1z,        // These are the coordinates specifying the first unit vector.
            float v2x, float v2y, float v2z,        // These are the coordinates specifying the second unit vector.
            float lower_limit, float upper_limit    // These are the limits to help pick out the correct points for the sampling grid. 
          )

          {

            // Get thread coordinates in the computational grid. 

            unsigned int idx_x = get_global_id(0) + 1;    

            unsigned int idx_y = get_global_id(1) + 1;

            // Find sum of these indices

            unsigned int index_sum = idx_x + idx_y;

            // Define limits to make comparisons on the slanted grid

            unsigned int lower_compare = isless(index_sum, lower_limit);

            unsigned int upper_compare = isgreater(index_sum,upper_limit);

            if (lower_compare | upper_compare) return;

            // Assign grid coordiantes.
  
            float pixel_x_coordinate = (float) v1x*delta*(idx_x-side_length) + v2x*delta*(idx_y-side_length) + x0 ;
            float pixel_y_coordinate = (float) v1y*delta*(idx_x-side_length) + v2y*delta*(idx_y-side_length) + y0 ;
            float pixel_z_coordinate = (float) v1z*delta*(idx_x-side_length) + v2z*delta*(idx_y-side_length) + z0 ;
            
            // Output these pixel coordinates so that we can double check they match up with the python code. 

            unsigned int output_pointer_base = 3 * ( idx_x - 1 ) + (3 * (  ( 2 * side_length ) - 1 )  * ( idx_y - 1 )  );
           
            cl_field[output_pointer_base+0] = pixel_x_coordinate;
            cl_field[output_pointer_base+1] = pixel_y_coordinate;
            cl_field[output_pointer_base+2] = pixel_z_coordinate;

          }