import pandas as pd
import numpy as np
from pathlib import Path

expected_dtype: dict[int: str] = {0: "int", 1: "float", 2: "str", 3: "int"}

def read_file(file_path: Path, probes: list[str], n_probes: int) -> np.ndarray:
	container = dict.fromkeys(probes)
	data = pd.read_csv(file_path, header = None, dtype = expected_dtype)

	for idx in range(n_probes):
		probe_data = data[data.iloc[:, 3] == (idx+1)].values
		probe_data = probe_data[:, 0:2]
		probe_data[:, 0] = np.arange(start = 1, stop = probe_data.shape[0]+1)
		
		container[probes[idx]] = probe_data
	
	return container

def read_folder(folder_path: Path) -> None:
	
	_file_path = next(folder_path.glob("*.txt"))
	_data =  pd.read_csv(_file_path, header = None, dtype = expected_dtype)

	n_probes = len(_data.iloc[:, 3].drop_duplicates().values)
	probes = [i.split("_")[-2] for i in _file_path.stem.split("-")]

	for file_path in folder_path.iterdir():

		# print(file_path.stem.split("-"))
		read_file(file_path, probes, n_probes)
# def samples_data(file_name: str) -> dict:
# 	samples = dict()
# 	file_name = os.path.splitext(file_name)[0]
# 	split = file_name.split("_")
# 	split = iter(split)
	
# 	for i in range(1, 5):
# 		item = next(split)
# 		samples[i] = dict()
# 		item = next(split)
# 		samples[i]["Nombre"] = item.split("-")[-1]
# 		item = next(split)
# 		samples[i]["Carga"] = item.split("KG")[0]

# 	return samples

# def load_file(file_path: str, samples: dict[str: str], filtro_dir: str) -> None:
# 	data = pd.read_csv(file_path, names = ["Tiempo", "Lectura", "Unidades", "ID"], sep = ",", header = None)
# 	data.drop(columns = "Unidades", axis = 1, inplace = True)
	
# 	for i in range(1, 5):
# 		tmp_data = data[data["ID"] == i]
# 		tmp_data.reset_index(inplace = True, drop = True)
# 		nrows = tmp_data.shape[0]
# 		tmp_data.iloc[:, 0] = np.arange(1, nrows+1)

# 		tmp_file_path = os.path.join(filtro_dir, samples[i]["Nombre"]+".xlsx")
# 		sheet_name = samples[i]["Carga"]

# 		if os.path.exists(tmp_file_path):
# 			with pd.ExcelWriter(tmp_file_path, engine='openpyxl', mode='a') as writer:
# 				try:
# 					if sheet_name not in writer.book.sheetnames:
# 						tmp_data.to_excel(writer, sheet_name=sheet_name, index=False)
# 				except Exception as e:
# 					print(f"Failed to append data: {e}")
# 		else:
# 			with pd.ExcelWriter(tmp_file_path, engine='openpyxl') as writer:
# 				tmp_data.to_excel(writer, sheet_name=sheet_name, index=False)