import xarray as xr
import global_vars
import numpy as np
import plot_model


def read_atom_data(path_atom_meta):
    """ This function reads in the ATom in situ aircraft data from netcdf files
    Returns: all relevant variables needed from the dataset"""
    ds_atom_palms = xr.open_mfdataset(path_atom_meta,
                                      group='PALMS-PartType-Mass',
                                      concat_dim='time',
                                      combine='nested',
                                      preprocess=lambda ds:
                                      ds[['SeaSaltMass_PALMS', 'BioBurnMass_PALMS', 'OilCombMass_PALMS']])

    ds_atom_meta = xr.open_mfdataset(path_atom_meta,
                                     group='AMS',
                                     concat_dim='time',
                                     combine='nested',
                                     preprocess=lambda ds:
                                     ds[['ALT_AMS', 'LON_AMS', 'LAT_AMS', 'OA_PM1_AMS']])

    ds_atom_meta_p = xr.open_mfdataset(path_atom_meta,
                                       group='MMS',
                                       concat_dim='time',
                                       combine='nested',
                                       preprocess=lambda ds:
                                       ds[['P']])

    ds_atom_time = xr.open_mfdataset(path_atom_meta,
                                     concat_dim='time',
                                     combine='nested',
                                     preprocess=lambda ds: ds[['time']])

    return ds_atom_palms, ds_atom_meta, ds_atom_time, ds_atom_meta_p


def ds_atom_data_sel_filter():
    """
    Selecting only atom levels under 1 km height and concentrations smaller than 0.2 ug/m3
    :return: dataframe with filtered ATom data
    """

    at_var = global_vars.atom_var
    height = global_vars.height_criteria
    ds_atom_c, ds_atom_meta, ds_atom_time, ds_atom_meta_p = read_atom_data(global_vars.path_atom_meta)

    ds_atom_c['P'] = ds_atom_meta_p['P'] * 100

    ds_atom = ds_atom_c.assign(lat=ds_atom_meta['LAT_AMS'],
                               lon=ds_atom_meta['LON_AMS'] % 360,
                               alt=ds_atom_meta['ALT_AMS'],
                               OA_PM1_AMS=ds_atom_meta['OA_PM1_AMS'],
                               time=ds_atom_time['time'])

    # selecting only atom levels under 1 km height
    ds_atom = ds_atom.where(ds_atom['alt'].compute() < height, drop='True')
    if at_var == 'OA_PM1_AMS':
        # Constrain ATom OA_PM1_AMS to limits in remote regions as in Pai et al. 2020
        ds_atom = ds_atom.where((ds_atom[at_var].compute() > 0.) & (ds_atom[at_var].compute() <= 0.2), drop='True')
    else:
        ds_atom = ds_atom.where(ds_atom[at_var].compute() > 0., drop='True')
    return ds_atom


def read_model_data(ds_atom):
    """
    Reading model data for each experiment, only loads the time steps where ATom data exists
    :return: dataframe with model data
    """
    start_time_atom = ds_atom['time'].values[0]
    end_time_atom = ds_atom['time'].values[-1]
    end_time_atom = end_time_atom + (end_time_atom - end_time_atom.astype('datetime64[M]'))

    mo_var = global_vars.model_var
    exper = global_vars.experiments
    exper_id = global_vars.exp_id

    # Only time period of ATom-measurements and only selected variables are loaded in order to save memory.
    # read in all files in directory

    dict_model_obs_data = {}
    ds_ac3_arctic = []
    path_arctic = f'{global_vars.p_model}{exper[0]}/'
    for e_id, m_v in enumerate(mo_var[:-2]):
        dict_model_obs_data[exper_id[e_id]] = xr.open_mfdataset(f'{path_arctic}*_{m_v}_plev.nc',
                                                                concat_dim='time',
                                                                combine='nested',
                                                                preprocess=lambda ds:
                                                                ds[[mo_var[e_id]]].sel(
                                                                    time=slice(start_time_atom, end_time_atom)))

    path_echam = f'{global_vars.p_model}{exper[-1]}/'
    dict_model_obs_data[exper_id[-1]] = xr.open_mfdataset(f'{path_echam}*_{mo_var[-2]}_plev.nc',
                                                          concat_dim='time',
                                                          combine='nested',
                                                          preprocess=lambda ds:
                                                          ds[[mo_var[-2]]].sel(
                                                              time=slice(start_time_atom, end_time_atom)))

    return dict_model_obs_data
