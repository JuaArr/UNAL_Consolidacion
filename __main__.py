import os
import numpy as np
from rich import print
from utils.templates import error_template
from pathlib import Path
from preprocessing import pp_data

results_dir = Path("./test/old1")
loading_dir = results_dir / "loading_data"
properties_dir = results_dir / "properties"
unloading_dir = results_dir / "unloading_data"
export_dir = Path("./export")

def main() -> None:
	pp_data(loading_dir, properties_dir, unloading_dir, export_dir)

	# A = np.load(export_dir/"S2M45"/"loading.npz", allow_pickle=True)
	# B = np.load(export_dir/"S2M45"/"properties.npy", allow_pickle=True)
	# print(list(A.keys()))
	# print(sorted(list(A.keys()), key = float))

	# loading_data = old.read_folder(loading_dir)
	# properties_data = read_properties(properties_dir, export_dir)
	
	# Depurar datos de descarga ...
	# Revisar a cuanto tiempo corresponde cada toma de datos ... 
	# Cargar datos de descarga (dentro de un .txt)
	# Juntar carga y descarga
	# Generar tablas asociadas
	# Graficar

if __name__ == "__main__":
	os.system("cls")
	error_template()
	main() 