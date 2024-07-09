import pandas as pd
import numpy as np

def samples_data(file_name: str) -> dict:
	samples = dict()
	split = [item.replace(" ", "") for item in file_name.split(".")]
	split = iter(split)
	
	for i in range(1, 5):
		item = next(split)
		samples[i] = dict()
		item = next(split)
		samples[i]["nombre"] = item
		item = next(split)
		samples[i]["carga"] = item

	print(samples)

	return samples

def load_file(file_name: str) -> None:
	data = pd.read_csv(filepath_or_buffer = file_name, names = ["time", "read", "units", "ID"], sep = ",", header = None)
	data.drop(columns = "units", axis = 1, inplace = True)
	
	for i in range(1, 5):
		tmp_data = data[data["ID"] == i]
		tmp_data.reset_index(inplace = True, drop = True)
		nrows = tmp_data.shape[0]
		tmp_data.iloc[:, 0] = np.arange(1, nrows+1)

		print(tmp_data)