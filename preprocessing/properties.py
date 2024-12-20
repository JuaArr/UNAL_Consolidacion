import numpy as np
import pandas as pd
from pathlib import Path

expected_dtype: dict[int: str] = {0: "str", 1: "float", 2: "str"}
yw = 9.81

def read_properties(properties_file_path: Path) -> tuple[np.ndarray]:
	data = pd.read_csv(properties_file_path, dtype=expected_dtype)
	_properties = data.iloc[:, 0].values
	_values = data.iloc[:, 1].values

	properties = np.zeros(10, dtype=str)
	values = np.zeros(10, dtype=float)

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
	values[8] = (values[4]/values[7] * yw)/1e3

	# initial void rate
	properties[9] = 'eo'
	values[9] = values[2]*yw/values[8] * (1+values[3]) - 1

	return properties, values

def save_properties_data(properties_path: Path, export_path: Path) -> None:
	for file_path in properties_path.iterdir():
		probe = file_path.stem.split('_')[-1]
		properties, values = read_properties(file_path)
		np.savez(export_path/probe/"properties.npz", properties=properties, values=values)