from abc import ABC, abstractmethod
from .file_uploader import IFileUploader
from .file_downloader import IFileDownloader


class IStorageFactory(ABC):
    @abstractmethod
    def create_uploader(self) -> IFileUploader:
        pass

    @abstractmethod
    def create_downloader(self) -> IFileDownloader:
        pass

