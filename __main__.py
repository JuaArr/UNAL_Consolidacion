import os

from read_format import read_old

def main() -> None:
	lecturas_dir = "./lecturas/"
	filtro_dir = lecturas_dir + "filtro/"

	for item in os.listdir(lecturas_dir):
		item_path = os.path.join(lecturas_dir, item)
		if os.path.isfile(item_path):
			samples = read_old.samples_data(item_path)
			read_old.load_file(item_path, samples, filtro_dir)

if __name__ == "__main__":
	main() 