from read_format import read_old

def main() -> None:
	file_name = "1. KAMS-IMPAR_S2-M45-2.0KG_CAR. 2. KAMS-IPARM_S3-M24-2.0KG_CAR. 3. KAMS-IPARM_S3-M39-2.0KG_CAR. 4. KAMS-IPARM_S4-M4-2.0KG_CAR..TXT"
	samples = read_old.samples_data(file_name)

	# read_old.load_file(file_name)

if __name__ == "__main__":
	main()