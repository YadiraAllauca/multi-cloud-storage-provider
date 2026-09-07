import pytest

from src.exceptions import StorageFileNotFoundError, InvalidPathError, StorageOperationError
from src.products.local import DiskUploader


class TestExceptionHierarchy:
    def test_storage_errors_share_a_common_base(self):
        assert issubclass(StorageFileNotFoundError, StorageOperationError)
        assert issubclass(InvalidPathError, StorageOperationError)

    def test_storage_file_not_found_does_not_shadow_the_builtin(self):
        """Importing our exceptions must leave `FileNotFoundError` untouched.

        An earlier version named this class `FileNotFoundError`, so any module
        importing from `src.exceptions` silently replaced the builtin and
        `except FileNotFoundError` caught the wrong thing depending on imports.
        """
        assert StorageFileNotFoundError is not FileNotFoundError
        assert not issubclass(StorageFileNotFoundError, OSError)

    def test_missing_source_does_not_raise_the_builtin(self):
        uploader = DiskUploader()

        with pytest.raises(StorageFileNotFoundError):
            uploader.upload("/nonexistent/file.txt", "/tmp/dest.txt")

        with pytest.raises(StorageOperationError):
            uploader.upload("/nonexistent/file.txt", "/tmp/dest.txt")
