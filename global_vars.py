p_main = '/work/bb1005/b381361/'
base_path = f'{p_main}echam_postproc/aerosol_data_comparison/ATom/ATom-merge_ncfiles/MER-SAGA'
var_list_atom = ['SeaSaltMass_PALMS','BioBurnMass_PALMS','OilCombMass_PALMS']
plot_dir = f'{p_main}echam_postproc/moa_oa_aerosols_evaluation/plots/'
path_atom_meta = f'{base_path}*.nc'

height_criteria = 1000
p_model = f'{p_main}my_experiments/'
model_var = ['SS','SS']#['OA', 'OC']
experiments = ['ac3_arctic','echam_base']  # ,
atom_var = 'SeaSaltMass_PALMS'#'OA_PM1_AMS'
atom_plot_varna = 'SS'#'OA'
data_units = '${\mu}$g/m3'
