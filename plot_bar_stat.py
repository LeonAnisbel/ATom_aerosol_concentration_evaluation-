import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker

import global_vars
import statistics_atom

font = 12
def each_panel_fig(ax, data, var_na, lims, tick_space, title, top_pannel=False):
    """
    Create bar plots of statistics
    :var ax: matplotlib axes
    :var data: pandas.DataFrame with statistics
    :param var_na: statistical parameter name
    :param lims: maximum y-axis limit
    :param tick_space: space for plotting axis ticks
    :param title: subplot title
    :param top_pannel: boolean, whether to plot top panel
    :return: matplotlib object
    """
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


    for bars, hatch, legend_handle in zip(ax.containers, ['////', '----'], pl.legend_.legend_handles):
        for bar, color in zip(bars, palette):
            bar.set_facecolor(color)
            bar.set_hatch(hatch)
        # update the existing legend, use twice the hatching pattern to make it denser
        legend_handle.set_hatch(hatch + hatch)

    if not top_pannel:
        ax.legend_.remove()

    if title!= r'$\bf{(e)}$':
        ax.set(xlabel=None)
        ax.set_xticklabels(['S. Atlantic', 'S. Pacific', 'C. Pacific'], rotation=45)
    ax.set_title(title,
                 loc='left',
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
    """
    Adding diagonal lines in logarithmic axis
    :var axis: matplotlib axis
    :var x: x value
    :var y: y value
    :param style: line style
    :return: None
    """
    axis.loglog(x, y,
              color="black",
              linestyle=style,
              alpha=0.5,
              linewidth=0.5)

def setbox_pos(axs, x):
    """
    Creates extra space for legend
    """
    box = axs.get_position()
    axs.set_position([box.x0+x, box.y0 + box.height * 0.1+0.02,
                         box.width, box.height * 0.9])

def scatter_plot(data_new, ax, parameter, title, var, f):
    """
    Used to create a scatter plot per panel
    :var data_new: dataframe with model interpolated values, ATom observations and corresponding region names
    :param ax: matplotlib axes object
    :param parameter: statistics to plot as text
    :param title: title of plot
    :param var: name of variable
    :param f: font size
    :return: matplotlib object
    """
    color_reg = ['y', 'r', 'lightgreen'] #, 'g', 'm', 'k'
    pl = sns.scatterplot(data=data_new,
                         x="Observation",
                         y="Model",
                         hue=" ",
                         style=" ",
                         palette=color_reg,
                         ax = ax)
    ax.set_yscale('log')
    ax.set_xscale('log')
    yli_min = 10 ** -5
    ax.set_ylim((yli_min, 10 ** 0))
    ax.set_xlim((yli_min, 10 ** 0))
    ax.set_xlabel('Observation OA (µg m$^{-3}$)',
                  fontsize=f)
    ax.set_ylabel(f'Model {var} ' +  '(µg m$^{-3}$)',
                  fontsize=f)

    k = 10
    set_log_ax(ax,
               [yli_min, 10 ** 0],
               [yli_min, 10 ** 0],
              "-",)
    set_log_ax(ax,
               [yli_min , 10 ** 0],
               [yli_min*k, 10 ** 0 * k],
           ":")
    set_log_ax(ax,
              [yli_min, 10 ** 0] ,
              [yli_min/k, 10 ** 0 / k],
                ":")

    ax.set_title(f'{title[0]} ({var})',
                 loc='right',
                 fontsize=f)
    ax.set_title(title[1],
                 loc='left',
                 fontsize=f)
    ax.tick_params(axis='both',
                   labelsize=f)

    ax.text(0.1, 0.95,
            parameter,
            verticalalignment='top',
            horizontalalignment='left',
            transform=ax.transAxes,
            color='k',
            fontsize=f-2)
    ax.legend_.remove()

    ax.grid(linestyle='--',
            linewidth=0.4)

    return pl

def create_scatter_plots(axsLeft, data_total, experiments, f):
    """
    Creates scatter plot for the SPMOAoff and SPMOAon experiments of the measured
    Organic Aerosol in ATom aircraft campaign in contrast to modelled organic carbon (OC)
    or OC+PMOA for each experiment, respectively
    :param axsLeft: list of matplotlib axes
    :var data_total: dictionary with model and ATom data
    :param experiments: experiment names
    :param f: font size
    :return: None
    """
    indices = [r'$\bf{(a)}$', r'$\bf{(b)}$']
    var = ['OC', 'PMOA+OC']
    left_panel_list = [False, True]
    for i, exp in enumerate(experiments):
        data_exp = data_total[data_total['Experiments'] == exp]
        region_names = []
        model = []
        observation = []
        for region in data_exp['Regions']:
            data_exp_region = data_exp[data_exp['Regions'] == region]
            for obs, mod in zip(data_exp_region["atom_vals"].values[0], data_exp_region["model_vals"].values[0]):
                region_names.append(region)
                observation.append(obs)
                model.append(mod)
        data_new = pd.DataFrame(data={' ': region_names,
                                      'Model': model,
                                      'Observation': observation})

        _, _, RMSE, mean_bias, NMB, pearsons_coeff, pval_corr, _, res_lin_reg = (
            statistics_atom.get_statistics(np.array(observation), np.array(model)))
        parameters = (f' y = {np.round(res_lin_reg.slope, 2)}x'
                      f'{format(res_lin_reg.intercept, '.3f')}\n'
                      f' R: {np.round(pearsons_coeff, 2)} \n \n'
                      f' RMSE: {np.round(RMSE, 2)} \n '
                      f'MB: {np.round(mean_bias, 2)} \n '
                      f'NMB: {np.round(NMB, 2)} \n ')

        pl_sct = scatter_plot(data_new,
                              axsLeft[i],
                              parameters,
                              [experiments_names[i], indices[i]],
                              var[i],
                              f,
                              right_panel=left_panel_list[i])

    x = [0, 0.05]
    for i, ax in enumerate(axsLeft):
        setbox_pos(ax, x[i])
    handles, labels = pl_sct.get_legend_handles_labels()
    subfigs[0].legend(handles=handles,
                      labels=labels,
                      ncol=3,
                      loc='lower center',
                      fontsize=f)

if __name__ == '__main__':
    data = pd.read_pickle('stat_exp_regions.pkl')
    data_ratio = pd.read_pickle('moa_moa_oc_ratio.pkl')

    experiments = ['echam_base_var', 'ac3_arctic_OA_var']

    experiments_names = ["SPMOAoff", "SPMOAon"]


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
    data = data.rename(columns={'RMSE':f'RMSE\n({global_vars.unit_atom})',
                                'Mean Bias':f'MB\n({global_vars.unit_atom})'})
    data_south_reg = data[(data['Regions'] == 'South Atlantic') |
                          (data['Regions'] == 'South Pacific') |
                          (data['Regions'] == 'Central Pacific') ]

    data_off = data_south_reg[data_south_reg["Model variables"]==experiments_names[0]]
    data_on = data_south_reg[data_south_reg["Model variables"]==experiments_names[1]]
    data_total = pd.concat([data_off, data_on])


######################################################################
    # Plot used for paper
    fig, axsLeft = plt.subplots(1,
                                2,
                                figsize=(7, 5))
    subfigs = [fig]
    create_scatter_plots(axsLeft,
                         data_total,
                         experiments,
                         font) # Scatter plots for both experiments
    plt.savefig(f'plots/scatter_plot_regions.png',
                dpi=300)
    plt.close()

 ######################################################################
# Create scatter and barplot together for Thesis
    fig = plt.figure(layout='constrained',
                     figsize=(12, 6))
    subfigs = fig.subfigures(1, 2,
                             wspace=0.038,
                             width_ratios=[2, 1])
    axsLeft = subfigs[0].subplots(1, 2)
    create_scatter_plots(axsLeft,
                         data_total,
                         experiments,
                         14) # Scatter plots for both experiments

    axsRight = subfigs[1].subplots(3, 1, sharex=True) # Bar plot of statistical parameters only for southern regions
    # pl = each_panel_fig(axsRight[0],
    #                     data_total,
    #                     'Pearson Coef.',
    #                     [-0.1, 1],
    #                     0.3,
    #                     r'$\bf{(c)}$',
    #                    top_pannel=True)
    pl = each_panel_fig(axsRight[0],
                        data_total,
                        'MB\n(µg m$^{-3}$)',
                        [-0.1, 0.1],
                        0.05,
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

    plt.savefig(f'plots/scatter_bar_plot_regions.png', dpi=300)
    plt.close()