import os
import sys
from pathlib import Path

from src.crud.i_crud import ICRUD
from src.setup_logger import logger

sys.dont_write_bytecode = True


class CRUDFolders(ICRUD):
    """
    Providing functionality to execute the CRUD operations on folders.
    Limited by the 'NOT_ALLOWED_FOLDERNAME_ELEMENTS'. Tracks the paths that
    this class has interacted with.
    """

    def __init__(self, not_allowed_foldername_elements: list[str]) -> None:
        super().__init__(allowed_extensions=[""])
        self.NOT_ALLOWED_FOLDERNAME_ELEMENTS = not_allowed_foldername_elements

    def create(self, path_to_create: str) -> Path:
        """
        Creates a folder on the path that is given via the parameters.

        Args:
            path_to_create (str): path to folder to be created

        Returns:
            Path: the path of the created or already existing folder
        """
        folder_path = Path(path_to_create)
        if not self.check_foldername_elements(path_to_create):
            raise Exception(
                f"Some elements in your foldername cannot be handled by this instance: {folder_path}"
            )
        if folder_path.exists():
            logger.info(f"Folder already exists: {folder_path}")
        else:
            try:
                os.mkdir(folder_path)
            except Exception as error:  # probably to general
                logger.error(f"Could not create folder: {str(error)}")
        return folder_path

    def delete(self, path_to_delete: str) -> Path:
        """
        Deletes a folder.

        Args:
            path_to_delete (str): path to the folder to be deleted

        Returns:
            Path: the deleted folder path
        """
        folder_path = Path(path_to_delete)
        if not self.check_foldername_elements(folder_path):
            logger.debug(
                f"deletion possible although some elements of path not in allowed extension: {path_to_delete}"
            )

        if folder_path.exists():
            try:
                os.rmdir(folder_path)
            except PermissionError as error:  # probably no permission in this path
                logger.error(f"Could not delete folder: {str(error)}")
        else:
            logger.debug(f"Folder does not exist: {folder_path}")
        logger.debug(f"CRUDFolder instance deleted path: {folder_path}")
        return folder_path

    def update(self, path_to_update: str, content_to_append) -> Path:
        pass

    def read(self, path_to_read: str) -> str:
        pass

    def check_foldername_elements(self, folder_path: Path) -> bool:
        """Check if the foldername of given 'folder_path' can be handled by this class.

        Args:
            folder_path (Path): path to check

        Returns:
            bool: can this class handle the extension
        """
        args = os.path.split(folder_path)
        for element in self.NOT_ALLOWED_FOLDERNAME_ELEMENTS:
            if element in args[-1]:
                return False
        return True


if __name__ == "__main__":
    test_folder: str = "./test/test_data/hello"
    inacceptable_characters_in_path: list[str] = [
        " ",
        ":",
        "?",
        "*",
        '"',
        "|",
        "<",
        ">",
    ]
    crud_folders: CRUDFolders = CRUDFolders(inacceptable_characters_in_path)
    crud_folders.create(test_folder)
    input("\n>>> Press [ENTER] to continue\n")

    deleted_path = crud_folders.delete(test_folder)
    input("\n>>> Press [ENTER] to continue\n")

    logger.info("Done Demonstrating! \n")
