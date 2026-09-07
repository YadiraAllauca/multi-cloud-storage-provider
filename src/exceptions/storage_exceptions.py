class StorageOperationError(Exception):
    pass


class StorageFileNotFoundError(StorageOperationError):
    pass


class InvalidPathError(StorageOperationError):
    pass
