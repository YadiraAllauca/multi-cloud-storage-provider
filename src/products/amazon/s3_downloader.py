from pathlib import Path
from src.interfaces.file_downloader import IFileDownloader
from src.utils.logger import get_logger
from src.exceptions import FileNotFoundError, InvalidPathError, StorageOperationError


class S3Downloader(IFileDownloader):
    def __init__(self, aws_access_key: str = None, aws_secret_key: str = None, region: str = None):
        self._logger = get_logger(self.__class__.__name__)
        self._aws_access_key = aws_access_key
        self._aws_secret_key = aws_secret_key
        self._region = region or "us-east-1"

    def download(self, source: str, destination: str) -> bool:
        try:
            if not source.startswith("s3://"):
                raise InvalidPathError(f"Invalid S3 source format: {source}")

            dest_path = Path(destination)
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            self._logger.info(f"Downloading {source} from S3 to {destination}")
            self._logger.warning("S3Downloader is a mock implementation. Real S3 integration requires boto3.")
            return True

        except (FileNotFoundError, InvalidPathError):
            raise
        except Exception as e:
            self._logger.error(f"Failed to download {source} to {destination}: {str(e)}")
            raise StorageOperationError(f"Download failed: {str(e)}") from e

