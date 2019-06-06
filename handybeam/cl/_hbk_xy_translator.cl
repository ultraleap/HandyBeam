// This is the kernel for translating focal point in the (x,y) plane.

__kernel void _hbk_xy_translator(
            __global float *cl_TxArrayDescriptor,           // This is the input buffer for the transducer information.
            __global float *cl_output_buffer,               // This is the output buffer for the transducer information.
            float x_translate,                              // This is the distance to translate the focal points in the x-axis.
            float y_translate,                              // This is the distance to translate the focal points in the y-axis.
            float plane_height_recp                         // This is the distance along the z-axis between the transducer array and the focal plane.
          )

          {

            // Get global ID to use to index transducers.

            unsigned int tx_index = get_global_id(0);  

            // Unpack the relevant parts of the tx_array_descriptor

            unsigned int tx_pointer_base = 16 * tx_index;

            float tx_x = cl_TxArrayDescriptor[tx_pointer_base + 0];
            float tx_y = cl_TxArrayDescriptor[tx_pointer_base + 1];

            float tx_phase = cl_TxArrayDescriptor[tx_pointer_base + 11];  
        
            // Determine angle required to translate by a given amount x.

            float x_d = x_translate * plane_height_recp;

            // First term of maclaurin series expansion for arctan - this is accurate up to < 1% error 
            // for x_d <= 0.1 -> if we only translate 1mm at a time this means we it will be accuracte
            // beyond 10mm with an error of less than 1 %

            float alpha_x = x_d;
            
            // Determine angle required to translate by a given amount y.

            float y_d = y_translate * plane_height_recp;

            // First term of maclaurin series expansion for arctan - this is accurate up to < 1% error 
            // for x_d <= 0.1 -> if we only translate 1mm at a time this means we it will be accuracte
            // beyond 10mm with an error of less than 1 %

            float alpha_y = y_d;

            // Beam steering angle coefficient for x using first term for maclaurin series expansion -
            // this is accurate up to < 1 % error for alpha_x <= 0.1

            float beta_x = alpha_x;

            // Beam steering angle coefficient for x using first term for maclaurin series expansion -
            // this is accurate up to < 1 % error for alpha_y <= 0.1

            float beta_y = alpha_y;

            // Phase modification for translation along x-axis.

            float delta_phase_x = translation_medium_wavenumber * beta_x * tx_x;

            // Phase modification for translation along y-axis.
                    
            float delta_phase_y = translation_medium_wavenumber * beta_y * tx_y;

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
            cl_output_buffer[tx_pointer_base + 11] = (float) tx_phase + delta_phase_x + delta_phase_y;
            cl_output_buffer[tx_pointer_base + 12] = cl_TxArrayDescriptor[tx_pointer_base + 12]; 
            cl_output_buffer[tx_pointer_base + 13] = cl_TxArrayDescriptor[tx_pointer_base + 13]; 
            cl_output_buffer[tx_pointer_base + 14] = cl_TxArrayDescriptor[tx_pointer_base + 14];
            cl_output_buffer[tx_pointer_base + 15] = cl_TxArrayDescriptor[tx_pointer_base + 15]; 
      

          }