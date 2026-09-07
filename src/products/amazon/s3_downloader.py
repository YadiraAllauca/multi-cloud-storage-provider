from typing import Optional
from src.interfaces.file_downloader import IFileDownloader
from src.utils.logger import get_logger
from src.utils.cloud_uri import validate_cloud_uri
from src.exceptions import InvalidPathError, StorageOperationError


class S3Downloader(IFileDownloader):
    """Mock S3 downloader: validates inputs and logs. It does NOT talk to AWS.

    No destination directory is created and no file is written, so a caller is
    never left with an empty directory tree that looks like a real download.
    """

    def __init__(
        self,
        aws_access_key: Optional[str] = None,
        aws_secret_key: Optional[str] = None,
        region: Optional[str] = None,
    ):
        self._logger = get_logger(self.__class__.__name__)
        self._aws_access_key = aws_access_key
        self._aws_secret_key = aws_secret_key
        self._region = region or "us-east-1"

    def download(self, source: str, destination: str) -> bool:
        try:
            bucket, object_key = validate_cloud_uri(source, "s3")

            if not destination:
                raise InvalidPathError("Destination path must not be empty")

            self._logger.info(
                f"Downloading '{object_key}' from S3 bucket '{bucket}' to {destination}"
            )
            self._logger.warning(f"S3Downloader is a mock: {destination} was NOT written.")
            return True

        except StorageOperationError:
            raise
        except Exception as e:
            self._logger.error(f"Failed to download {source} to {destination}: {str(e)}")
            raise StorageOperationError(f"Download failed: {str(e)}") from e
