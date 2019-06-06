## Imports

import cmocean
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
import matplotlib.pylab as pl
import numpy as np
import vispy
from vispy import io, plot as vp
from vispy import app, scene, io

amplitude_colormap = cmocean.cm.haline
phase_colormap = cmocean.cm.phase

## Functions

def visualise_flat_tx_array(world = None,filename = None, figsize=[15,10], dpi=150 ):
  
    '''
    ---------------------------------------------
    visualise_flat_tx_array(world,filename,figsize,dpi)
    ---------------------------------------------
        
    This method visualises the location of the sampling grid points.

    Parameters
    ----------

    world : handybeam_core.world
            An instance of the handybeam_core.world class.  
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    figsize : tuple
            This tuple sets the size of the figure used to display the visualisation image.
    dpi : int
            This int sets the resolution of the visualisation image.
    
    '''

    los = dict()

    los['figure'] = plt.figure(figsize=figsize, dpi=dpi)
    los['figure'].plot(world.tx_array.tx_array_element_descriptor[:,0]*1e3, world.tx_array.tx_array_element_descriptor[:,1]*1e3, 'o')
    los['figure'].grid()
    los['figure'].axis('equal')
    los['figure'].xlabel('x [mm]')
    los['figure'].ylabel('y [mm]')
    los['figure'].title(world.tx_array.__str__())
    los['figure'].show()

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def visualise_sampling_grid(sampler=None, filename=None, figsize=[15,10], dpi=150):

    '''
    ---------------------------------------------
    visualise_sampling_grid(sampler,filename,figsize,dpi)
    ---------------------------------------------
        
    This method visualises the location of the transducers.

    Parameters
    ----------
    
    world : handybeam_core.world
            An instance of the handybeam_core.world class.
    sampler : handybeam_core.sampler
            An instance of one of the handybeam_core sampler classes.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    figsize : tuple
            This tuple sets the size of the figure used to display the visualisation image.
    dpi : int
            This int sets the resolution of the visualisation image.
    '''
    los = dict()

    x_points = sampler.coordinates[:,:,0]
    y_points = sampler.coordinates[:,:,1]
    z_points = sampler.coordinates[:,:,2]

    los['figure'] = plt.figure(figsize=figsize, dpi=dpi)
    los['axes'] = Axes3D(los['figure'])
    los['axes'].scatter(x_points,y_points,z_points)
 
    los['axes'].set_zlabel('z [m]',FontSize  = 15 )
    los['axes'].set_ylabel('y [m]',FontSize  = 15 )
    los['axes'].set_xlabel('x [m]',FontSize  = 15 )

    los['axes'].legend(prop={'size': 15})
    los['axes'].set_title('Sampling grid coordinates', FontSize = 15)

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

def visualise_sampling_grid_and_array(world=None,sampler=None, filename=None, figsize=[15,10], dpi=150):

    '''
    ---------------------------------------------
    visualise_sampling_grid_and_array(world,sampler,filename,figsize,dpi)
    ---------------------------------------------
        
    This method visualises the location of the samnpling grid points and the 
    transducers.

    Parameters
    ----------

    world : handybeam_core.world
            An instance of the handybeam_core.world class.
    sampler : handybeam_core.sampler
            An instance of one of the handybeam_core sampler classes.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    figsize : tuple
            This tuple sets the size of the figure used to display the visualisation image.
    dpi : int
            This int sets the resolution of the visualisation image.

    '''
    los = dict()

    sg_x_points = sampler.coordinates[:,:,0] 
    sg_y_points = sampler.coordinates[:,:,1] 
    sg_z_points = sampler.coordinates[:,:,2] 

    arr_x_points = world.tx_array.tx_array_element_descriptor[:,0]
    arr_y_points = world.tx_array.tx_array_element_descriptor[:,1]
    arr_z_points = world.tx_array.tx_array_element_descriptor[:,2]

    norm_axis_x = [-sampler.normal_vector[0]*k*0.1 + sampler.origin[0] for k in range(2)]
    norm_axis_y = [-sampler.normal_vector[1]*k*0.1 + sampler.origin[1] for k in range(2)]
    norm_axis_z = [-sampler.normal_vector[2]*k*0.1 + sampler.origin[2] for k in range(2)]

    par_axis_x = [sampler.parallel_vector[0]*k*0.1 + sampler.origin[0] for k in range(2)]
    par_axis_y = [sampler.parallel_vector[1]*k*0.1 + sampler.origin[1] for k in range(2)]
    par_axis_z = [sampler.parallel_vector[2]*k*0.1 + sampler.origin[2] for k in range(2)]

    vec_x_2 = [sampler.vector_2[0]*k*0.1 + sampler.origin[0] for k in range(2)]
    vec_y_2 = [sampler.vector_2[1]*k*0.1 + sampler.origin[1] for k in range(2)]
    vec_z_2 = [sampler.vector_2[2]*k*0.1 + sampler.origin[2] for k in range(2)]

    los['figure'] = plt.figure(figsize=figsize, dpi=dpi)
    los['axes'] = Axes3D(los['figure'])

    sampling_points = los['axes'].scatter(sg_x_points,sg_y_points,sg_z_points,'b')
    array_points = los['axes'].scatter(arr_x_points,arr_y_points,arr_z_points,'r')
    line_normal = los['axes'].plot(norm_axis_x,norm_axis_y,norm_axis_z,color='k')
    line_par_1 = los['axes'].plot(par_axis_x,par_axis_y,par_axis_z,color='r')
    line_uv_2 = los['axes'].plot(vec_x_2,vec_y_2,vec_z_2,color='b')

    sampling_points.set_label('Sampling points')
    array_points.set_label('Tranducers')
 
    los['axes'].set_zlabel('z [m]',FontSize  = 20 )
    los['axes'].set_ylabel('y [m]',FontSize  = 20 )
    los['axes'].set_xlabel('x [m]',FontSize  = 20 )
    los['axes'].legend(prop={'size': 15},loc ='center left')

    los['axes'].set_title('Sampling grid and array coordinates', FontSize = 20)

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

def visualise_all_in_one(world=None,sampler=None,filename=None,figsize=(16,9),dpi=80):
    
    '''
    ---------------------------------------------
    visualise_all_in_one(world,sampler,filename,figsize,dpi)
    ---------------------------------------------
        
    This method visualises the amplitude and phase of the pressure field and the transducers.

    Parameters
    ----------

    world : handybeam_core.world
            An instance of the handybeam_core.world class.
    sampler : handybeam_core.sampler
            An instance of one of the handybeam_core sampler classes.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    figsize : tuple
            This tuple sets the size of the figure used to display the visualisation image.
    dpi : int
            This int sets the resolution of the visualisation image.
    '''

    los = dict()

    sg_x_points = sampler.coordinates[:,:,0] 
    sg_y_points = sampler.coordinates[:,:,1] 
    sg_z_points = sampler.coordinates[:,:,2] 

    arr_x_points = world.tx_array.tx_array_element_descriptor[:,0]
    arr_y_points = world.tx_array.tx_array_element_descriptor[:,1]
    arr_z_points = world.tx_array.tx_array_element_descriptor[:,2]

    pressure_field = np.nan_to_num(sampler.pressure_field)
    
    # If there are a lot of points in the sampling grid then just display a subset of them.
    
    if len(sg_x_points) > 50:
        
        stepper = int(np.ceil(len(sg_x_points)/50))

        sg_x_points = sg_x_points[0::stepper]
        sg_y_points = sg_y_points[0::stepper]
        sg_z_points = sg_z_points[0::stepper]

        pressure_field = pressure_field[0::stepper]
  
  
    gs = gridspec.GridSpec(2, 2)    

    fig = pl.figure(figsize=figsize,dpi=dpi)

    los['amplitude'] = pl.subplot(gs[0,0],projection = '3d')
    los['phase'] = pl.subplot(gs[0,1],projection = '3d')
    los['trans_amp'] = pl.subplot(gs[1,0])
    los['trans_phase'] = pl.subplot(gs[1,1])
    
    sampling_points_amp = los['amplitude'].scatter(sg_x_points,sg_y_points,sg_z_points,
                                c = np.abs(pressure_field).ravel(),
                                cmap = amplitude_colormap)
    array_points = los['amplitude'].scatter(arr_x_points,arr_y_points,arr_z_points,
                                c = world.tx_array.tx_array_element_descriptor[:,11],
                                cmap = phase_colormap)

    array_points.set_label('Transducer coordinates')
 
    los['amplitude'].set_zlabel('z [m]',FontSize  = 15 )
    los['amplitude'].set_ylabel('y [m]',FontSize  = 15 )
    los['amplitude'].set_xlabel('x [m]',FontSize  = 15 )

    los['amplitude'].set_proj_type('persp')

    amp_cbar = plt.colorbar(sampling_points_amp,ax = los['amplitude'],cmap = amplitude_colormap)
    amp_cbar.ax.set_ylabel('SPL (Pa)',rotation = 0, y = 0,FontSize = 15)

    los['amplitude'].set_title('Amplitude of the pressure field.', FontSize = 15,y=1.08)
    los['amplitude'].legend(loc=9, bbox_to_anchor=(0.5, -0.01),ncol = 2,prop={'size': 15})
    
    sampling_points_phase = los['phase'].scatter(sg_x_points,sg_y_points,sg_z_points,
                                c = np.angle(pressure_field).ravel(),
                                cmap = phase_colormap)
    array_points = los['phase'].scatter(arr_x_points,arr_y_points,arr_z_points,
                                c = world.tx_array.tx_array_element_descriptor[:,11],
                                cmap = phase_colormap)

    array_points.set_label('Transducer coordinates')
 
    los['phase'].set_zlabel('z [m]',FontSize  = 15 )
    los['phase'].set_ylabel('y [m]',FontSize  = 15 )
    los['phase'].set_xlabel('x [m]',FontSize  = 15 )

    los['phase'].set_proj_type('persp')

    phase_cbar = plt.colorbar(sampling_points_phase,ax = los['phase'],cmap = phase_colormap)
    phase_cbar.ax.set_ylabel('Radians',rotation = 0, y = 0,FontSize = 15)

    los['phase'].set_title('Phase of the pressure field.', FontSize = 15,y=1.08)
    los['phase'].legend(loc=9, bbox_to_anchor=(0.5, -0.01),ncol = 2,prop={'size': 15})

    x0 = np.min(arr_x_points)
    xmax = np.max(arr_x_points)

    y0 = np.min(arr_y_points)
    ymax = np.max(arr_y_points)

    transducer_amplitude_distribution = world.tx_array.tx_array_element_descriptor[:,10]
    transducer_phase_distribution =world.tx_array.tx_array_element_descriptor[:,11]

    trans_phase = los['trans_phase'].scatter(arr_x_points,arr_y_points,
                                c = world.tx_array.tx_array_element_descriptor[:,11],
                                cmap = phase_colormap,
                                s = 100)

    los['trans_phase'].set_ylabel('y [m]',FontSize  = 15 )
    los['trans_phase'].set_xlabel('x [m]',FontSize  = 15 )
    los['trans_phase'].set_title('Phase distribution at the transducer plane.', FontSize = 15)

    phase_cbar = plt.colorbar(trans_phase,ax = los['trans_phase'],cmap = phase_colormap)
    phase_cbar.ax.set_ylabel('Radians',rotation = 0, y = 0,FontSize = 15)

    trans_amp = los['trans_amp'].scatter(arr_x_points,arr_y_points,
                                c = world.tx_array.tx_array_element_descriptor[:,10],
                                cmap = amplitude_colormap,
                                s = 100)

    los['trans_amp'].set_ylabel('y [m]',FontSize  = 15 )
    los['trans_amp'].set_xlabel('x [m]',FontSize  = 15 )
    los['trans_amp'].set_title('Amplitude distribution at the transducer plane.', FontSize = 15)

    amp_cbar = plt.colorbar(trans_amp,ax = los['trans_amp'],cmap = amplitude_colormap)
    amp_cbar.ax.set_ylabel('SPL (Pa)',rotation = 0, y = 0,FontSize = 15)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace= 0.3, hspace=0.3)

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def visualise_translation(  world=None, original_pressure_field=None,
                            sampler=None,filename=None, figsize=(15, 10), dpi=150):

    '''
    ---------------------------------------------
    visualise_translation(world,original_pressure_field,sampler,
                          filename,figsize,dpi)
    ---------------------------------------------
        
    This method visualises the effect of the (x-y) translation algorithm on the
    amplitude and phase of the acoustic field.

    Parameters
    ----------

    world : handybeam_core.world
            An instance of the handybeam_core.world class.
    original_pressure_field : numpy array
            A numpy array containing the propagated acoustic pressure field.
    sampler : handybeam_core.sampler
            An instance of one of the handybeam_core sampler classes.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    figsize : tuple
            This tuple sets the size of the figure used to display the visualisation image.
    dpi : int
            This int sets the resolution of the visualisation image.

    '''

    los = dict()

    sg_x_points = sampler.coordinates[:, :, 0]
    sg_y_points = sampler.coordinates[:, :, 1]
    sg_z_points = sampler.coordinates[:, :, 2]

    arr_x_points = world.tx_array.tx_array_element_descriptor[:, 0]
    arr_y_points = world.tx_array.tx_array_element_descriptor[:, 1]
    arr_z_points = world.tx_array.tx_array_element_descriptor[:, 2]

    pressure_field_after = np.nan_to_num(sampler.pressure_field)
    
    # If there are a lot of points in the sampling grid then just display a subset of them.
    
    if len(sg_x_points) > 50:
        
        stepper = int(np.ceil(len(sg_x_points)/50))

        sg_x_points = sg_x_points[0::stepper]
        sg_y_points = sg_y_points[0::stepper]
        sg_z_points = sg_z_points[0::stepper]

        pressure_field_after = pressure_field_after[0::stepper]
        pressure_field_before = original_pressure_field[0::stepper]
   
    else:

        pressure_field_after = pressure_field_after
        pressure_field_before = original_pressure_field

  
    gs = gridspec.GridSpec(2, 2)    

    fig = pl.figure(figsize=figsize, dpi=dpi)

    los['amplitude_1'] = pl.subplot(gs[0, 0], projection='3d')
    los['phase_1'] = pl.subplot(gs[0, 1], projection='3d')

    # Plot original field amplitude.

    sampling_points_amp = los['amplitude_1'].scatter(sg_x_points, sg_y_points, sg_z_points,
                                c=np.abs(pressure_field_before).ravel(),
                                cmap=amplitude_colormap)
    array_points = los['amplitude_1'].scatter(arr_x_points, arr_y_points, arr_z_points, 'r')

    array_points.set_label('Transducer coordinates')
 
    los['amplitude_1'].set_zlabel('z [m]', FontSize=15)
    los['amplitude_1'].set_ylabel('y [m]', FontSize=15)
    los['amplitude_1'].set_xlabel('x [m]', FontSize=15)

    los['amplitude_1'].set_proj_type('persp')

    amp_cbar = plt.colorbar(sampling_points_amp, ax=los['amplitude_1'], cmap=amplitude_colormap)
    amp_cbar.ax.set_ylabel('SPL (Pa)', rotation=0, y=0, FontSize=15)

    los['amplitude_1'].set_title('Amplitude of the pressure field before translation.', FontSize=15, y=1.08)
    los['amplitude_1'].legend(loc=9, bbox_to_anchor=(0.5, -0.01), ncol=2, prop={'size': 15})
    
    # Plot original field phase.

    sampling_points_phase = los['phase_1'].scatter(sg_x_points, sg_y_points, sg_z_points,
                                c=np.angle(pressure_field_before).ravel(),
                                cmap=phase_colormap)
    array_points = los['phase_1'].scatter(arr_x_points, arr_y_points, arr_z_points, 'r')

    array_points.set_label('Transducer coordinates')
 
    los['phase_1'].set_zlabel('z [m]', FontSize=15)
    los['phase_1'].set_ylabel('y [m]', FontSize=15)
    los['phase_1'].set_xlabel('x [m]', FontSize=15)

    los['phase_1'].set_proj_type('persp')

    phase_cbar = plt.colorbar(sampling_points_phase, ax=los['phase_1'], cmap=phase_colormap)
    phase_cbar.ax.set_ylabel('Radians', rotation=0, y=0, FontSize=15)

    los['phase_1'].set_title('Phase of the pressure field before translation.', FontSize=15, y=1.08)
    los['phase_1'].legend(loc=9, bbox_to_anchor=(0.5, -0.01), ncol=2, prop={'size': 15})


    los['amplitude_2'] = pl.subplot(gs[1,0], projection = '3d')
    los['phase_2'] = pl.subplot(gs[1,1], projection='3d')

    # Plot translated field amplitude.

    sampling_points_amp = los['amplitude_2'].scatter(sg_x_points, sg_y_points, sg_z_points,
                                c=np.abs(pressure_field_after).ravel(),
                                cmap=amplitude_colormap)
    array_points = los['amplitude_2'].scatter(arr_x_points, arr_y_points, arr_z_points, 'r')

    array_points.set_label('Transducer coordinates')
 
    los['amplitude_2'].set_zlabel('z [m]', FontSize=15)
    los['amplitude_2'].set_ylabel('y [m]', FontSize=15)
    los['amplitude_2'].set_xlabel('x [m]', FontSize=15)

    los['amplitude_2'].set_proj_type('persp')

    amp_cbar = plt.colorbar(sampling_points_amp, ax=los['amplitude_2'], cmap=amplitude_colormap)
    amp_cbar.ax.set_ylabel('SPL (Pa)', rotation=0, y=0, FontSize=15)

    los['amplitude_2'].set_title('Amplitude of the pressure field after translation.', FontSize=15, y=1.08)
    los['amplitude_2'].legend(loc=9, bbox_to_anchor=(0.5, -0.01), ncol=2, prop={'size': 15})
    
    # Plot translated field phase.

    sampling_points_phase = los['phase_2'].scatter(sg_x_points, sg_y_points, sg_z_points,
                                c=np.angle(pressure_field_after).ravel(),
                                cmap=phase_colormap)
    array_points = los['phase_2'].scatter(arr_x_points, arr_y_points, arr_z_points, 'r')

    array_points.set_label('Transducer coordinates')
 
    los['phase_2'].set_zlabel('z [m]', FontSize=15 )
    los['phase_2'].set_ylabel('y [m]', FontSize=15 )
    los['phase_2'].set_xlabel('x [m]', FontSize=15 )

    los['phase_2'].set_proj_type('persp')

    phase_cbar = plt.colorbar(sampling_points_phase, ax=los['phase_2'], cmap=phase_colormap)
    phase_cbar.ax.set_ylabel('Radians', rotation=0, y=0, FontSize=15)

    los['phase_2'].set_title('Phase of the pressure field after translation.', FontSize = 15,y=1.08)
    los['phase_2'].legend(loc=9, bbox_to_anchor=(0.5, -0.01),ncol = 2,prop={'size': 15})

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.3)

    if filename is not None:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def visualise_translation_3D(world = None,original_pressure_field = None,sampler = None,
        threshold = 50, colour_map = 'cubehelix'):

    '''
    ---------------------------------------------
    visualise_translation(world,original_pressure_field,sampler,
                          filename,figsize,dpi)
    ---------------------------------------------
        
    This method visualises the effect of the (x-y) translation algorithm on the
    amplitude and phase of the acoustic field.

    Parameters
    ----------

    world : handybeam_core.world
            An instance of the handybeam_core.world class.
    original_pressure_field : numpy array
            A numpy array containing the propagated acoustic pressure field.
    sampler : handybeam_core.sampler
            An instance of one of the handybeam_core sampler classes.
    filename : string
            This string indicates the location in which the visualisation image should be stored.
    threshold : float / int
            This sets the threshold for which sampling points are visualised in the image. It can
            be modified to ignore regions with pressure less than the threshold.
    colour_map : string
            This sets the colour map to be used in the visualisation. Please see
            https://github.com/vispy/vispy/blob/master/vispy/color/colormap.py#L348-L441.

    '''

    reshape_no = int(np.round(np.power(sampler.no_points, 1 / 3), 3))
    sampler_pressure_field_reshaped = sampler.pressure_field.reshape((reshape_no,
                                                       reshape_no,
                                                       reshape_no))
    original_pressure_field_reshaped = original_pressure_field.reshape((reshape_no,
                                                       reshape_no,
                                                       reshape_no))



    fig = vp.Fig(bgcolor='white', size=(2000, 2000), show=False)

    vol_data_before = np.abs(original_pressure_field_reshaped)
    vol_data_before = np.flipud(np.rollaxis(vol_data_before, 1))

    vol_data_before[vol_data_before < threshold] = 0
    vol_pw_before = fig[0, 0]
    vol_pw_before.volume(vol_data_before,cmap = colour_map)

    vol_data_after = np.abs(sampler_pressure_field_reshaped)
    vol_data_after = np.flipud(np.rollaxis(vol_data_after, 1))

    vol_data_after[vol_data_after < threshold] = 0
    vol_pw_after = fig[0, 1]
    vol_pw_after.volume(vol_data_after,cmap = colour_map)

    vol_pw_before.camera = scene.cameras.TurntableCamera(fov = 45)
    vol_pw_after.camera = scene.cameras.TurntableCamera(fov = 45)

    vol_pw_before.camera.link(vol_pw_after.camera)
    
    fig.show(run=True)
 
def visualise_3D(world = None,sampler = None,threshold = 50,colour_map = 'cubehelix'):

    fig = vp.Fig(bgcolor='white', size=(2000, 2000), show=False)

    reshape_no = int(np.round(np.power(sampler.no_points, 1 / 3), 3))
    sampler_pressure_field_reshaped = sampler.pressure_field.reshape((reshape_no,
                                                                        reshape_no,
                                                                        reshape_no))


    vol_data_after = np.abs(sampler_pressure_field_reshaped)
    vol_data_after = np.flipud(np.rollaxis(vol_data_after, 1))
    vol_data_after[vol_data_after < threshold] = 0
    vol_pw_after = fig[0, 0]
    vol_pw_after.volume(vol_data_after,cmap = colour_map)
    vol_pw_after.camera = scene.cameras.TurntableCamera(fov = 45)
     
    fig.show(run=True)

