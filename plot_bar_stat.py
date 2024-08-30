import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker

import global_vars


def plot_multiplot(da_stat, da_map):
    fig = plt.figure(constrained_layout=True, figsize=(10, 7))

    (subfig1, subfig2) = fig.subfigures(nrows=1, ncols=2)
    axs = subfig1.subplots(nrows=2, ncols=1, sharex=True)
    pl = sns.barplot(data=da_stat, x='Regions', y='NMB', hue="Model variables", ax=axs[0])
    sns.barplot(data=da_stat, x='Regions', y='Pearson Coef.', hue="Model variables", ax=axs[1])
    axs[0].legend_.remove()
    axs[1].legend_.remove()
    pl.legend(loc='upper center', bbox_to_anchor=(0.5, 1.4), ncol=3)

    ax = subfig2.subplots(nrows=1, ncols=1, sharex=True,
                          subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})
    orig_cmap = plt.get_cmap('jet')
    colors = orig_cmap(np.linspace(0.1, 1, 14))
    cmap = mcolors.LinearSegmentedColormap.from_list("mycmap", colors)
    print(da_map['moa_oc_ratio'])
    im = ax.scatter(da_map['lon'].values,
                    da_map['lat'].values,
                    c=da_map['moa_oc_ratio'].values * 100,
                    vmax=50,
                    cmap=cmap, transform=ccrs.PlateCarree())
    cbar = subfig2.colorbar(im, orientation="horizontal", extend='max')  # ,cax = cbar_ax
    cbar.ax.tick_params(labelsize=12)
    cbar.set_label(label='$MOA/(MOA+OC)$', fontsize=12, weight='bold')
    ax.coastlines()
    plt.savefig(f'plots/Stat_regions_bar_map.png')


def each_panel_fig(ax, data, var_na, lims, tick_space, title):
    pl = sns.barplot(data=data, x='Regions', y=var_na, hue="Model variables", palette=color, width=0.6, ax=ax)
    if title!= r'$\bf{(c)}$':
        ax.set(xlabel=None)
        ax.set_xticklabels([])
    ax.set_title(title, loc='right', fontsize=18)
    ax.legend_.remove()
    ax.set_ylim(lims)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_space))
    ax.grid(linestyle='--', linewidth=0.4)

    return pl


if __name__ == '__main__':
    data = pd.read_pickle('stat_exp_regions.pkl')
    data_ratio = pd.read_pickle('moa_moa_oc_ratio.pkl')

    new_var_na = []
    for i in data["Experiments"].values:
        if i == 'ac3_arctic_OA_var':
            new_var_na.append("SPMOAon (PMOA+OC)")
        if i == 'ac3_arctic_MOA_var':
            new_var_na.append("PMOA")
        if i == 'echam_base_var':
            new_var_na.append("SPMOAoff (OC)")
    data["Model variables"] = new_var_na

    # plot_multiplot(data, data_ratio)
    print(data)
    fig, ax = plt.subplots(3, 1, figsize=(14, 10))
    axs = ax.flatten()
    color = sns.color_palette("Paired")
    data = data.rename(columns={'RMSE':f'RMSE\n({global_vars.unit_atom})'})

    pl = each_panel_fig(ax[0], data, 'NMB', [-1, 3], 1, r'$\bf{(a)}$')
    plt.subplots_adjust(hspace=0.3)
    pl = each_panel_fig(ax[1], data, f'RMSE\n({global_vars.unit_atom})', [0, 0.4], 0.1, r'$\bf{(b)}$')
    pl.legend(loc='upper center', bbox_to_anchor=(0.5, 2.8), ncol=3, fontsize=14)
    pl = each_panel_fig(ax[2], data, 'Pearson Coef.', [-0.3, 1], 0.3, r'$\bf{(c)}$')

    for axs in ax:
        axs.tick_params(axis='both', labelsize='18')
        axs.yaxis.get_label().set_fontsize(18)
        axs.xaxis.get_label().set_fontsize(18)

    #fig.tight_layout()
    plt.savefig(f'plots/Stat_regions_bar.png', dpi=300)
    plt.close()
