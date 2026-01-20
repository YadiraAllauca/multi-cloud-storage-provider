import os
from src.interfaces.storage_factory import IStorageFactory
from src.interfaces.file_uploader import IFileUploader
from src.interfaces.file_downloader import IFileDownloader
from src.products.google.gcs_uploader import GCSUploader
from src.products.google.gcs_downloader import GCSDownloader


class GoogleStorageFactory(IStorageFactory):
    def __init__(self, project_id: str = None, credentials_path: str = None):
        self._project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self._credentials_path = credentials_path or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    def create_uploader(self) -> IFileUploader:
        return GCSUploader(self._project_id, self._credentials_path)

    def create_downloader(self) -> IFileDownloader:
        return GCSDownloader(self._project_id, self._credentials_path)

