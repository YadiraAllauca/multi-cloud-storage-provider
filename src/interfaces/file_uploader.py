from abc import ABC, abstractmethod


class IFileUploader(ABC):
    @abstractmethod
    def upload(self, file_path: str, destination: str) -> bool:
        pass

