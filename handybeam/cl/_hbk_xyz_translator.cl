// This is the kernel for translating focal point along the z-axis.
    
__kernel void _hbk_xyz_translator(
            __global float *cl_TxArrayDescriptor,           // This is the input buffer for the transducer information.
            __global float *cl_output_buffer,               // This is the output buffer for the transducer information.
            float focal_x_coordinate,                       // This is the x coordinate of the focal point to be translated.
            float focal_y_coordinate,                       // This is the y coordinate of the focal point to be translated.
            float focal_z_coordinate,                       // This is the z coordinate of the focal point to be translated.
            float x_translate,                              // This is the distance to translate the focal points in the x-axis.
            float y_translate,                              // This is the distance to translate the focal points in the y-axis.
            float z_translate                               // This is the distance to translate the focal points in the z-axis.
          )

          {

            // Get global ID to use to index transducers.

            unsigned int tx_index = get_global_id(0);    
 
            // Unpack the relevant parts of the tx_array_descriptor

            unsigned int tx_pointer_base = 16 * tx_index;

            float tx_x = cl_TxArrayDescriptor[tx_pointer_base + 0];
            float tx_y = cl_TxArrayDescriptor[tx_pointer_base + 1];
            float tx_z = cl_TxArrayDescriptor[tx_pointer_base + 2];
            
            float tx_phase = cl_TxArrayDescriptor[tx_pointer_base + 11];
                
            // Calculate distance to original focal point.

            float delta_x = focal_x_coordinate - tx_x;
            float delta_y = focal_y_coordinate - tx_y;
            float delta_z = focal_z_coordinate - tx_z;

            float recp_original_distance = rsqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z);

            // Calculate change in phase (approximated using binomial expansion).

            float delta_phase = - translation_medium_wavenumber * (delta_x * x_translate + delta_y * y_translate + delta_z * z_translate) * recp_original_distance;

            // Output these pixel coordinates so that we can double check they match up with the python code. 
           
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
            cl_output_buffer[tx_pointer_base + 10] = cl_TxArrayDescriptor[tx_pointer_base + 10]; 
            cl_output_buffer[tx_pointer_base + 11] = (float) tx_phase + delta_phase;    
            cl_output_buffer[tx_pointer_base + 12] = cl_TxArrayDescriptor[tx_pointer_base + 12]; 
            cl_output_buffer[tx_pointer_base + 13] = cl_TxArrayDescriptor[tx_pointer_base + 13];
            cl_output_buffer[tx_pointer_base + 14] = cl_TxArrayDescriptor[tx_pointer_base + 14];
            cl_output_buffer[tx_pointer_base + 15] = cl_TxArrayDescriptor[tx_pointer_base + 15];   

          }