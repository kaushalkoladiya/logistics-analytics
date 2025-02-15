from pathlib import Path


def get_data_file_path(file_name: str) -> Path:
    return Path(__file__).resolve().parent.parent.parent / file_name
