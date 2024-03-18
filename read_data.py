import xarray as xr
import global_vars
import numpy as np
import plot_model


def read_atom_data(path_atom_meta):
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
    ds_atom = ds_atom.where(ds_atom[at_var].compute() > 0., drop='True')

    return ds_atom


def read_model_data(ds_atom):
    start_time_atom = ds_atom['time'].values[0]
    end_time_atom = ds_atom['time'].values[-1]
    end_time_atom = end_time_atom + (end_time_atom - end_time_atom.astype('datetime64[M]'))

    mo_var = global_vars.model_var
    exper =  global_vars.experiments
    # Only time period of ATom-measurements and only selected variables are loaded in order to save memory.
    # read in all files in directory


    path_arctic = f'{global_vars.p_model}{exper[0]}/'
    ds_ac3_arctic = xr.open_mfdataset(f'{path_arctic}*_{mo_var[0]}_plev.nc',
                                      concat_dim='time',
                                      combine='nested',
                                      preprocess=lambda ds:
                                      ds[[mo_var[0]]].sel(time=slice(start_time_atom, end_time_atom)))

    path_echam = f'{global_vars.p_model}{exper[1]}/'
    ds_echam_base = xr.open_mfdataset(f'{path_echam}*_{mo_var[1]}_plev.nc',
                                      concat_dim='time',
                                      combine='nested',
                                      preprocess=lambda ds:
                                      ds[[mo_var[1]]].sel(time=slice(start_time_atom, end_time_atom)))
    return ds_echam_base, ds_ac3_arctic


def sel_time(C, month):
    C_ti = C.where(C.time.dt.month == month, drop=True)
    return C_ti.mean(dim='time', skipna=True).mean(dim='plev', skipna=True)


def read_model_moa_oa():
    exper =  global_vars.experiments

    path_arctic = f'{global_vars.p_model}{exper[0]}/'
    ds_ac3_arctic = xr.open_mfdataset(f'{path_arctic}*_OA_plev.nc',
                                      concat_dim='time',
                                      combine='nested',
                                      preprocess=lambda ds:
                                      ds[['OA']])

    ds_ac3_arctic_moa = xr.open_mfdataset(f'{path_arctic}*_MOA_plev.nc',
                                          concat_dim='time',
                                          combine='nested',
                                          preprocess=lambda ds:
                                          ds[['MOA']])

    ds_ac3_arctic = ds_ac3_arctic.where(ds_ac3_arctic['plev'] > 90000, drop=True)
    ds_ac3_arctic_moa = ds_ac3_arctic_moa.where(ds_ac3_arctic_moa['plev'] > 90000, drop=True)

    yr_list = ds_ac3_arctic.time.dt.year.values
    years = [min(yr_list), max(yr_list)]
    months = np.arange(1, 13)

    oa_list = []
    moa_list = []

    for m in months:
        oa_list.append(sel_time(ds_ac3_arctic, m).compute())
        moa_list.append(sel_time(ds_ac3_arctic_moa, m).compute())

    ds_ac3_arctic_monthly = xr.concat(oa_list, dim='time')
    ds_ac3_arctic_moa_monthly = xr.concat(moa_list, dim='time')

    ratio = ds_ac3_arctic_moa_monthly.rename({'MOA' : 'VAR'})/ds_ac3_arctic_monthly.rename({'OA': 'VAR'})

    print(ratio,'\n', ratio.min(),ratio.max())

    lon = ds_ac3_arctic.lon
    lat = ds_ac3_arctic.lat

    plot_model.plot_3_pannel([ratio['VAR'].isel(time=4),
                              ratio['VAR'].isel(time=7),
                              ratio['VAR'].isel(time=10)],
                             ['4', '7', '10'],
                             lon, lat, years)
