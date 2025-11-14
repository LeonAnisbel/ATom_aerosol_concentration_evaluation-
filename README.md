# Evaluation of simulated organic aerosol against aircraft observations
> This project reads ATom data (also available on [Zenodo](10.5281/zenodo.17582048)) and linearly interpolates ECHAM-HAM model grid to the location and height of ATom aircraft.

* Run ATom_ECHAM_compare.py (or sbatch run_python_main.sh in levante) to perform the interpolation. This will generate
a pickle file (stat_exp_regions.pkl) which contains the observation and model interpolated data in addition to the
statistical indices for predefined oceanic regions (region_cond.py) and can later be used for the plots

* global_vars.py contains all global variables\
- Directories to ATom and pressure levels ECHAM data\
- height_criteria as the top level to select the data. Near the surface marine aerosols have a greater influence\
- name of model variable to compare to ATom\
- ATom variable to compare\

* plot_bar_stat. py create figures of the comparison of model and measurements color coded for the predefined oceanic regions for each model experiment (a scatter plot with the data , plus a bar plot with relevant statistics). These plots were published by [Leon-Marcos et al. 2025](https://doi.org/10.5194/gmd-18-4183-2025) and in the doctoral thesis by Anisbel Leon Marcos at Leipzig University.

* region_cond.py contains the definition of the ocean regions used in the comparison

