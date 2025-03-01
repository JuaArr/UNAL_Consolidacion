import numpy as np
from pathlib import Path
from tabulate import tabulate

def create_folder(folder_path: Path) -> None:
	if not folder_path.exists():
		folder_path.mkdir()

def save_table(file_path: Path, table: dict, fmt: str | tuple[str]) -> None:
	printed_table = tabulate(tabular_data=table, 
							 headers='keys', 
							 tablefmt='simple',
							 numalign='left',
							 floatfmt=fmt)

	with open(file_path, 'w') as f:
		print(printed_table, file=f)

def ceil_multiple(x: np.float64, m: np.float64) -> np.float64:
	return m * np.ceil(x/m)

def floor_multiple(x: np.float64, m: np.float64) -> np.float64:
	return m * np.floor(x/m)