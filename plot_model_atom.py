import Taylor_diagram
import global_vars
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

import statistics


def diff_plot(c_echam_txy, c_atom, ds_atom_vs_daily, na):
    var = global_vars.model_var
    diff_abs = c_echam_txy - c_atom

    # define data range covered by colormap; make sure that it is symmetrical around 0
    #     colormap_range = max(abs(math.floor(diff_abs.min())),
    #                          abs(math.ceil(diff_abs.max())))
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    cmap = plt.get_cmap('RdBu_r',10)
    map_plot = ax.scatter(ds_atom_vs_daily.lon,
                          ds_atom_vs_daily.lat,
                          c=diff_abs.values,
                          cmap=cmap,
                          vmin=-0.2, #5
                          vmax=0.2,
                          transform=ccrs.PlateCarree())
    ax.coastlines()
    cbar = fig.colorbar(map_plot)
    ax.set_title(
        f'{na}_$c_\mathrm{{{var}}}$$_\mathrm{{,ECHAM}} - c_\mathrm{{{var}}}$$_\mathrm{{,ATom}}$ in $\mu g m^{-3}$')

    # add grid lines
    gl = ax.gridlines(draw_labels=True,
                      x_inline=False,
                      y_inline=False)  #adding grid lines with labels
    gl.top_labels = False
    gl.right_labels = False

    var_na = global_vars.atom_plot_varna
    plt.savefig(f'{global_vars.plot_dir}{na}_diff_abs_{var_na}.pdf', bbox_inches='tight')


def scatter_plot(c_echam_txy, c_atom, statistical_quantities, exp):
    var = global_vars.model_var
    units = global_vars.data_units

    fig = plt.figure()
    ax_scatter = plt.axes()
    ax_scatter.plot(c_atom,
                    c_echam_txy,
                    marker='.',
                    markeredgecolor='none',
                    markersize=4,
                    ls='',
                    zorder=2)
    #ax_scatter.set_aspect(aspect=1)

    ax_scatter.set_xlabel(f'$c_\mathrm{{{var}}}$$_\mathrm{{,ATom}}$ ({units})')
    ax_scatter.set_ylabel(f'$c_\mathrm{{{var}}}$$_\mathrm{{,ECHAM}}$ ({units})')

    linreg_coeffs = np.polynomial.Polynomial.fit(c_atom,
                                                 c_echam_txy,
                                                 deg=1).convert().coef  # perform linear regression, get intercept and slope
    x = np.linspace(c_atom.min(),
                    c_atom.max(),
                    num=2)  # define x-values of regression line
    y = linreg_coeffs[0] + linreg_coeffs[1] * x  # define y-values of regression line

    ax_scatter.plot(x, y,
                    label=f'linear regression\ny = {linreg_coeffs[1]:.2f} x + {linreg_coeffs[0]:.2f}',
                    zorder=3)  # draw regression line
    # x_eq = np.array([max(c_echam_txy.min(),
    #                      c_atom.min()),
    #                  min(c_echam_txy.max(),
    #                      c_atom.max())])
    # ax_scatter.plot(x_eq, x_eq,
    #                 label='y = x', zorder=1)
    lims = [
        np.min([ax_scatter.get_xlim(), ax_scatter.get_ylim()]),  # min of both axes
        np.max([ax_scatter.get_xlim(), ax_scatter.get_ylim()]),  # max of both axes
    ]
    ax_scatter.plot(lims, lims, 'k--', alpha=0.75, zorder=0, label='1:1 line')
    ax_scatter.legend()
    ax_scatter.grid(True)

    for i in range(len(statistical_quantities)):
        plt.gcf().text(0.11, -(i + 3) * 0.04,
                       f'{statistical_quantities[i][0]} = {statistical_quantities[i][1]:.2f} {statistical_quantities[i][2]}')

    plt.savefig(f'{global_vars.plot_dir}scatter_{exp}.pdf', bbox_inches='tight')


def plot_scatter_improve(axs, atom, model, title, std_obs):
    axs.errorbar(atom, model, xerr=std_obs, fmt='o', color="grey", alpha=0.8)
    axs.scatter(atom, model, color='blue')
    axs.set_title(title, fontsize='16')
    linreg_coeffs = np.polynomial.Polynomial.fit(atom, model,
                                                 deg=1).convert().coef  # perform linear regression, get intercept and slope
    x = np.linspace(atom.min(), atom.max(), num=2)  # define x-values of regression line
    y = linreg_coeffs[0] + linreg_coeffs[1] * x  # define y-values of regression line
    axs.plot(x, y,color = 'darkred',
             label=f'linear regression\ny = {linreg_coeffs[1]:.2f} x + {linreg_coeffs[0]:.2f}', zorder=3)


    at_max = atom.max()
    mo_max = model.max()
    max_list = [at_max, mo_max]
    # axs.set_xlim([0, max(max_list)])
    # axs.set_ylim([0, max(max_list)])

    # x_eq = np.array([max(model.min(), atom.min()),
    #                  min(model.max(), atom.max())])
    # axs.plot(x_eq, x_eq, label='y = x', zorder=1)
    lims = [
        np.min([axs.get_xlim(), axs.get_ylim()]),  # min of both axes
        np.max([axs.get_xlim(), axs.get_ylim()]),  # max of both axes
    ]
    axs.plot(lims, lims, 'k--', alpha=0.75, zorder=0, label='1:1 line')
    axs.legend()
    axs.grid(linewidth=0.5)
    axs.tick_params(axis='both', labelsize='14')


def plot_one_pannel(c_echam, c_atom, ds_atom_vs_daily):
    mo_var = global_vars.model_var
    at_var = global_vars.atom_plot_varna

    for idx, na in enumerate(list(c_echam.keys())):
        print(na)
        units = global_vars.data_units
        mo_var_title = mo_var[idx]
        if mo_var[idx] == 'OA':
            mo_var_title = 'MOA + OC'
        c_echam_txy = c_echam[na]
        diff_plot(c_echam_txy, c_atom, ds_atom_vs_daily, na)
        std_model, std_obs, RMSE, mean_bias, normalized_mean_bias, pearsons_coeff, statistical_quantities = (
            statistics.get_statistics(
            c_atom,c_echam_txy))
        scatter_plot(c_atom, c_atom, statistical_quantities, na)

        stat = f'(RMSE: {RMSE:.2f}, bias:{mean_bias:.2f}, R: {pearsons_coeff:.2f})'
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        fig_na = f'Daily concentration {units}'
        plot_scatter_improve(ax, c_atom, c_echam_txy, fr'$\bf{fig_na}$' + f'\n{stat}', std_obs)
        ax.set_ylabel(f'Model {mo_var_title}', fontsize='16')
        ax.set_xlabel(f'ATom {at_var}', fontsize='16')
        plt.tight_layout()

        plt.savefig(f'{global_vars.plot_dir}{na}_{mo_var_title}_global_single_plot.png', dpi=300)


def plot_multipannel(reg_data):
    at_var = global_vars.atom_plot_varna
    mo_var = global_vars.model_var
    units = global_vars.data_units

    reg_data_4_taylor_obs = dict((name, {})
                       for name in list(reg_data.keys()))
    reg_data_4_taylor_mod = dict((name, {})
                       for name in list(reg_data.keys()))
    reg_data_stat = dict((name, {})
                       for name in list(reg_data.keys()))
    reg_data_4_taylor_mod_list = []

    for idx, ex in enumerate(reg_data.keys()):
        print('plotting', ex)
        mo_var_title = mo_var[idx]
        if mo_var[idx] == 'OA':
            mo_var_title = 'MOA + OC'

        plt.close()
        fig, ax = plt.subplots(2, 3, figsize=(15, 10))
        axes = ax.flatten()
        fig_na = f'Daily concentration {units}'
        fig.suptitle(f'{fig_na}', fontsize='20')
        for i, na in enumerate(reg_data[ex].keys()):
            reg_data_stat[ex][na] = {}
            print(na)
            print("_______________________________")
            # calculate daily means
            # reg_data[ex][na]['time'] = reg_data[ex][na].time.dt.ceil('1D')
            ds_atom_vs_daily = reg_data[ex][na].groupby('time').mean(skipna=True)

            #daily std for observations
            time_val_list = set(list(reg_data[ex][na]['time'].values))
            std_daily_obs = []
            for ti_val in time_val_list:
                std_obs_list = []
                for ti_idx, ti_obs_val in enumerate(reg_data[ex][na]['time'].values):
                    if ti_val == ti_obs_val:
                        std_obs_list.append(reg_data[ex][na]['atom_data'][ti_idx].values)

                std_daily_obs.append(np.nanstd(np.array(std_obs_list)))

            ds_atom_vs_daily['std_daily_observ'] = (['time'], std_daily_obs)
            ds_atom_vs_daily_filter = ds_atom_vs_daily#.where(ds_atom_vs_daily['echam_data'] < 0.8, drop=True)

            c_echam_txy = ds_atom_vs_daily_filter['echam_data']
            c_atom = ds_atom_vs_daily_filter['atom_data']

            reg_data_4_taylor_mod[ex][na] = c_echam_txy
            reg_data_4_taylor_obs[ex][na] = c_atom

            print(ds_atom_vs_daily_filter['time'], '\n', c_echam_txy)

            print(ds_atom_vs_daily_filter['time'], '\n', c_atom)

            std_model, std_obs, RMSE, mean_bias, normalized_mean_bias, pearsons_coeff, _ = statistics.get_statistics(
                c_atom, c_echam_txy)
            stat = f'(RMSE: {RMSE:.2f}, bias:{mean_bias:.2f}, R: {pearsons_coeff:.2f})'

            reg_data_stat[ex][na]['R'] = pearsons_coeff
            reg_data_stat[ex][na]['bias'] = mean_bias
            reg_data_stat[ex][na]['NMB'] = normalized_mean_bias
            reg_data_stat[ex][na]['RMSE'] = RMSE

            plot_scatter_improve(axes[i],
                                 c_atom.values,
                                 c_echam_txy.values,
                                 fr'$\bf{na}$' + f'\n{stat}',
                                 ds_atom_vs_daily_filter['std_daily_observ'])

        axes[0].set_ylabel(f'Model {mo_var_title}', fontsize='16')
        axes[3].set_ylabel(f'Model {mo_var_title}', fontsize='16')

        axes[3].set_xlabel(f'ATom {at_var}', fontsize='16')
        axes[4].set_xlabel(f'ATom {at_var}', fontsize='16')
        axes[5].set_xlabel(f'ATom {at_var}', fontsize='16')
        # axes[7].set_xlabel(f'ATom {at_var}', fontsize='16')

        plt.tight_layout()
        plt.savefig(f'{global_vars.plot_dir}{ex}_{mo_var_title}_model_atom.png', dpi=300)
        plt.close()

    return reg_data_stat
        # Taylor_diagram.taylor_diag(reg_data_4_taylor_obs, reg_data_4_taylor_mod)
