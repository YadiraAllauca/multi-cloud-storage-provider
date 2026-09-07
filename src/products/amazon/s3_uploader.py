from typing import Optional
from pathlib import Path
from src.interfaces.file_uploader import IFileUploader
from src.utils.logger import get_logger
from src.utils.cloud_uri import validate_cloud_uri
from src.exceptions import StorageFileNotFoundError, InvalidPathError, StorageOperationError


class S3Uploader(IFileUploader):
    """Mock S3 uploader: validates inputs and logs. It does NOT talk to AWS."""

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

    def upload(self, file_path: str, destination: str) -> bool:
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                raise StorageFileNotFoundError(f"Source file not found: {file_path}")
            if not source_path.is_file():
                raise InvalidPathError(f"Source path is not a file: {file_path}")

            bucket, object_key = validate_cloud_uri(destination, "s3")

            self._logger.info(f"Uploading {file_path} to S3 bucket '{bucket}' as '{object_key}'")
            self._logger.warning("S3Uploader is a mock: no bytes were sent to AWS.")
            return True

        except StorageOperationError:
            raise
        except Exception as e:
            self._logger.error(f"Failed to upload {file_path} to {destination}: {str(e)}")
            raise StorageOperationError(f"Upload failed: {str(e)}") from e
