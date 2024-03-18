import global_vars
def get_daily_nonull(ds_atom_vs,new_keys):
    at_var = global_vars.atom_var
    # extract nan values from dataset
    ds_atom_vs_notnan = ds_atom_vs.where(ds_atom_vs[at_var].compute().notnull(), drop=True)
    # calculate daily means
    ds_atom_vs_notnan['time'] = ds_atom_vs_notnan.time.dt.ceil(
        '1D')  # DDTHH:MM --> DD+1T00:00; alternatively, use floor(): DDTHH:MM --> DDT00:00
    ds_atom_vs_daily = ds_atom_vs_notnan.groupby('time').mean(skipna=True)


    # c_echam_txy = ds_atom_vs_daily['interp_SS']
    c_echam_txy_dicc = dict((name, ds_atom_vs_daily[name]) for name in new_keys)
    c_atom = ds_atom_vs_daily[at_var]

    return c_echam_txy_dicc,c_atom,ds_atom_vs_daily
