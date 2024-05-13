import numpy as np
import math
import global_vars
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


def get_statistics(c_atom, c_echam_txy):
    units = global_vars.data_units
    num_timesteps = len(c_atom.time)

    # model
    std_model = float(np.nanstd(c_echam_txy, ddof=1))  # model data's standard deviation at station location
    mean_model = float(np.nanmean(c_echam_txy))  # model data's mean at station location

    # observations
    std_obs = float(np.nanstd(c_atom, ddof=1))  # standard deviation of observed values
    mean_obs = float(np.nanmean(c_atom))  # mean of observed values over time

    # model-observations
    # root mean square error btw. model and observations at station location
    MSE = mean_squared_error(c_atom, c_echam_txy)
    RMSE = float(math.sqrt(MSE))

    # mean bias btw. model and observation at station location
    mean_bias = np.nanmean(np.subtract(c_echam_txy, c_atom))
    # print(mean_bias, np.nanmean(c_echam_txy - c_atom))
    # print(c_echam_txy, c_atom)

    # normalized mean biases btw. model and observations, at station locations
    normalized_mean_bias = np.nansum(np.subtract(c_echam_txy, c_atom)) / np.nansum(c_atom)

    # Pearson's correlation coefficient
    pearsons_coeff = np.corrcoef(c_atom, c_echam_txy)[0, 1]

    # index of agreement
    ioa = 1 - (np.nansum(np.square(c_atom - c_echam_txy))) / (
        np.nansum(np.square(np.abs(c_echam_txy - np.nanmean(c_atom)) + np.abs(c_atom - np.nanmean(c_atom)))))

    # mean fractional bias
    mean_fractional_bias = np.nanmean(2 * (c_echam_txy - c_atom) / (c_echam_txy + c_atom))

    # mean fractional errors
    mean_fractional_error = np.nanmean(2 * np.abs(c_echam_txy - c_atom) / (c_echam_txy + c_atom))

    # model values with respect to obs. values
    m_t_wrt_o_t = c_echam_txy.values / c_atom.values

    # fraction of complete data pairs where model is within a factor of 2 of observation
    fac2 = np.count_nonzero(np.logical_and(0.5 <= m_t_wrt_o_t, m_t_wrt_o_t <= 2)) / num_timesteps

    # fraction of complete data pairs where model is within a factor of 10 of observation
    fac10 = np.count_nonzero(np.logical_and(0.1 <= m_t_wrt_o_t, m_t_wrt_o_t <= 10)) / num_timesteps

    statistical_quantities = [
        ['mean standard deviation (of model, at station location)', std_model, units],
        ['model mean (at station location)', mean_model, units],
        ['standard deviation of observations', std_obs, units],
        ['mean of observations', mean_obs, units],
        ['mean RMSE (btw. model and observations, at station location)', RMSE, units],
        ['mean bias (btw. model and observations)', mean_bias, units],
        ['normalized mean bias (btw. model and observations, at station location)', normalized_mean_bias, units],
        ["Pearson's correlation coefficient (btw. model and observations, at station location)", pearsons_coeff, ''],
        ['index of agreement (btw. model and observations, at station location)', ioa, '']]

    # Coefficient of Determination-R2 score
    r2 = r2_score(c_atom, c_echam_txy)
    # for statistical_quantity in statistical_quantities:
    #     print(f'{statistical_quantity[0]} = {statistical_quantity[1]:.2f} {statistical_quantity[2]}\n')

    return std_model, std_obs, RMSE, mean_bias, normalized_mean_bias, pearsons_coeff, r2, statistical_quantities
