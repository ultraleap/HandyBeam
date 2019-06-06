// This is the kernel for generating lambert sampling grid coordinates.

__kernel void _hbk_lamb_grid_sampler(
            __global float *cl_field,               // This is the output buffer for the sampling grid coordinates. 
            float delta,                            // This is the density parameter for the sampling grid.
            float radius,                           // This is the radius of the hemisphere.
            float N,                                // This is the length of the square grid that gets projected to the hemisphere.
            float x0, float y0, float z0            // These are the coordinates of the origin.
          )
          {

            // Get thread coordinates in the computational grid. 

            unsigned int idx_x = get_global_id(0);    

            unsigned int idx_y = get_global_id(1);

            unsigned int output_pointer_base = 3 * idx_x + (3 * N * idx_y );

            // Define variables for Lambert projection

            float x_base = (-1 + density * idx_x ) * root_2;
            float y_base = (-1 + density * idx_y ) * root_2;
            
            float rho = sqrt(x_base * x_base + y_base * y_base);
            float c = 2 * asin(0.5*rho);

            float phi = asin(cos(c)) / rho;
            float l = atan2( (x_base * sin(c)), -y_base*sin(c));
            float cos_phi = cos(phi);

            // Store coordinates 

            float lambert_x = radius * sin(phi);
            float lambert_y = radius * cos(l) * cos_phi;
            float lambert_z = radius * sin(l) * cos_phi;

            // Make comparison to ignore points with z < 0. 
            
            unsigned int comparator = rho_2 > (float) 2 | lambert_z < 0;
            
            // Output these pixel coordinates.

            cl_field[output_pointer_base+0] =  select((float) lambert_x + x0, NAN, comparator);
            cl_field[output_pointer_base+1] =  select((float) lambert_y + y0, NAN, comparator);
            cl_field[output_pointer_base+2] =  select((float) lambert_z + z0, NAN, comparator);

            }