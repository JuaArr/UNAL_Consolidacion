from pathlib import Path

def create_folder(folder_path: Path) -> None:
	if not folder_path.exists():
		folder_path.mkdir()