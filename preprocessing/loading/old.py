import pandas as pd
import numpy as np
from pathlib import Path

expected_dtype: dict[int: str] = {0: "int", 1: "float", 2: "str", 3: "int"}

def read_file(file_path: Path, container: dict[str: dict], probes: list[str], loads: list[float]) -> None:
	n_probes = len(probes)
	data = pd.read_csv(file_path, header = None, dtype = expected_dtype)

	for idx in range(n_probes):
		probe_data = data[data.iloc[:, 3] == (idx+1)].values
		probe_data = probe_data[:, 0:2]
		probe_data[:, 0] = np.arange(start = 1, stop = probe_data.shape[0]+1)
		
		container[probes[idx]][loads[idx]] = probe_data

def read_folder(input_path: Path, probes: list[str]) -> dict[str: dict]:
	container = dict.fromkeys(probes, dict())

	for file_path in input_path.iterdir():
		file_name = file_path.stem
		loads = [str(name_section.split('_')[-1]) for name_section in file_name.split('-')] # Por si son diferentes (no deberia pero aja ...)
		read_file(file_path, container, probes, loads)

	return container

def save_loading_data(input_path: Path, export_path: Path, probes: list[str]) -> None:
	loading_data = read_folder(input_path, probes)
	for probe in loading_data.keys():
		np.savez(export_path/probe/"loading.npz", **loading_data[probe])