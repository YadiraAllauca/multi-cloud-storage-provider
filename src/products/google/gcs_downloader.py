from typing import Optional
from src.interfaces.file_downloader import IFileDownloader
from src.utils.logger import get_logger
from src.utils.cloud_uri import validate_cloud_uri
from src.exceptions import InvalidPathError, StorageOperationError


class GCSDownloader(IFileDownloader):
    """Mock GCS downloader: validates inputs and logs. It does NOT talk to Google Cloud.

    No destination directory is created and no file is written, so a caller is
    never left with an empty directory tree that looks like a real download.
    """

    def __init__(self, project_id: Optional[str] = None, credentials_path: Optional[str] = None):
        self._logger = get_logger(self.__class__.__name__)
        self._project_id = project_id
        self._credentials_path = credentials_path

    def download(self, source: str, destination: str) -> bool:
        try:
            bucket, object_key = validate_cloud_uri(source, "gs")

            if not destination:
                raise InvalidPathError("Destination path must not be empty")

            self._logger.info(
                f"Downloading '{object_key}' from GCS bucket '{bucket}' to {destination}"
            )
            self._logger.warning(f"GCSDownloader is a mock: {destination} was NOT written.")
            return True

        except StorageOperationError:
            raise
        except Exception as e:
            self._logger.error(f"Failed to download {source} to {destination}: {str(e)}")
            raise StorageOperationError(f"Download failed: {str(e)}") from e
