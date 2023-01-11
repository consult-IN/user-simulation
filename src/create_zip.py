from pathlib import Path
from zipfile import ZipFile


def create_zip(path_to_zip: str, path_of_zip: str) -> str:
    """
    Creates a zip-archive from a path that should be part of it and returns a
    name of the resulting zip-archive.

    Args:
        path_to_zip (str): Path which gets zipped (can be dir or file)
        path_of_zip (str): Path of the resulting zip-archive that will be created.

    Returns:
        str: the path of the resulting zip-archive
    """
    files_to_zip = get_files_in_path(Path(path_to_zip))
    with ZipFile(Path(path_of_zip), "w") as zip_arch:
        for file_path in files_to_zip:
            zip_arch.write(file_path)
    return path_of_zip


def get_files_in_path(path_to_zip: Path) -> list[Path]:
    """
    Determine the paths to include inside of a zip-archive as a path can be a file or a directory.

    Args:
        path_to_zip (Path): The path which should be zipped.

    Raises:
        Exception: On non-existance of the path_to_zip inside the filesystem

    Returns:
        list[Path]: Paths inside the directory given in path_to_zip
    """
    files_in_path = []
    if not path_to_zip.exists():
        raise Exception(f"Path does not exist {path_to_zip}")
    if path_to_zip.is_file():
        files_in_path.append(path_to_zip)
    elif path_to_zip.is_dir():
        files_in_path.extend(list(path_to_zip.iterdir()))

    return files_in_path
