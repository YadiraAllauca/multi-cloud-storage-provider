from src.interfaces.storage_factory import IStorageFactory
from src.interfaces.file_uploader import IFileUploader
from src.interfaces.file_downloader import IFileDownloader


class ServiceRunner:
    def __init__(self, storage_factory: IStorageFactory):
        self._uploader: IFileUploader = storage_factory.create_uploader()
        self._downloader: IFileDownloader = storage_factory.create_downloader()

    def upload_file(self, file_path: str, destination: str) -> bool:
        return self._uploader.upload(file_path, destination)

    def download_file(self, source: str, destination: str) -> bool:
        return self._downloader.download(source, destination)

