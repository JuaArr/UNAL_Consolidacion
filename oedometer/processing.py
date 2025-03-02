from pathlib import Path
import numpy as np
import numpy.typing as npt
import scipy.optimize as opt
from sklearn.metrics import root_mean_squared_error, r2_score
from .utils import save_table

# from raw data to required data

def consolidate_stages(loading_data: dict, unloading_data: dict, stages: npt.ArrayLike) -> tuple[npt.NDArray]:
	n_preloading_stages, n_loading_stages, n_unloading_stages = stages
	n_stages = n_preloading_stages + n_loading_stages + n_unloading_stages

	loads = np.empty(shape=(n_stages), dtype=np.float64)
	heights = np.empty(shape=(n_stages, 2), dtype=np.float64)

	sorted_loadings = sorted(list(loading_data.keys()), key=float)

	# Special case when load is equal to 0 (initial expansion or compression)
	initial_height = 0.0
	final_height = loading_data.get(sorted_loadings[0]).get('deformation')[0]
	loads[0] = 0.0
	heights[0, :] = initial_height, final_height

	# General case. Taken from data
	for idx in range(1, n_stages):
		if idx < 1+n_loading_stages:
			fixed_idx = idx-1

			initial_height = max(final_height, loading_data.get(sorted_loadings[fixed_idx]).get('deformation')[0])
			final_height = loading_data.get(sorted_loadings[fixed_idx]).get('deformation')[-1]
			loads[idx] = np.float64(sorted_loadings[fixed_idx])
		else:
			fixed_idx = idx-1-n_loading_stages

			initial_height = final_height
			final_height = unloading_data.get('values')[fixed_idx]
			loads[idx] = unloading_data.get('loads')[fixed_idx]

		heights[idx, :] = initial_height, final_height

	return loads, heights

def load_correction(loads: npt.NDArray, properties: dict) -> npt.NDArray:
	
	names = properties.get('properties')

	arg = np.nonzero(names==np.str_('la'))
	lever_arm = properties.get('values')[arg][0]

	arg = np.nonzero(names=='bm')
	block_mass = properties.get('values')[arg][0]
	
	loads = lever_arm * loads + block_mass

	return loads

def calculate_stress(loads: npt.NDArray, properties: dict) -> npt.NDArray:
	"""
	Calculates the effective stress over the sample.

	Args:
		loads (NDArray):
		properties (dict):
	
	Returns:
		NDArray: The effective stress after a correction of the `loads`.
	"""
	
	names = properties.get('properties')

	arg = np.nonzero(names=='A')
	A = properties.get('values')[arg]
	
	loads = load_correction(loads, properties)
	stress = np.empty_like(loads)
	stress = loads/A * 9.81/1e3

	return stress

def calculate_settlement(heights: npt.NDArray) -> npt.NDArray:

	settlement = np.empty(shape=heights.shape[0], dtype=np.float64)
	settlement = heights[:, 0] - heights[:, -1] # equivalent to h_i - h_f

	return settlement

def calculate_strain(heights: npt.NDArray, properties: dict) -> npt.NDArray:

	names = properties.get('properties')

	arg = np.nonzero(names=='h')
	initial_height = properties.get('values')[arg]
	
	settlement = calculate_settlement(heights)
	strain = np.empty_like(settlement)
	strain = settlement/initial_height * 1e-3
	strain = np.cumsum(strain)

	return strain

def calculate_void_ratio(strain: npt.NDArray, properties: dict) -> npt.NDArray:
	
	names = properties.get('properties')
	
	arg = np.nonzero(names=='eo')
	initial_void_ratio = properties.get('values')[arg]

	void_ratio = np.empty_like(strain)
	void_ratio = initial_void_ratio - strain * (1+initial_void_ratio)

	return void_ratio

def calculate_strain_energy(stress: npt.NDArray, strain: npt.NDArray) -> npt.NDArray:

	iter_work =  (np.trapezoid(y=stress[:idx], x=strain[:idx]) for idx in range(1, stress.shape[0]+1))
	work = np.fromiter(iter=iter_work, dtype=np.float64)

	return work

# Fitting and data estimation

def semilog_model(s: npt.NDArray, params: npt.ArrayLike) -> npt.NDArray:
	a, b = params
	model = a*np.log10(s) + b 
	
	return model

def linear_model(s: npt.NDArray, params: npt.ArrayLike) -> npt.NDArray:
	a, b = params
	model = a*s + b

	return model

def residual_semilog(params: npt.ArrayLike, s: npt.NDArray, vr: npt.NDArray) -> npt.NDArray:
	residual = semilog_model(s, params) - vr

	return residual

def residual_linear(params: npt.ArrayLike, s: npt.NDArray, w: npt.NDArray) -> npt.NDArray:
	residual = linear_model(s, params) - w

	return residual

def fit_vr_s(s: npt.NDArray, vr: npt.NDArray) -> npt.NDArray:
	
	initial_guess = [-0.5, 1.0]
	bounds = ([-2.0, -np.inf], [2.0, np.inf])
	fitted = opt.least_squares(fun=residual_semilog, x0=initial_guess, bounds=bounds, args=(s, vr))
	params = fitted.x.astype(np.float64)

	return params

def fit_w_s(s: npt.NDArray, w: npt.NDArray) -> npt.NDArray:

	initial_guess = [0.2, 0.0]
	bounds = ([0.0, -np.inf], [np.inf, 0.0])
	fitted = opt.least_squares(fun=residual_linear, x0=initial_guess, bounds=bounds, args=(s, w))
	params = fitted.x.astype(np.float64)

	return params

# Addtional parameters

def intersection_two_functions(x, fun1, params1, fun2, params2):

	zero = fun1(x, params1) - fun2(x, params2)

	return zero

def calculate_strain_energy_params(stress: npt.NDArray, work: npt.NDArray, save_metrics: bool=False,
								   export_dir: Path|None=None) -> dict[np.float64|slice]:

	slice_w1 = slice(5)
	slice_w2 = slice(4, -2)
	params_w1 = fit_w_s(stress[slice_w1], work[slice_w1])
	params_w2 = fit_w_s(stress[slice_w2], work[slice_w2])

	pre_stress = opt.newton(func=intersection_two_functions, x0=10.0, args=(linear_model, params_w1, linear_model, params_w2))

	# Metrics
	rmse_w1 = root_mean_squared_error(work[slice_w1], linear_model(stress[slice_w1], params_w1))
	r2_w1 = r2_score(work[slice_w1], linear_model(stress[slice_w1], params_w1))
		
	rmse_w2 = root_mean_squared_error(work[slice_w2], linear_model(stress[slice_w2], params_w2))
	r2_w2 = r2_score(work[slice_w2], linear_model(stress[slice_w2], params_w2))

	if save_metrics:
		table: dict = {'Parameter': ['sp [kPa]', 'w1 [-]', 'w2 [-]'], 
					   'Value': [pre_stress, None, None],
					   'RMSE': [None, rmse_w1, rmse_w2],
					   'R2': [None, r2_w1, r2_w2]}
		
		save_table(file_path=export_dir/'strain_energy_metrics.txt', table=table, 
				   fmt=('.1e', '.3f', '.2e', '.2f'))

	return dict(pre_stress=pre_stress, params_w1=params_w1, slice_w1=slice_w1,
				params_w2=params_w2, slice_w2=slice_w2)

def calculate_compressibility_params(stress: npt.NDArray, void_ratio: npt.NDArray, stages: npt.ArrayLike, 
							  save_metrics: bool=False, export_dir: Path|None=None) -> dict[npt.NDArray|slice]:

	n_preloading_stages, n_loading_stages, n_unloading_stages = stages

	# Nota: Incluir un cambio de el punto de inicio para el calculo de la curva cc
	slice_cc = slice(n_preloading_stages+3, n_preloading_stages+n_loading_stages)
	slice_cr = slice(n_preloading_stages+n_loading_stages-1, n_preloading_stages+n_loading_stages+n_unloading_stages)
	params_cc = fit_vr_s(s=stress[slice_cc], vr=void_ratio[slice_cc])
	params_cr = fit_vr_s(s=stress[slice_cr], vr=void_ratio[slice_cr])

	# Metrics
	rmse_cc = root_mean_squared_error(void_ratio[slice_cc], semilog_model(stress[slice_cc], params_cc))
	r2_cc = r2_score(void_ratio[slice_cc], semilog_model(stress[slice_cc], params_cc))
		
	rmse_cr = root_mean_squared_error(void_ratio[slice_cr], semilog_model(stress[slice_cr], params_cr))
	r2_cr = r2_score(void_ratio[slice_cr], semilog_model(stress[slice_cr], params_cr))
	
	if save_metrics:
		table: dict = {'Parameter': ['Cc [-]', 'Cr [-]'], 
					   'Value': [-params_cc[0], -params_cr[0]],
					   'RMSE': [rmse_cc, rmse_cr],
					   'R2': [r2_cc, r2_cr]}
		
		save_table(file_path=export_dir/'compressibility_metrics.txt', table=table, 
				   fmt=('.1e', '.3f', '.2e', '.2f'))
	
	return dict(params_cc=params_cc, params_cr=params_cr, slice_cc=slice_cc, slice_cr=slice_cr)