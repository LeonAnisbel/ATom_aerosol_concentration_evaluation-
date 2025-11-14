# Authors: @Anisbel Leon & @Swetlana Paul
import plot_model_atom
import read_data
import utils_data_sel
import utils_interp_func
import utils_region_def
import plot_atom_data

# Reading ATom data
ds_atom = read_data.ds_atom_data_sel_filter()

# Defining and plotting regions
reg_data = utils_region_def.get_region_dict(ds_atom)
plot_atom_data.plot_regions_map(reg_data)

# read model data for the same dates of ATom
dict_model_obs_data = read_data.read_model_data(ds_atom)

# interpolate data
ds_atom_vs_mod, mod_dicc_keys = utils_interp_func.get_model_ds_interp(ds_atom, dict_model_obs_data)
c_echam, c_atom, ds_atom_vs_daily = utils_data_sel.get_daily_nonull(ds_atom_vs_mod, mod_dicc_keys)
plot_model_atom.plot_one_pannel(c_echam, c_atom, ds_atom_vs_daily)

#Plotting and computing statistics per regions
reg_model_atom = utils_region_def.get_region_dict_model_atom(ds_atom_vs_mod, mod_dicc_keys)
reg_data_stat = plot_model_atom.plot_multipannel(reg_model_atom)

# save all data and statistics as dataframe in a pickle file
utils_data_sel.create_df(reg_data_stat)

