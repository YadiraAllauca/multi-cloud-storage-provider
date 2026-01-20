from src.interfaces.storage_factory import IStorageFactory
from src.interfaces.file_uploader import IFileUploader
from src.interfaces.file_downloader import IFileDownloader
from src.products.local.disk_uploader import DiskUploader
from src.products.local.disk_downloader import DiskDownloader


class LocalDiskStorageFactory(IStorageFactory):
    def create_uploader(self) -> IFileUploader:
        return DiskUploader()

    def create_downloader(self) -> IFileDownloader:
        return DiskDownloader()

