import pytest
from src.factories import AmazonStorageFactory, LocalDiskStorageFactory
from src.products.amazon.s3_uploader import S3Uploader
from src.products.amazon.s3_downloader import S3Downloader
from src.products.local.disk_uploader import DiskUploader
from src.products.local.disk_downloader import DiskDownloader


class TestAmazonStorageFactory:
    def test_create_uploader(self):
        factory = AmazonStorageFactory()
        uploader = factory.create_uploader()
        
        assert isinstance(uploader, S3Uploader)

    def test_create_downloader(self):
        factory = AmazonStorageFactory()
        downloader = factory.create_downloader()
        
        assert isinstance(downloader, S3Downloader)

    def test_create_uploader_with_credentials(self):
        factory = AmazonStorageFactory(
            aws_access_key="test_key",
            aws_secret_key="test_secret",
            region="us-west-2"
        )
        uploader = factory.create_uploader()
        
        assert isinstance(uploader, S3Uploader)
        assert uploader._aws_access_key == "test_key"
        assert uploader._aws_secret_key == "test_secret"
        assert uploader._region == "us-west-2"


class TestLocalDiskStorageFactory:
    def test_create_uploader(self):
        factory = LocalDiskStorageFactory()
        uploader = factory.create_uploader()
        
        assert isinstance(uploader, DiskUploader)

    def test_create_downloader(self):
        factory = LocalDiskStorageFactory()
        downloader = factory.create_downloader()
        
        assert isinstance(downloader, DiskDownloader)

