import pytest
from src.factories import GoogleStorageFactory
from src.products.google.gcs_uploader import GCSUploader
from src.products.google.gcs_downloader import GCSDownloader


class TestGoogleStorageFactory:
    def test_create_uploader(self):
        factory = GoogleStorageFactory()
        uploader = factory.create_uploader()
        
        assert isinstance(uploader, GCSUploader)

    def test_create_downloader(self):
        factory = GoogleStorageFactory()
        downloader = factory.create_downloader()
        
        assert isinstance(downloader, GCSDownloader)

    def test_create_uploader_with_credentials(self):
        factory = GoogleStorageFactory(
            project_id="test-project",
            credentials_path="/path/to/credentials.json"
        )
        uploader = factory.create_uploader()
        
        assert isinstance(uploader, GCSUploader)
        assert uploader._project_id == "test-project"
        assert uploader._credentials_path == "/path/to/credentials.json"

