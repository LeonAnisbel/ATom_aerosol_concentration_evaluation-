import xarray as xr
import numpy as np
import global_vars
import region_cond
import pandas as pd


# ### Defining regions

def find_region(var_set, cond, dicc, sub_na):
    """
    This function is used to select and filter certain regions according to the conditions variable (cond).
    var_set is the list of variables, dicc is the dictionary containing the regions of key argument sub_na
    :return : dictionary variable (dicc) with the data filtered to meet each condition
    """
    variables = []
    for i, v in enumerate(var_set):
        if len(cond) <= 1:
            v = v.where((cond[0][0] > cond[0][1]) &
                        (cond[0][0] < cond[0][2])
                        , drop=True)
        elif len(cond) > 1:
            v = v.where(((cond[0][0] > cond[0][1]) &
                         (cond[0][0] < cond[0][2]) &
                         (cond[1][0] > cond[1][1]) &
                         (cond[1][0] < cond[1][2]))
                        , drop=True)

        variables.append(v)
        dicc[sub_na[i]] = v
    return dicc, variables


def get_region_dict(ds_atom):
    """
    Creates a dictionary containing the ATom data per regions as key arguments
    :param ds_atom: ATom data
    :return: Dictionary after region classification
    """
    lat = ds_atom['lat'].compute()
    lon = ds_atom['lon'].compute()
    data = ds_atom['SeaSaltMass_PALMS'].compute()
    alt = ds_atom['alt'].compute()
    pres = ds_atom['P'].compute()
    date = ds_atom['time'].compute()

    conditions = region_cond.get_cond_list(lat, lon)
    reg_data = region_cond.reg_data

    for na in reg_data.keys():
        reg_data[na] = region_cond.subkeys

    for i, na in enumerate(reg_data.keys()):
        sub_na = list(reg_data[na].keys())
        variables = [lat, lon, data, alt, pres, date]
        reg_data[na], _ = find_region(variables,
                                      conditions[i],
                                      reg_data[na],
                                      sub_na)
    return reg_data


def define_ds(atom, echam, tt):
    """
    Defines a dataset with ATom and model data
    :var atom: ATom data
    :var echam: model data
    :var tt: time data
    :return: dataset with ATom and model data with time as coordinate
    """
    ds = xr.Dataset(
        {"echam_data": ("time", echam),
         "atom_data": ("time", atom)},
        coords={"time": tt}, )
    return ds


def get_region_dict_model_atom(ds_atom_vs, new_keys):
    """
    This function creates and returns a dictionary with both ATom and Model values grouped per regions
    :param ds_atom_vs: ATom data
    :param new_keys: new keys names
    :return: dictionary with ATom and Model values grouped per regions
    """
    at_var = global_vars.atom_var
    ds_atom_vs_notnan = ds_atom_vs.where(ds_atom_vs[at_var].compute().notnull(),
                                         drop=True)
    ds_atom_vs_notnan['time'] = ds_atom_vs_notnan.time.dt.ceil(
        '1D')

    lat = ds_atom_vs_notnan['lat'].compute()
    lon = ds_atom_vs_notnan['lon'].compute()
    da_atom = ds_atom_vs_notnan[at_var].compute()
    da_model_dicc = dict((name, ds_atom_vs_notnan[name].compute()) for name in new_keys)
    alt = ds_atom_vs_notnan['alt'].compute()
    pres = ds_atom_vs_notnan['P'].compute()
    date = ds_atom_vs_notnan['time'].compute()

    reg_data = dict((name, region_cond.reg_data)
                    for name in list(da_model_dicc.keys()))

    reg_data_ds = dict((name, {})
                       for name in list(da_model_dicc.keys()))

    conditions = region_cond.get_cond_list(lat, lon)

    #create empty dictionary
    for ex in list(reg_data.keys()):
        for na in reg_data[ex].keys():
            reg_data[ex][na] = region_cond.subkeys
    #         reg_data_ds[ex][na] = region_cond.subkeys

    #group data per experiment and region
    for ex_id, ex in enumerate(list(da_model_dicc.keys())):
        print(ex)
        tot_lon, tot_lat = [], []
        # sub_na = f'{global_vars.experiments[ex_id]}_{global_vars.height_criteria}'
        for i, na in enumerate(reg_data[ex].keys()):
            sub_na = list(reg_data[ex][na].keys())
            variables = [lat, lon, da_atom, da_model_dicc[ex], alt, pres, date]
            _, new_vars = find_region(variables,
                                      conditions[i],
                                      reg_data[ex][na],
                                      sub_na)
            reg_data_ds[ex][na] = define_ds(new_vars[2].data, new_vars[3].data, new_vars[6].data)
            for ll in range(len(new_vars[0].data)):
                tot_lat.append(new_vars[0].data[ll])
                tot_lon.append(new_vars[1].data[ll])

    tot_ratio = []
    for i, na in enumerate(reg_data[new_keys[0]].keys()):
        ratio = (reg_data_ds[new_keys[1]][na]['echam_data'] /
                 reg_data_ds[new_keys[0]][na]['echam_data'])
        for ll in ratio:
            tot_ratio.append(ll.values)

    da_df = {"moa_oc_ratio": tot_ratio,
             "lat": tot_lat,
             "lon": tot_lon}
    ds_ratio = pd.DataFrame(data=da_df)
    ds_ratio.to_pickle('./moa_moa_oc_ratio.pkl')

    return reg_data_ds
