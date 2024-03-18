import global_vars, read_data
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from datetime import datetime


def plot_flight_heights():
    colors = ['r', 'b', 'g', 'm']
    names = ['ATom-1', 'ATom-2', 'ATom-3', 'ATom-4']
    at_var = global_vars.atom_var
    dates = []
    altitude = []
    oa_mass = []
    for i in range(4):
        path_atom_meta = f'{global_vars.base_path}*{i + 1}.nc'
        ds_atom_c, ds_atom_meta, ds_atom_time, ds_atom_meta_p = read_data.read_atom_data(path_atom_meta)

        dates.append([datetime.strptime(str(m), '%Y-%m-%dT%H:%M:%S.000000000') for m in ds_atom_time['time'].values])
        altitude.append(ds_atom_meta['ALT_AMS'].values / 1000)
        oa_mass.append(ds_atom_meta[at_var].values)

    fig = plt.figure(constrained_layout=True, figsize=(14, 8))
    (subfig1,subfig2) = fig.subfigures(nrows = 1, ncols = 2)
    subfigs = [subfig1,subfig2]
    ax = subfig1.subplots(nrows=1, ncols=1)
    for i,axs in enumerate(colors):
        ax.scatter(oa_mass[i],altitude[i],c = colors[i],label=names[i])
        ax.tick_params(axis = 'both',labelsize = '12')
        ax.axhline(y = 2, color = 'k', linestyle = '--')

    ax.set_ylabel('Flight Height (km)',fontsize = 12)
    ax.set_xlabel('Mass_concentration_of_organic_aerosol_in_air_\n'
                     'for_particle_diameter_less_than_1um_measured_by_HRAMS\n(ug sm-3)'
                 ,fontsize = 12)
    ax.set_xscale('log')


    axes = subfig2.subplots(nrows=4, ncols=1)
    # axes.flatten()
    for i,axs in enumerate(axes):
        axs.plot(dates[i],altitude[i],c = colors[i])
        axs.tick_params(axis='x', labelrotation=45,colors = colors[i])
        axs.yaxis.label.set_color(colors[i])
        axs.tick_params(axis = 'both',labelsize = '10')

    ax.legend()
    plt.savefig(f'{global_vars.plot_dir}mass_conc_OA_flight_height.png',dpi = 300)


def plot_regions_map(reg_data):
    color_reg = ['y', 'r', 'lightgreen', 'g', 'm', 'k', 'b', 'orange']

    fig, ax = plt.subplots(1, 1, figsize=(9, 8),
                           subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)}, )
    for i, na in enumerate(reg_data.keys()):
        cb = ax.scatter(reg_data[na]['longitud'], reg_data[na]['latitud'], c=color_reg[i], label=na,
                        transform=ccrs.PlateCarree())

    ax.legend(loc='upper left')
    ax.coastlines()
    ax.gridlines(draw_labels=True, )
    plt.savefig(f'{global_vars.plot_dir}atom_region_sel.png', dpi=300)
