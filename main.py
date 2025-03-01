import os
import numpy as np
from pathlib import Path
import oedometer as oedo

from matplotlib import pyplot as plt

results_dir = Path("./test/old1")
loading_dir = results_dir / "loading_data"
properties_dir = results_dir / "properties"
unloading_dir = results_dir / "unloading_data"
export_dir = Path("./export")

test_dir = export_dir/'S3M24'

def main() -> None:

	oedo.pp_data(loading_dir, properties_dir, unloading_dir, export_dir)

	for test_dir in export_dir.iterdir():

		properties_data: dict = np.load(test_dir/'properties.npy', allow_pickle=True).item()
		loading_data: dict = np.load(test_dir/'loading.npy', allow_pickle=True).item()
		unloading_data: dict = np.load(test_dir/'unloading.npy', allow_pickle=True).item()

		n_preloading_stages = 1
		n_loading_stages = len(loading_data.get('loads'))
		n_unloading_stages = len(unloading_data.get('loads'))
		stages = [n_preloading_stages, n_loading_stages, n_unloading_stages]

		loads, heights = oedo.consolidate_stages(loading_data=loading_data, unloading_data=unloading_data, stages=stages)
		stress = oedo.calculate_stress(loads=loads, properties=properties_data)
		strain = oedo.calculate_strain(heights=heights, properties=properties_data)
		void_ratio = oedo.calculate_void_ratio(strain=strain, properties=properties_data)
		work = oedo.calculate_strain_energy(stress=stress, strain=strain)

		compressibility_params = oedo.calculate_compressibility_params(stress=stress, void_ratio=void_ratio, stages=stages, save_metrics=True, export_dir=test_dir)
		strain_energy_params = oedo.calculate_strain_energy_params(stress=stress, work=work, save_metrics=True, export_dir=test_dir)

		oedo.init_plot(lnewdth=1.2, page_lnewdth_cm=15, mrksze=4)
		
		oedo.save_compressibility(stress, void_ratio, compressibility_params, export_dir=test_dir)
		oedo.save_strain_energy(stress, work, strain_energy_params, export_dir=test_dir)

	# Depurar datos de descarga ...
	# Revisar a cuanto tiempo corresponde cada toma de datos ... 
	# Cargar datos de descarga (dentro de un .txt)
	# Juntar carga y descarga
	# Generar tablas asociadas
	# Graficar

if __name__ == '__main__':
	os.system("cls")
	main() 