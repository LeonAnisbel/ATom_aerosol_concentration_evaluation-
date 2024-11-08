p_main = '/work/bb1005/b381361/'
base_path = f'{p_main}echam_postproc/aerosol_data_comparison/ATom/ATom-merge_ncfiles/MER-SAGA'
var_list_atom = ['SeaSaltMass_PALMS','BioBurnMass_PALMS','OilCombMass_PALMS']
#plot_dir = f'{p_main}echam_postproc/moa_oa_aerosols_evaluation/plots/'
plot_dir = f'{p_main}echam_postproc/moa_oa_aerosols_evaluation/'

path_atom_meta = f'{base_path}*.nc'

height_criteria = 1000
#p_model = f'{p_main}my_experiments/'
p_model = '/scratch/b/b381361/'
model_var = ['OA', 'OC', 'ratio_MOA_MOA_OC']#['SS','SS']
experiments = ['ac3_arctic','echam_base']
exp_id = ['ac3_arctic_OA', 'echam_base']

atom_var = 'OA_PM1_AMS'#'SeaSaltMass_PALMS'#
atom_plot_varna = 'OA'#'SS'##
data_units = '${\mu}$g\m$^{3}$)'
unit_atom = '${\mu}$g\m$^{3}$'
