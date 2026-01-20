from pathlib import Path
from src.interfaces.file_uploader import IFileUploader
from src.utils.logger import get_logger
from src.exceptions import FileNotFoundError, InvalidPathError, StorageOperationError


class GCSUploader(IFileUploader):
    def __init__(self, project_id: str = None, credentials_path: str = None):
        self._logger = get_logger(self.__class__.__name__)
        self._project_id = project_id
        self._credentials_path = credentials_path

    def upload(self, file_path: str, destination: str) -> bool:
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                raise FileNotFoundError(f"Source file not found: {file_path}")
            if not source_path.is_file():
                raise InvalidPathError(f"Source path is not a file: {file_path}")

            if not destination.startswith("gs://"):
                raise InvalidPathError(f"Invalid GCS destination format: {destination}")

            self._logger.info(f"Uploading {file_path} to GCS: {destination}")
            self._logger.warning("GCSUploader is a mock implementation. Real GCS integration requires google-cloud-storage.")
            return True

        except (FileNotFoundError, InvalidPathError):
            raise
        except Exception as e:
            self._logger.error(f"Failed to upload {file_path} to {destination}: {str(e)}")
            raise StorageOperationError(f"Upload failed: {str(e)}") from e

