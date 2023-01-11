import os
from pathlib import Path

from src.crud.i_crud import ICRUD
from src.setup_logger import logger


class CRUDFiles(ICRUD):
    """
    Providing functionality to execute the CRUD operations on files.
    Limited by the 'ALLOWED_EXTENSIONS'. Tracks the paths that this class has interacted with.
    """

    def __init__(self, allowed_extensions: list[str]):
        super().__init__(allowed_extensions=allowed_extensions)

    def create(self, path_to_create: str) -> Path:
        """
        Creates a file on the path that is given via the parameters.

        Args:
            path_to_create (str): path of the file to be created

        Raises:
            Exception: On extension that is unprocessable by this class

        Returns:
            Path: the path of the created or already existing file
        """
        file_path = Path(path_to_create)
        if not self.check_extension(file_path):
            raise Exception(
                f"Extension of path cannot be handled by this instance: {file_path}"
            )

        if file_path.exists():
            logger.info(f"Path already exists: {file_path}")
        else:
            with open(file_path, "w", encoding="utf-8"):
                pass

        self.register_path(file_path)
        logger.debug(f"CRUDFiles instance created path:{file_path}")
        return file_path

    def read(self, path_to_read: str) -> str:
        """Reads the content of a file.

        Args:
            path_to_read (str): path to the file with the content to be read

        Raises:
            Exception: On extension that is unprocessable by this class

        Returns:
            str: content of the file
        """
        file_path = Path(path_to_read)
        if not self.check_extension(file_path):
            raise Exception(
                f"Extension of path cannot be handled by this instance: {file_path}"
            )

        with open(file_path, "r", encoding="utf-8") as file_handle:
            self.register_path(file_path)
            return file_handle.readlines()

    def update(self, path_to_update: str, content_to_append: list[str]) -> Path:
        """
        Update file with specified content

        Args:
            path_to_update (str): path to the file to update
            content_to_append (list[str]): content to append

        Raises:
            Exception: On extension that is unprocessable by this class

        Returns:
            Path: path of updated file
        """
        file_path = Path(path_to_update)
        if not self.check_extension(file_path):
            raise Exception(
                f"Extension of path cannot be handled by this instance: {file_path}"
            )
        with open(file_path, "a", encoding="utf-8") as file_handle:
            self.register_path(file_path)
            file_handle.writelines(content_to_append)
        logger.debug(
            f"CRUDFiles instance update path: {file_path} with content:\n{content_to_append}\n"
        )
        return file_path

    def delete(self, path_to_delete: str) -> Path:
        """
        Deletes a file.

        Args:
            path_to_delete (str): path to the file to be deleted

        Returns:
            Path: the deleted file path
        """
        file_path = Path(path_to_delete)
        if not self.check_extension(file_path):
            logger.debug(
                f"deletion possible although extension of path not in allowed extension: {file_path}"
            )

        if file_path.exists():
            os.remove(file_path)
        else:
            logger.debug(f"File not available: {file_path}")
        self.register_path(file_path)
        logger.debug(f"CRUDFiles instance deleted path: {file_path}")
        return file_path

    def __del__(self):
        self.registered_paths = []


if __name__ == "__main__":
    test_file: str = r"test\test_data\test.txt"
    test_content: list[str] = ["Hello World!"]

    crud_files: CRUDFiles = CRUDFiles(allowed_extensions=[".txt"])
    crud_files.create(test_file)
    input("\n>>> Press [ENTER] to continue\n")

    crud_files.update(test_file, test_content)
    input("\n>>> Press [ENTER] to continue\n")

    logger.info(f"Content of file is: {crud_files.read(test_file)}")
    input("\n>>> Press [ENTER] to continue\n")

    deleted_path = crud_files.delete(test_file)
    input("\n>>> Press [ENTER] to continue\n")

    logger.info("Done Demonstrating! \n")
