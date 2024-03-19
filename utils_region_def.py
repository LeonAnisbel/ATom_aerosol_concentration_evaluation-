import xarray as xr

import global_vars
import region_cond


# ### Defining regions

def find_region(var_set, cond, dicc, sub_na):
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
    ds = xr.Dataset(
        {"echam_data": ("time", echam),
         "atom_data": ("time", atom)},
        coords={"time": tt}, )
    return ds


def get_region_dict_model_atom(ds_atom_vs, new_keys):
    at_var = global_vars.atom_var
    ds_atom_vs_notnan = ds_atom_vs.where(ds_atom_vs[at_var].compute().notnull(), drop=True)
    ds_atom_vs_notnan['time'] = ds_atom_vs_notnan.time.dt.ceil('12H')  # DDTHH:MM --> DD+1T00:00; alternatively, use floor(): DDTHH:MM --> DDT00:00

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
    # print('\n', reg_data)

    conditions = region_cond.get_cond_list(lat, lon)

    for ex in reg_data.keys():
        for na in reg_data[ex].keys():
            reg_data[ex][na] = region_cond.subkeys
    #         reg_data_ds[ex][na] = region_cond.subkeys

    for ex_id, ex in enumerate(list(da_model_dicc.keys())):
        print(ex)
        # sub_na = f'{global_vars.experiments[ex_id]}_{global_vars.height_criteria}'
        for i, na in enumerate(reg_data[ex].keys()):
            sub_na = list(reg_data[ex].keys())
            variables = [lat, lon, da_atom, da_model_dicc[ex], alt, pres, date]
            _, new_vars = find_region(variables,
                                      conditions[i],
                                      reg_data[ex][na],
                                      sub_na)

            reg_data_ds[ex][na] = define_ds(new_vars[2].data, new_vars[3].data, new_vars[6].data)

    return reg_data_ds
