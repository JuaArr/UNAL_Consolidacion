import os
from pathlib import Path
from read_data import read_old

results_dir = Path("./test/old1")
loading_dir = results_dir / "loading_data"
properties_dir = results_dir / "properties"
unloading_dir = results_dir / "unloading_data"
export_dir = Path("./export")

def main() -> None:
	data = read_old.read_folder(loading_dir)
	print(data.keys())

	# Revisar a cuanto tiempo corresponde cada toma de datos ... 
	# Cargar datos de descarga (dentro de un .txt)
	# Cargar datos de la muestra (dentro de un .txt)
	# Juntar carga y descarga
	# Generar tablas asociadas
	# Graficar

if __name__ == "__main__":
	os.system("cls")
	main() 