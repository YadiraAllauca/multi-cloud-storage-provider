import os
from src.interfaces.storage_factory import IStorageFactory
from src.interfaces.file_uploader import IFileUploader
from src.interfaces.file_downloader import IFileDownloader
from src.products.amazon.s3_uploader import S3Uploader
from src.products.amazon.s3_downloader import S3Downloader


class AmazonStorageFactory(IStorageFactory):
    def __init__(self, aws_access_key: str = None, aws_secret_key: str = None, region: str = None):
        self._aws_access_key = aws_access_key or os.getenv("AWS_ACCESS_KEY_ID")
        self._aws_secret_key = aws_secret_key or os.getenv("AWS_SECRET_ACCESS_KEY")
        self._region = region or os.getenv("AWS_REGION", "us-east-1")

    def create_uploader(self) -> IFileUploader:
        return S3Uploader(self._aws_access_key, self._aws_secret_key, self._region)

    def create_downloader(self) -> IFileDownloader:
        return S3Downloader(self._aws_access_key, self._aws_secret_key, self._region)

