import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import seaborn as sns


def plot_multiplot(data):
    fig = plt.figure(constrained_layout=True, figsize=(10, 7))

    (subfig1, subfig2) = fig.subfigures(nrows=1, ncols=1)
    axs = subfig1.subplots(nrows=2, ncols=1, sharex=True)
    sns.barplot(data=data, x='Regions', y='NMB', hue="Experiments", ax=axs[0])
    sns.barplot(data=data, x='Regions', y='R', hue="Experiments", ax=axs[1])

    # ax = subfig1.subplots(nrows=1, ncols=1, sharex=True,
    #                       subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})
    # orig_cmap = plt.get_cmap('rainbow')
    # colors = orig_cmap(np.linspace(0.1, 1, 14))
    # cmap = mcolors.LinearSegmentedColormap.from_list("mycmap", colors)
    # im = ax.pcolormesh(da_ds.lon, da_ds.lat, da_ds*100,
    #                      cmap=cmap, transform=ccrs.PlateCarree(),
    #                      vmin=0, vmax=100)
    plt.savefig(f'plots/Stat_regions_bar_map.png')


if __name__ == '__main__':
    data = pd.read_pickle('stat_exp_regions.pkl')
    print(data['RMSE'], data['NMB'])
    new_var_na = []
    for i in data["Experiments"].values:
        if i == 'ac3_arctic_OA_var':
            new_var_na.append("MOA+OC")
        if i == 'ac3_arctic_MOA_var':
            new_var_na.append("MOA")
        if i == 'echam_base_var':
            new_var_na.append("OC")
    data["Model variables"] = new_var_na

    fig, ax = plt.subplots(3, 1, figsize=(6, 5))
    axs = ax.flatten()
    pl = sns.barplot(data=data, x='Regions', y='NMB', hue="Model variables", width=0.6, ax=axs[0])
    ax[0].legend_.remove()

    # plt.savefig(f'plots/Stat_regions_NMB_bar.png')
    # plt.close()

    # fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(data=data, x='Regions', y='Pearson Coef.', hue="Model variables", width=0.6, ax=axs[1])
    ax[1].legend_.remove()

    sns.barplot(data=data, x='Regions', y='RMSE', hue="Model variables", width=0.6, ax=axs[2])
    ax[2].legend_.remove()

    pl.legend(loc='upper center', bbox_to_anchor=(0.5, 1.4), ncol=3)
    fig.tight_layout()

    plt.savefig(f'plots/Stat_regions_bar.png')
    plt.close()
