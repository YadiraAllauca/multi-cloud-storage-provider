class StorageOperationError(Exception):
    pass


class FileNotFoundError(StorageOperationError):
    pass


class InvalidPathError(StorageOperationError):
    pass

