from abc import ABC, abstractmethod


class IFileDownloader(ABC):
    @abstractmethod
    def download(self, source: str, destination: str) -> bool:
        pass

