import os
import misc.template
from pathlib import Path
from read_data.loading import old

results_dir = Path("./test/old1")
loading_dir = results_dir / "loading_data"
properties_dir = results_dir / "properties"
unloading_dir = results_dir / "unloading_data"
export_dir = Path("./export")

def main() -> None:
	loading_data = old.read_folder(loading_dir)
	p = properties_dir / "properties_S2M45.txt"
	itera = iter(p.read_text().split("\n"))
	print(next(itera))
	print(p)
	# loading_properties = 

	# Revisar a cuanto tiempo corresponde cada toma de datos ... 
	# Cargar datos de descarga (dentro de un .txt)
	# Cargar datos de la muestra (dentro de un .txt)
	# Juntar carga y descarga
	# Generar tablas asociadas
	# Graficar

if __name__ == "__main__":
	os.system("cls")
	main() 