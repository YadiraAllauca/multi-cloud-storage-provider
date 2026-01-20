import os
import shutil
from pathlib import Path
from src.interfaces.file_uploader import IFileUploader
from src.utils.logger import get_logger
from src.exceptions import FileNotFoundError, InvalidPathError, StorageOperationError


class DiskUploader(IFileUploader):
    def __init__(self):
        self._logger = get_logger(self.__class__.__name__)

    def upload(self, file_path: str, destination: str) -> bool:
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                raise FileNotFoundError(f"Source file not found: {file_path}")
            if not source_path.is_file():
                raise InvalidPathError(f"Source path is not a file: {file_path}")

            dest_path = Path(destination)
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(source_path, dest_path)
            self._logger.info(f"Successfully copied {file_path} to {destination}")
            return True

        except (FileNotFoundError, InvalidPathError):
            raise
        except Exception as e:
            self._logger.error(f"Failed to upload {file_path} to {destination}: {str(e)}")
            raise StorageOperationError(f"Upload failed: {str(e)}") from e

