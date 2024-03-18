import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy
import global_vars

def plot_help(subfig, C, titles, lon, lat):
    axes = subfig.subplots(nrows=1, ncols=1, sharex=True,
                           subplot_kw={'projection': ccrs.Robinson()})
    #     for i,ax in enumerate(axes):
    cmap = plt.get_cmap('Blues', 11)  # 11 discrete colors
    im = axes.pcolormesh(lon, lat, C,
                         cmap=cmap, transform=ccrs.PlateCarree(),
                         vmax = 1)
    axes.set_title(f'month = {titles}', fontsize='12')
    axes.coastlines()
    axes.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')

    #     cbar_ax = subfig.add_axes([0.1, -0.05, 0.8, 0.03])
    cbar = subfig.colorbar(im, orientation="horizontal")  # ,cax = cbar_ax
    cbar.ax.tick_params(labelsize=12)
    cbar.set_label(label="$MOA/(MOA+OC)$", size='large', weight='bold')

    gl = axes.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                   linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False

def plot_3_pannel(C, names, lon, lat,yrs):
    fig = plt.figure(constrained_layout=True, figsize=(10, 7))
    (subfig1, subfig2, subfig3) = fig.subfigures(nrows=1, ncols=3)
    subfigs = [subfig1, subfig2, subfig3]

    for idx, subf in enumerate(subfigs):
        plot_help(subf, C[idx], names[idx], lon, lat)

    # fig.suptitle(f'Multiannual monthly mean for {yrs[0]}-{yrs[1]}')
    # fig.tight_layout()

    plt.savefig(global_vars.plot_dir + f'3_pannel_sfc_conc_MOA_OA_{yrs[0]}-{yrs[1]}.png', dpi=300, bbox_inches="tight")

