p_main = '/work/bb1005/b381361/'
base_path = f'{p_main}echam_postproc/aerosol_data_comparison/ATom/ATom-merge_ncfiles/MER-SAGA'
var_list_atom = ['SeaSaltMass_PALMS','BioBurnMass_PALMS','OilCombMass_PALMS']
plot_dir = f'{p_main}echam_postproc/moa_oa_aerosols_evaluation/plots/'
path_atom_meta = f'{base_path}*.nc'

height_criteria = 1000
p_model = f'{p_main}my_experiments/'
model_var = ['OA', 'MOA', 'OC']#['SS','SS']
experiments = ['ac3_arctic', 'ac3_arctic', 'echam_base']  # ,
exp_id = ['ac3_arctic_OA', 'ac3_arctic_MOA', 'echam_base']  # ,

atom_var = 'OA_PM1_AMS'#'SeaSaltMass_PALMS'#
atom_plot_varna = 'OA'#'SS'##
data_units = '${\mu}$g/m3'
