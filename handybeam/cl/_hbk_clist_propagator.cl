// This is the kernel for propagating the acoustic field onto an arbitrary sampling surface
// or sampling volume defined by a set of provided coordinates.

__kernel void _hbk_clist_propagator(
        __global const float *cl_tx_element_array_descriptor,            // This is the input buffer for the tx elements. 
        __global float *sampling_point_list,                             // This is the list of sampling points. 
        __global float *cl_field,                                        // This is the output buffer for the sampling grid coordinates and pressure values.
        unsigned int tx_count,                                           // This is the number of transducers.
        unsigned int sampling_point_list_count                           // This is the number of points in the sampling point list.
          )
          {
             
                // Get thread coordinates in the computational grid. 
                
                unsigned int sampling_point_idx = get_global_id(0);    

                unsigned int sampling_point_pointer=3*sampling_point_idx;

                // Assign grid coordinates.
                
                float pixel_x_coordinate=(float)sampling_point_list[sampling_point_pointer+0];
                float pixel_y_coordinate=(float)sampling_point_list[sampling_point_pointer+1];
                float pixel_z_coordinate=(float)sampling_point_list[sampling_point_pointer+2];
              
                // Each thread is responsible for looping through the transducers to determine the field at a single
                // sampling point.

                // Initialise pressure values

                float pressure_re = (float)0.0;
                float pressure_im = (float)0.0;

                // Iterate through the transducers.
                unsigned int tx_idx = 0;
              
              
                for (tx_idx=0; tx_idx<tx_count; tx_idx++)
                { 

                // Unpack the tx array descriptor - load data from global memory into registers, hopefully through a cache and broadcast.
                unsigned int tx_pointer_base = 16 * tx_idx;

                float tx_x = cl_tx_element_array_descriptor[tx_pointer_base + 0];
                float tx_y = cl_tx_element_array_descriptor[tx_pointer_base + 1];
                float tx_z = cl_tx_element_array_descriptor[tx_pointer_base + 2];
                
                float tx_xnormal = cl_tx_element_array_descriptor[tx_pointer_base + 3];
                float tx_ynormal = cl_tx_element_array_descriptor[tx_pointer_base + 4];
                float tx_znormal = cl_tx_element_array_descriptor[tx_pointer_base + 5];
                
                float directivity_phase_poly1_c1 = cl_tx_element_array_descriptor[tx_pointer_base + 6];
                
                float directivity_amplitude_poly2_c0 = cl_tx_element_array_descriptor[tx_pointer_base + 7];
                float directivity_amplitude_poly2_c1 = cl_tx_element_array_descriptor[tx_pointer_base + 8];
                float directivity_amplitude_poly2_c2 = cl_tx_element_array_descriptor[tx_pointer_base + 9];

                float tx_amp = cl_tx_element_array_descriptor[tx_pointer_base + 10];
                float tx_phase = cl_tx_element_array_descriptor[tx_pointer_base + 11];
                
                // Calculate the distance from this transducer to the sampling point.

                float delta_x = pixel_x_coordinate - tx_x;
                float delta_y = pixel_y_coordinate - tx_y;
                float delta_z = pixel_z_coordinate - tx_z;
                
                float recp_distance = rsqrt(delta_x*delta_x + delta_y*delta_y + delta_z*delta_z);

                // There can be no output inside a transducer.

                if (medium_wavenumber<recp_distance)
                {
                    pressure_re = NAN;
                    pressure_im = NAN;
                    break; 
                }

                // Now calculate the cosine of angle using the normal.

                float cosine_of_angle_to_normal =  ( delta_x*tx_xnormal + delta_y*tx_ynormal + delta_z * tx_znormal ) * recp_distance ;

                // The is no signal behind the transducer.

                if (cosine_of_angle_to_normal<0.0)
                {
                    pressure_re = NAN;
                    pressure_im = NAN;
                    break; 
                }
                
                // Calculate the phase distance shift 

                float phase_distance_shift = (float) tau  * medium_wavenumber * (1.0 / recp_distance);

                // possibly edit this
                float phase_distance_shift_wrapped = fmod(phase_distance_shift, (float) tau);

                // Calculate amplitude distance drop 

                float amplitude_distance_drop = recp_distance * medium_wavelength;

                // ! Note: The air attenuation model is NOT INCLUDED here.
                // If you want to include air attenuation, it would be approx. -1dB to -2dB per meter,
                // note that the exact value depends heavily on the frequency, temperature and humidity,
                // as per this paper:
                // http://elibrary.lt/resursai/Mokslai/KTU/Ultragarsas/PDF%20straipsniai%2050-2004-Vol.1/50-2004-Vol.1_09-A.Vladisauskas.pdf
                // and, as per this standard: (ISO 9613)
                // https://www.iso.org/standard/20649.html
                //
                // example code:
                // distance = 1.0/recp_distance; // because the distance is not calculated anywhere before
                // amplitude_air_attenuation_drop = power(10,distance * attenuation_per_db_meter/20);

                // Apply the HN50 directivity function here
               
                float ca = 1.0 - cosine_of_angle_to_normal;
                
                // Calculate this first so that the register holding directivity_phase_poly1_c1 can be released for ca2

                float directivity_phase = directivity_phase_poly1_c1 * ca;

                // Ca2 is simply ca^2
                float ca2 = ca*ca;
                float directivity_amplitude_drop =            \
                        directivity_amplitude_poly2_c0        \
                      + directivity_amplitude_poly2_c1 * ca   \
                      + directivity_amplitude_poly2_c2 * ca2;


                float rx_amplitude = tx_amp   * amplitude_distance_drop * directivity_amplitude_drop;
                float rx_phase     = tx_phase + phase_distance_shift_wrapped  + directivity_phase;
               
                // Accumulate result
            
                pressure_re = pressure_re + native_cos(rx_phase) * rx_amplitude;
                pressure_im = pressure_im + native_sin(rx_phase) * rx_amplitude;
            
                } 

                // Output these pixel coordinates so that we can double check they match up with the python code. 
              
                unsigned int output_pointer_base = 2 * sampling_point_idx ;

                cl_field[output_pointer_base+0] = pressure_re;
                cl_field[output_pointer_base+1] = pressure_im;


         
          } 