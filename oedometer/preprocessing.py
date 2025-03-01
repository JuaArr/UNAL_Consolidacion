import pandas as pd
import numpy as np
import numpy.typing as npt
from pathlib import Path
from .utils import create_folder

# Constants

yw = 9.81 # kN/m3
g = 9.81 # m/s2

# General function

def pp_data(loading_path: Path, \
			properties_path: Path, \
			unloading_path: Path, \
			export_path: Path, \
			is_pinzuar: bool = False) -> None:
	
	if is_pinzuar:
		pass
	else:
		_file_path = next(loading_path.glob("*.txt"))
		probes = [_name_section.split('_')[-2] for _name_section in _file_path.stem.split('-')]
		for probe in probes: create_folder(export_path / probe)		
		
		save_loading_data(loading_path, export_path, probes)
		save_properties_data(properties_path, export_path)
		save_unloading_data(unloading_path, export_path)

# loading stage

def read_file(file_path: Path, container: dict[str: dict], probes: list[str], loads: list[float]) -> dict[str: dict]:
	n_probes = len(probes)
	expected_dtype: dict[int: str] = {0: "int", 1: "float", 2: "str", 3: "int"}
	data = pd.read_csv(file_path, header = None, dtype = expected_dtype)

	for idx in range(n_probes):
		probe_data = data[data.iloc[:, 3] == (idx+1)].values
		probe_data = probe_data[:, 0:2]
		probe_data[:, 0] = np.arange(start=0, stop=probe_data.shape[0])

		container[probes[idx]][loads[idx]] = probe_data

	return container
	
def read_folder(input_path: Path, probes: list[str]) -> dict[str: dict]:
	container = {probe: dict() for probe in probes}

	for file_path in input_path.iterdir():
		file_name = file_path.stem
		loads = [str(float(name_section.split('_')[-1])) for name_section in file_name.split('-')] # Por si son diferentes (no deberia pero aja ...)
		container = read_file(file_path, container, probes, loads)

	return container

def save_loading_data(input_path: Path, export_path: Path, probes: list[str]) -> None:
	loading_data = read_folder(input_path, probes)
	
	for probe in loading_data.keys():
		probe_loading_data = loading_data[probe]
		loads = np.array(list(probe_loading_data.keys()), dtype=float)
		loads = loads[np.argsort(loads)]
		values = [probe_loading_data[str(load)] for load in loads]

		loading_dict = {'loads': loads, 'values': values}
		np.save(export_path/probe/'loading.npy', loading_dict)

# unloading stage

def read_unloading(unloading_file_path: Path) -> tuple[np.ndarray]:
	expected_dtype: dict[int: str] = {0: "float", 1: "str", 2: "float", 3: "str"}
	data = pd.read_csv(unloading_file_path, dtype=expected_dtype)
	loads = data.iloc[:, 0].values
	values = data.iloc[:, 2].values

	return loads, values

def save_unloading_data(unloading_path: Path, export_path: Path) -> None:
	for file_path in unloading_path.iterdir():
		probe = file_path.stem.split('_')[-1]
		loads, values = read_unloading(file_path)
		unloading_dict = {'loads': loads, 'values': values}
		np.save(export_path/probe/"unloading.npy", unloading_dict)

# Properties

def read_properties(properties_file_path: Path) -> tuple[np.ndarray]:
	expected_dtype: dict[int: str] = {0: "str", 1: "float", 2: "str"}
	data = pd.read_csv(properties_file_path, dtype=expected_dtype)
	_properties = data.iloc[:, 0].values
	_values = data.iloc[:, 1].values

	properties = np.zeros(11, dtype='U10')
	values = np.zeros(11, dtype=float)

	# height
	properties[0] = _properties[0]
	values[0] = _values[0]/1e3

	# diameter
	properties[1] = _properties[1]
	values[1] = _values[1]/1e3

	# Gs
	properties[2] = _properties[2]
	values[2] = _values[2]

	# initial water content
	properties[3] = _properties[3]
	values[3] = _values[3]

	# probe mass
	properties[4] = 'mm'
	values[4] = (_values[4] - _values[5])/1e3
	
	# block mass
	properties[5] = _properties[6]
	values[5] = _values[6]/1e3

	# area
	properties[6] = 'A'
	values[6] = np.pi/4 * values[1]**2

	# volume
	properties[7] = 'V'
	values[7] = values[6] * values[0]

	# total unit weight
	properties[8] = 'yt'
	values[8] = (values[4]/values[7] * g)/1e3

	# initial void rate
	properties[9] = 'eo'
	values[9] = values[2]*yw/values[8] * (1+values[3]) - 1

	# lever arm
	properties[10] = _properties[7]
	values[10] = _values[7]

	return properties, values

def save_properties_data(properties_path: Path, export_path: Path) -> None:
	for file_path in properties_path.iterdir():
		probe = file_path.stem.split('_')[-1]
		properties, values = read_properties(file_path)
		properties_dict = {'properties': properties, 'values': values}
		np.save(export_path/probe/"properties.npy", properties_dict)