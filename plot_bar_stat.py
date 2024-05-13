import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.colors as mcolors


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
                    c=da_map['moa_oc_ratio'].values*100,
                    vmax = 50,
                    cmap=cmap, transform=ccrs.PlateCarree())
    cbar = subfig2.colorbar(im, orientation="horizontal", extend='max')  # ,cax = cbar_ax
    cbar.ax.tick_params(labelsize=12)
    cbar.set_label(label='$MOA/(MOA+OC)$', fontsize=12, weight='bold')
    ax.coastlines()
    plt.savefig(f'plots/Stat_regions_bar_map.png')


if __name__ == '__main__':
    data = pd.read_pickle('stat_exp_regions.pkl')
    data_ratio = pd.read_pickle('moa_moa_oc_ratio.pkl')

    new_var_na = []
    for i in data["Experiments"].values:
        if i == 'ac3_arctic_OA_var':
            new_var_na.append("MOA+OC")
        if i == 'ac3_arctic_MOA_var':
            new_var_na.append("MOA")
        if i == 'echam_base_var':
            new_var_na.append("OC")
    data["Model variables"] = new_var_na

    plot_multiplot(data, data_ratio)

    
    fig, ax = plt.subplots(2, 1, figsize=(6,3))
    axs = ax.flatten()
    pl = sns.barplot(data=data, x='Regions', y='NMB', hue="Model variables", width=0.6, ax=axs[0])
    ax[0].legend_.remove()

    # plt.savefig(f'plots/Stat_regions_NMB_bar.png')
    # plt.close()

    # fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(data=data, x='Regions', y='Pearson Coef.', hue="Model variables", width=0.6, ax=axs[1])
    ax[1].legend_.remove()
    print(data)
    #sns.barplot(data=data, x='Regions', y='Mean Bias', hue="Model variables", width=0.6, ax=axs[2])
    #ax[2].legend_.remove()

    pl.legend(loc='upper center', bbox_to_anchor=(0.5, 1.4), ncol=3)
    fig.tight_layout()

    plt.savefig(f'plots/Stat_regions_bar.png')
    plt.close()
