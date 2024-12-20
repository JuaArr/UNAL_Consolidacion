import numpy as np
from pathlib import Path
from utils.handling_folders import create_folder
from preprocessing.loading import old, pinzuar
from preprocessing.properties import save_properties_data
import preprocessing.unloading

def pp_data(loading_path: Path, 
			properties_path: Path, 
			unloading_path: Path, 
			export_path: Path, 
			is_pinzuar: bool = False
			) -> None:
	
	if is_pinzuar:
		pass
	else:
		_file_path = next(loading_path.glob("*.txt"))
		probes = [_name_section.split('_')[-2] for _name_section in _file_path.stem.split('-')]
		for probe in probes: create_folder(export_path / probe)		
		
		old.save_loading_data(loading_path, export_path, probes)
		save_properties_data(properties_path, export_path, probes)