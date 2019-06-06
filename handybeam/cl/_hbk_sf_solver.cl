// This is the kernel for simple single point solver. 

__kernel void _hbk_sf_solver(
            __global float *cl_TxArrayDescriptor,           // This is the input buffer for the transducer information.
            __global float *cl_output_buffer,               // This is the output buffer for the transducer information.
            float focal_x_coordinate,                       // This is the x coordinate of the desired focal point.
            float focal_y_coordinate,                       // This is the y coordinate of the desired focal point.
            float focal_z_coordinate                        // This is the z coordinate of the desired focal point.
          )

          {
            // Get global ID to use to index the transducers.

            unsigned int tx_index = get_global_id(0);  

            // Unpack the relevant parts of the tx_array_descriptor

            unsigned int tx_pointer_base = 16 * tx_index;

            float tx_x = cl_TxArrayDescriptor[tx_pointer_base + 0];
            float tx_y = cl_TxArrayDescriptor[tx_pointer_base + 1];
            float tx_z = cl_TxArrayDescriptor[tx_pointer_base + 2];
 
            // Compute the distance between the focal point and the transducer. 

            float delta_x = focal_x_coordinate - tx_x;
            float delta_y = focal_y_coordinate - tx_y;
            float delta_z = focal_z_coordinate - tx_z;

            float recp_distance = rsqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z);

            float full_wavelengths = (1/recp_distance) * medium_wavenumber;

            float wrapped_wavelength =  fmin( full_wavelengths - floor(full_wavelengths), 0x1.fffffep-1f ) * tau;

            cl_output_buffer[tx_pointer_base + 0] = cl_TxArrayDescriptor[tx_pointer_base + 0]; 
            cl_output_buffer[tx_pointer_base + 1] = cl_TxArrayDescriptor[tx_pointer_base + 1]; 
            cl_output_buffer[tx_pointer_base + 2] = cl_TxArrayDescriptor[tx_pointer_base + 2]; 
            cl_output_buffer[tx_pointer_base + 3] = cl_TxArrayDescriptor[tx_pointer_base + 3]; 
            cl_output_buffer[tx_pointer_base + 4] = cl_TxArrayDescriptor[tx_pointer_base + 4]; 
            cl_output_buffer[tx_pointer_base + 5] = cl_TxArrayDescriptor[tx_pointer_base + 5]; 
            cl_output_buffer[tx_pointer_base + 6] = cl_TxArrayDescriptor[tx_pointer_base + 6]; 
            cl_output_buffer[tx_pointer_base + 7] = cl_TxArrayDescriptor[tx_pointer_base + 7]; 
            cl_output_buffer[tx_pointer_base + 8] = cl_TxArrayDescriptor[tx_pointer_base + 8]; 
            cl_output_buffer[tx_pointer_base + 9] = cl_TxArrayDescriptor[tx_pointer_base + 9]; 
            cl_output_buffer[tx_pointer_base + 10] = 1;
            cl_output_buffer[tx_pointer_base + 11] = (float)  - wrapped_wavelength ;
            cl_output_buffer[tx_pointer_base + 12] = cl_TxArrayDescriptor[tx_pointer_base + 12]; 
            cl_output_buffer[tx_pointer_base + 13] = cl_TxArrayDescriptor[tx_pointer_base + 13];
            cl_output_buffer[tx_pointer_base + 14] = cl_TxArrayDescriptor[tx_pointer_base + 14];
            cl_output_buffer[tx_pointer_base + 15] = cl_TxArrayDescriptor[tx_pointer_base + 15]; 
        

          }