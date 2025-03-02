import pandas as pd
import numpy as np
import numpy.typing as npt
from pathlib import Path
import warnings
from .utils import create_folder

# Constants

yw = 9.81 # kN/m3
g = 9.81 # m/s2

# General function

def initialize_preprocessing(loading_path: Path, properties_path: Path, unloading_path: Path, export_path: Path, format: str='byprobe') -> None:
	
	if format == 'simultaneous':
		simultaneous2byprobe(loading_path)	
		
	save_loading_data(loading_path, export_path)
	save_properties_data(properties_path, export_path)
	save_unloading_data(unloading_path, export_path)

# --- loading stage ---

def split_simultaneous(input_path: Path, name_sections: list[str], ids: npt.NDArray, data: npt.NDArray):
	for section in name_sections:
		splitted_section = section.split('_')
		id = np.int64(splitted_section[0])
		load = str(float(splitted_section[-1]))
		probe = splitted_section[-2]

		byprobe_dir = input_path/probe
		create_folder(byprobe_dir)
		
		arg = np.nonzero(ids==id)
		probe_data = data[arg]
		probe_data[:, 0] = np.arange(start=1, stop=probe_data.shape[0]+1)

		np.savetxt(byprobe_dir/f'loading_{probe}_{load}.txt', probe_data, delimiter=',', 
				   header='time [s],deformation [mm]', fmt=['%d', '%.3f'])

def simultaneous2byprobe(input_path: Path) -> None:
	for file_path in input_path.iterdir():
		if file_path.is_file():
			file_name = file_path.stem
			name_sections = file_name.split('-')
			data = np.loadtxt(file_path, usecols=[0, 1], delimiter=',', dtype=np.float64)
			ids = np.loadtxt(file_path, usecols=[3], delimiter=',', dtype=np.int64)

			split_simultaneous(input_path, name_sections, ids, data)

def read_byprobe(byprobe_dir: Path) -> dict:
	loading_dict = dict()

	for file_path in byprobe_dir.iterdir():
		file_name = file_path.stem
		load = str(float(file_name.split('_')[-1]))

		data = np.loadtxt(file_path, delimiter=',', dtype=np.float64)
		time = data[:, 0]
		deformation = data[:, 1]

		consolidation_curve = dict(time=time, deformation=deformation)
		loading_dict.update({load: consolidation_curve})
	
	return loading_dict

def save_loading_data(input_path: Path, export_path: Path) -> None:

	for byprobe_dir in input_path.iterdir():
		if byprobe_dir.is_dir():
			probe = byprobe_dir.stem
			create_folder(export_path/probe) # All the probes are diferent!!!

			loading_dict = read_byprobe(byprobe_dir)
			np.save(export_path/probe/'loading.npy', loading_dict)

# --- unloading stage ---

def read_unloading(unloading_file_path: Path) -> tuple[np.ndarray]:
	data = np.loadtxt(unloading_file_path, delimiter=',', dtype=np.float64)
	loads = data[:, 0]
	values = data[:, 1]
	# deformations = data[:, 1]

	return loads, values
	# return loads, deformations

def save_unloading_data(unloading_path: Path, export_path: Path) -> None:
	for file_path in unloading_path.iterdir():
		probe = file_path.stem.split('_')[-1]
		loads, values = read_unloading(file_path)
		# loads, deformations = read_unloading(file_path)
		unloading_dict = dict(loads=loads, values=values)
		# unloading_dict = {loads=loads, deformations=deformations}
		np.save(export_path/probe/"unloading.npy", unloading_dict)

# --- Properties ---

def read_properties(properties_file_path: Path) -> tuple[npt.NDArray]:
	properties = np.zeros(11, dtype='<U12')
	values = np.zeros(11, dtype=np.float64)
	
	with warnings.catch_warnings():
		# There is a warning generated due to the combination os np.loadtxt and dtype='U' which has no issue on the performance
		warnings.simplefilter('ignore')
		_properties = np.loadtxt(properties_file_path, usecols=0, delimiter=',', dtype='U')
		_values = np.loadtxt(properties_file_path, usecols=1, delimiter=',', dtype=np.float64)

	# height [m]
	properties[0] = _properties[0]
	values[0] = _values[0]/1e3

	# diameter [m]
	properties[1] = _properties[1]
	values[1] = _values[1]/1e3

	# Gs [-]
	properties[2] = _properties[2]
	values[2] = _values[2]

	# initial water content [-]
	properties[3] = _properties[3]
	values[3] = _values[3]

	# probe mass [kg]
	properties[4] = 'mm'
	values[4] = (_values[4] - _values[5])/1e3
	
	# block mass [kg]
	properties[5] = _properties[6]
	values[5] = _values[6]/1e3

	# area [m2]
	properties[6] = 'A'
	values[6] = np.pi/4 * values[1]**2

	# volume [m3]
	properties[7] = 'V'
	values[7] = values[6] * values[0]

	# total unit weight [kN/m3]
	properties[8] = 'yt'
	values[8] = (values[4]/values[7] * g)/1e3

	# initial void rate [-]
	properties[9] = 'eo'
	values[9] = values[2]*yw/values[8] * (1+values[3]) - 1

	# lever arm [-]
	properties[10] = _properties[7]
	values[10] = _values[7]

	return properties, values

def save_properties_data(properties_path: Path, export_path: Path) -> None:
	for file_path in properties_path.iterdir():
		probe = file_path.stem.split('_')[-1]
		properties, values = read_properties(file_path)
		properties_dict = dict(properties=properties, values=values)
		np.save(export_path/probe/"properties.npy", properties_dict)