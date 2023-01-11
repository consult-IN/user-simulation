import abc
from pathlib import Path

from src.setup_logger import logger


class ICRUD(metaclass=abc.ABCMeta):
    """
    Abstract class which defines the interface for classes offering CRUD functionality.

    Args:
        metaclass (abc.ABCMeta, optional): _description_. Defaults to abc.ABCMeta.
    """

    ALLOWED_EXTENSIONS: list[str] = []
    registered_paths: list[Path] = []

    def __init__(self, allowed_extensions: list[str]):
        """(Constructor)

        Args:
            allowed_extensions (list[str]): list of extensions that can be handled by this class
        """
        self.ALLOWED_EXTENSIONS = allowed_extensions

    @abc.abstractmethod
    def create(self, path_to_create: str) -> Path:
        """Create a path

        Args:
            path_to_create (str): path to be created

        Raises:
            NotImplementedError: Must be implemented by inheriting subclass

        Returns:
            Path: path which has been created
        """
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, path_to_read: str) -> str:
        """Read the content of the path

        Args:
            path_to_read (str): path to read

        Raises:
            NotImplementedError: Must be implemented by inheriting subclass

        Returns:
            str: path which has been read
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, path_to_update: str, content_to_append) -> Path:
        """Update the path

        Args:
            path_to_update (str): path to be updated
            content_to_append (undefinded): content which should update the path

        Raises:
            NotImplementedError: Must be implemented by inheriting subclass

        Returns:
            Path: path which has been updated
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, path_to_delete: str) -> Path:
        """Delete the path

        Args:
            path_to_delete (str): path to be deleted

        Raises:
            NotImplementedError: Must be implemented by inheriting subclass

        Returns:
            Path: Path which has been deleted
        """
        raise NotImplementedError

    def register_path(self, path: Path) -> None:
        """
        Adds the path to the instance variable 'registered_paths' to keep track of the
        paths that were touched by the operation.

        Args:
            path (Path): path that was used
        """
        if path not in self.registered_paths:
            self.registered_paths.append(path)
            logger.info(f"Path registered: {path}")

    def check_extension(self, path: Path) -> bool:
        """Check if the extension of given 'path' can be handled by this class.

        Args:
            path (Path): path to check

        Returns:
            bool: can this class handle the extension
        """
        if path.suffix in self.ALLOWED_EXTENSIONS:
            return True

        return False
