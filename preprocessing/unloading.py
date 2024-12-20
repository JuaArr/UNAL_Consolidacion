import numpy as np
import pandas as pd
from pathlib import Path

expected_dtype: dict[int: str] = {0: "float", 1: "str", 2: "float", 3: "str"}

def read_unloading(unloading_file_path: Path) -> tuple[np.ndarray]:
	data = pd.read_csv(unloading_file_path, dtype=expected_dtype)
	load = data.iloc[:, 0].values
	values = data.iloc[:, 2].values

	return load, values

def save_unloading_data(unloading_path: Path, export_path: Path) -> None:
	for file_path in unloading_path.iterdir():
		probe = file_path.stem.split('_')[-1]
		load, values = read_unloading(file_path)
		np.savez(export_path/probe/"unloading.npz", load=load, values=values)