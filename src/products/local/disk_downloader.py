import shutil
from pathlib import Path
from src.interfaces.file_downloader import IFileDownloader
from src.utils.logger import get_logger
from src.exceptions import StorageFileNotFoundError, InvalidPathError, StorageOperationError


class DiskDownloader(IFileDownloader):
    """Real implementation: copies a file on the local filesystem."""

    def __init__(self):
        self._logger = get_logger(self.__class__.__name__)

    def download(self, source: str, destination: str) -> bool:
        try:
            source_path = Path(source)
            if not source_path.exists():
                raise StorageFileNotFoundError(f"Source file not found: {source}")
            if not source_path.is_file():
                raise InvalidPathError(f"Source path is not a file: {source}")

            dest_path = Path(destination)
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                shutil.copy2(source_path, dest_path)
            except shutil.SameFileError as e:
                raise InvalidPathError(
                    f"Source and destination are the same file: {source}"
                ) from e

            self._logger.info(f"Successfully copied {source} to {destination}")
            return True

        except StorageOperationError:
            raise
        except Exception as e:
            self._logger.error(f"Failed to download {source} to {destination}: {str(e)}")
            raise StorageOperationError(f"Download failed: {str(e)}") from e
