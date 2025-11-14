import os

import global_vars
import region_cond
import pandas as pd

def get_daily_nonull(ds_atom_vs, new_keys):
    """
    Calculate daily average for observations
    :param ds_atom_vs: dataset with ATom data
    :param new_keys: new keys names
    :return: dictionary, observation values, daily average dataframe
    """

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

    return c_echam_txy_dicc, c_atom, ds_atom_vs_daily

def create_df(reg_data_stat):
    """
    Create pickle file to save the statistical indices, model and observation values
    :param reg_data_stat: dictionary with model and ATom data per experiment and region
    :return: None
    """
    file_name = './stat_exp_regions.pkl'
    try:
        os.remove(file_name)
    except OSError:
        pass

    reg_keys = list(region_cond.reg_data.keys())
    exp_keys = list(reg_data_stat.keys())

    reg_keys_2_dataframe = []
    exp_keys_2_dataframe = []

    vars_2_dataframe = [[] for i in range(10)]
    for i in exp_keys:
        for r in reg_keys:
            exp_keys_2_dataframe.append(i)
            reg_keys_2_dataframe.append(r)
            for v_id, v in enumerate(reg_data_stat[i][r].keys()):
                vars_2_dataframe[v_id].append(reg_data_stat[i][r][v])

    da = {'Experiments': exp_keys_2_dataframe,
            'Regions': reg_keys_2_dataframe,
            'Pearson Coef.': vars_2_dataframe[0],
            'Mean Bias': vars_2_dataframe[1],
            'NMB': vars_2_dataframe[2],
            'RMSE': vars_2_dataframe[3],
            'pval': vars_2_dataframe[4],
            'R2': vars_2_dataframe[5],
            'model_vals': vars_2_dataframe[6],
            'atom_vals': vars_2_dataframe[7]
          }
    df_data = pd.DataFrame(data=da)
    df_data.to_pickle(file_name)
