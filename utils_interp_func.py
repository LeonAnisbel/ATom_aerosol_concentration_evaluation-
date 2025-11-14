from datetime import datetime
import global_vars
import xarray as xr
import numpy as np

# #### Interpolating values onto ECHAM grid
def find_nearest(atom_val, echam_list):
    """find the closest date and return the index """
    diff = []
    for i in echam_list:
        diff.append(i - atom_val)
    m = min(i for i in diff if i > 0)
    return m, diff.index(m)


def interpolation(ds, x, y, z):
    """
    Performs linear interpolation and returns interpolated value od dataset for specific x, y, z location
    :return : interpolated value
    """
    int_val = ds.interp(lon=x, lat=y, plev=z, method="linear")
    return int_val.values


def get_model_ds_interp(ds_atom, dict_model_obs_data):
    """
    Interpolate model values to observation location and dates for every experiment
    :param ds_atom: ATom dataset
    :param dict_model_obs_data: dictionary with model data (as dataset) per experiment
    :return: ds_atom_vs: dataframe with interpolated values per experiment,
             new_keys: experiment names
    """
    exp = global_vars.exp_id
    mo_var = global_vars.model_var

    # Lists wit Coverted datetime to decimals
    dates_atom = []
    dates_echam = []
    dates_atom.append([datetime.strptime(str(m),
                                         '%Y-%m-%dT%H:%M:%S.000000000').timestamp()
                       for m in ds_atom.time.values])
    dates_echam.append([datetime.strptime(str(m),
                                          '%Y-%m-%dT%H:%M:%S.000000000').timestamp()
                        for m in dict_model_obs_data[exp[-1]].time.values])

    ds_model_data = [dict_model_obs_data[exp[0]]]
    interp_model = [[]]  # initialize interp list
    if len(exp) > 1:
        interp_model = [[], [], []]  # initialize interp list

    # go through all date values from atom and interpolate the spatial grid
    # to the ECHAM-HAM suitable time. Note that ECHAM output is every 12h
    # and every datetime from atom between 00 and 12 h will be interpolated
    # to the same spatial ECHAM grid
    for lidx, mo_exp in enumerate(list(dict_model_obs_data.keys())):
        print('interpolating experiment: ', mo_exp)
        for i, idx in enumerate(dates_atom[0]):
            _, index = find_nearest(idx, dates_echam[0])
            interp = interpolation(dict_model_obs_data[mo_exp].isel(time=index)[mo_var[lidx]],
                                   ds_atom['lon'].values[i],
                                   ds_atom['lat'].values[i],
                                   ds_atom['P'].values[i])
            interp_model[lidx].append(float(interp))

    dict_model = dict((name, da) for da, name in zip(interp_model, list(dict_model_obs_data.keys())))

    # create new dataset with the interpoalted variables
    dicc_keys = list(dict_model.keys())
    new_keys = [f'{m}_var' for m in list(dict_model_obs_data.keys())]

    ds_inter = xr.Dataset({
        new_keys[0]: (
            "time",
            dict_model[dicc_keys[0]]),
    },
        coords={"time": ds_atom.time.values}, )
    ds_atom_vs = ds_atom.assign(ac3_arctic_OA_var=ds_inter[new_keys[0]] * 1e9)

    if len(exp) > 1:
        ds_inter = xr.Dataset({
            new_keys[0]: (
                "time",
                dict_model[dicc_keys[0]]),
            new_keys[1]: (
                "time",
                dict_model[dicc_keys[1]]),
            },
            coords={"time": ds_atom.time.values}, )

        ds_atom_vs = ds_atom.assign(ac3_arctic_OA_var=ds_inter[new_keys[0]] * 1e9,
                                    echam_base_var=ds_inter[new_keys[1]] * 1e9,)


    return ds_atom_vs, new_keys
