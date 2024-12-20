import numpy as np
import pandas as pd
from pathlib import Path

expected_dtype: dict[int: str] = {0: "str", 1: "float", 2: "str"}
y_w = 9.81


def read_properties(properties_path: Path, probes: list[str]) -> tuple[np.ndarray]:
	for file_path in properties_path.iterdir():
		data = pd.read_csv(file_path, dtype=expected_dtype)
		_properties = data.iloc[:, 0].values
		_values = data.iloc[:, 1].values

		properties = np.zeros(10, dtype=str)
		values = np.zeros(10, dtype=float)

		print(properties)
		add_properties = np.array(['A', 'V', 'yt', 'eo'])

	return properties, values


def save_properties_data(input_path: Path, export_path: Path, probes: list[str]) -> None:
	properties_data = read_properties(input_path, probes)
	# for probe in properties_data.keys(): 
		# np.save(export_path/probe/"properties.npy", properties_data[probe])