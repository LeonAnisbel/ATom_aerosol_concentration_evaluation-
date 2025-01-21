import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker

import global_vars

font = 12
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


def each_panel_fig(ax, data, var_na, lims, tick_space, title, top_pannel=False):
    pl = sns.barplot(data=data,
                     x='Regions',
                     y=var_na,
                     hue="Model variables",
                     palette=['lightgrey', 'lightgrey'],
                     errorbar=None,
                     edgecolor='black',
                     width=0.6,
                     alpha=0.8,
                     ax=ax)
    palette = ['y', 'r', 'lightgreen']
    if top_pannel:
        pl.legend(loc='upper center',
                  bbox_to_anchor=(0.5, 1.5),
                  ncol=2,
                  fontsize=font)

        # Add pvalues on top of the bars
        hue_col = data["Regions"].unique()
        pval_pmoaoff, pval_pmoaon = [], []
        for col in hue_col:
            data_reg = data[data["Regions"] == col]
            pval = data_reg[data_reg["Model variables"]=='SPMOAoff']['pval'].values[0]
            pval_pmoaoff.append(round(pval, 2))
            pval = data_reg[data_reg["Model variables"]=='SPMOAon']['pval'].values[0]
            pval_pmoaon.append(round(pval, 2))

        labels = [pval_pmoaoff, pval_pmoaon]
        for c, lab in zip(ax.containers, labels):
            # add the name annotation to the top of the bar
            ax.bar_label(c, labels=lab, padding=3)  # rotation=90 if needed
            ax.margins(y=0.1)

    for bars, hatch, legend_handle in zip(ax.containers, ['////', '----'], pl.legend_.legendHandles):
        for bar, color in zip(bars, palette):
            bar.set_facecolor(color)
            bar.set_hatch(hatch)
        # update the existing legend, use twice the hatching pattern to make it denser
        legend_handle.set_hatch(hatch + hatch)

    if not top_pannel:
        ax.legend_.remove()

    if title!= r'$\bf{(e)}$':
        ax.set(xlabel=None)
        ax.set_xticklabels([])
    ax.set_title(title,
                 loc='right',
                 fontsize=font)
    ax.set_ylim(lims)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_space))
    ax.xaxis.get_label().set_fontsize(font)
    ax.yaxis.get_label().set_fontsize(font)
    ax.tick_params(axis='both',
                   labelsize=font)

    ax.grid(linestyle='--',
            linewidth=0.4)

    return pl


def set_log_ax(axis, x, y, style):
    axis.loglog(x, y,
              color="black",
              linestyle=style,
              alpha=0.5,
              linewidth=0.5)

def setbox_pos(axs, x):
    box = axs.get_position()
    axs.set_position([box.x0+x, box.y0 + box.height * 0.1+0.02,
                         box.width, box.height * 0.9])

def scatter_plot(data_new, ax, parameter, title, var, right_panel=False):
    color_reg = ['y', 'r', 'lightgreen', 'g', 'm', 'k']
    pl = sns.scatterplot(data=data_new,
                         x="Observation",
                         y="Model",
                         hue=" ",
                         style=" ",
                         palette=color_reg,
                         ax = ax)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylim((10 ** -3, 10 ** 0))
    ax.set_xlim((10 ** -3, 10 ** 0))
    ax.set_xlabel('Observation OA (${\mu}$g m$^{-3}$)',
                  fontsize=font)
    ax.set_ylabel(f'Model {var} ' +  '(${\mu}$g m$^{-3}$)',
                  fontsize=font)

    k = 10
    set_log_ax(ax,
               [10 ** -3, 10 ** 0],
               [10 ** -3, 10 ** 0],
              "-",)
    set_log_ax(ax,
               [10 ** -3 , 10 ** 0],
               [10 ** -3*k, 10 ** 0 * k],
           ":")
    set_log_ax(ax,
              [10 ** -3, 10 ** 0] ,
              [10 ** -3/k, 10 ** 0 / k],
                ":")

    ax.set_title(f'{title[0]} ({var})',
                 loc='center',
                 fontsize=font)
    ax.set_title(title[1],
                 loc='right',
                 fontsize=font)
    ax.tick_params(axis='both',
                   labelsize=font)

    ax.text(0.1, 0.95,
            parameter,
            verticalalignment='top',
            horizontalalignment='left',
            transform=ax.transAxes,
            color='k',
            fontsize=font)
    ax.legend_.remove()

    return pl



if __name__ == '__main__':
    data = pd.read_pickle('stat_exp_regions.pkl')
    data_ratio = pd.read_pickle('moa_moa_oc_ratio.pkl')

    experiments = ['echam_base_var', 'ac3_arctic_OA_var']
    parameters = ['RMSE: 0.1 \n NMB: 0.01 \n R: 0.35',
                  'RMSE: 0.15 \n NMB: 0.93 \n R: 0.46']
    experiments_names = ["SPMOAoff", "SPMOAon"]
######################################################################
# Create scatter and barplot together
    fig = plt.figure(layout='constrained',
                     figsize=(12, 6))
    subfigs = fig.subfigures(1, 2,
                             wspace=0.03,
                             width_ratios=[2, 1])
    axsLeft = subfigs[0].subplots(1, 2)

# Scatter plots for both experiments
    indices = [r'$\bf{(a)}$', r'$\bf{(b)}$']
    var = ['OC', 'PMOA+OC']
    left_panel_list= [False, True]
    for i, exp in enumerate(experiments):
        data_exp = data[data['Experiments']== exp]
        region_names = []
        model = []
        observation  = []
        for region in data_exp['Regions']:
            data_exp_region = data_exp[data_exp['Regions']==region]
            for obs, mod in zip(data_exp_region["atom_vals"].values[0], data_exp_region["model_vals"].values[0]):
                region_names.append(region)
                observation.append(obs)
                model.append(mod)
        data_new = pd.DataFrame(data={' ':region_names,
                                      'Model':model,
                                      'Observation':observation})
        pl_sct = scatter_plot(data_new,
                              axsLeft[i],
                              parameters[i],
                              [experiments_names[i], indices[i]],
                              var[i],
                              right_panel = left_panel_list[i])

    x = [0, 0.05]
    for i, ax in enumerate(axsLeft):
        setbox_pos(ax, x[i])
    handles, labels = pl_sct.get_legend_handles_labels()
    subfigs[0].legend(handles=handles,
                       labels= labels,
                       ncol=3,
                       #bbox_to_anchor=(0.1, 0.1),
                       loc='lower center',
                       fontsize=font)

# Bar plot of statistical parameters only for southern regions
    new_var_na = []
    for i in data["Experiments"].values:
        if i == experiments[0]:
            new_var_na.append(experiments_names[0])
        if i == 'ac3_arctic_MOA_var':
            new_var_na.append("PMOA")
        if i == experiments[1]:
            new_var_na.append(experiments_names[1])
    data["Model variables"] = new_var_na
    color = sns.color_palette("Paired")
    data = data.rename(columns={'RMSE':f'RMSE\n({global_vars.unit_atom})'})
    data_south_reg = data[(data['Regions'] == 'S. Atlantic') |
                          (data['Regions'] == 'S. Pacific') |
                          (data['Regions'] == 'C. Pacific')]
    data_off = data_south_reg[data_south_reg["Model variables"]==experiments_names[0]]
    data_on = data_south_reg[data_south_reg["Model variables"]==experiments_names[1]]
    data_total = pd.concat([data_off, data_on])

    axsRight = subfigs[1].subplots(3, 1, sharex=True)
    pl = each_panel_fig(axsRight[0],
                        data_total,
                        'Pearson Coef.',
                        [-0.1, 1],
                        0.3,
                        r'$\bf{(c)}$',
                       top_pannel=True)
    _ = each_panel_fig(axsRight[1],
                        data_total,
                        'NMB',
                        [-1, 1],
                        0.5,
                        r'$\bf{(d)}$')
    _ = each_panel_fig(axsRight[2],
                        data_total,
                        f'RMSE\n({global_vars.unit_atom})',
                        [0, 0.2],
                        0.05,
                        r'$\bf{(e)}$')
    for ax in axsRight:
        setbox_pos(ax, 0)

    # plt.show()
    plt.savefig(f'plots/scatter_bar_plot_regions.png', dpi=300)