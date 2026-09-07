import pytest
import tempfile
from pathlib import Path

from src.products.amazon import S3Uploader, S3Downloader
from src.products.google import GCSUploader, GCSDownloader
from src.exceptions import StorageFileNotFoundError, InvalidPathError


@pytest.fixture
def sample_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test.txt"
        path.write_text("test content")
        yield path


UPLOADERS = [
    (S3Uploader, "s3://bucket/test.txt", "gs://bucket/test.txt"),
    (GCSUploader, "gs://bucket/test.txt", "s3://bucket/test.txt"),
]

DOWNLOADERS = [
    (S3Downloader, "s3://bucket/test.txt", "gs://bucket/test.txt"),
    (GCSDownloader, "gs://bucket/test.txt", "s3://bucket/test.txt"),
]


class TestMockUploaders:
    @pytest.mark.parametrize("uploader_cls,valid_uri,_", UPLOADERS)
    def test_upload_returns_true_for_valid_uri(self, uploader_cls, valid_uri, _, sample_file):
        assert uploader_cls().upload(str(sample_file), valid_uri) is True

    @pytest.mark.parametrize("uploader_cls,_,wrong_scheme_uri", UPLOADERS)
    def test_upload_rejects_wrong_scheme(self, uploader_cls, _, wrong_scheme_uri, sample_file):
        with pytest.raises(InvalidPathError):
            uploader_cls().upload(str(sample_file), wrong_scheme_uri)

    @pytest.mark.parametrize("uploader_cls,valid_uri,_", UPLOADERS)
    def test_upload_rejects_missing_source(self, uploader_cls, valid_uri, _):
        with pytest.raises(StorageFileNotFoundError):
            uploader_cls().upload("/nonexistent/file.txt", valid_uri)

    @pytest.mark.parametrize("uploader_cls,valid_uri,_", UPLOADERS)
    def test_upload_rejects_directory_as_source(self, uploader_cls, valid_uri, _, sample_file):
        with pytest.raises(InvalidPathError):
            uploader_cls().upload(str(sample_file.parent), valid_uri)

    @pytest.mark.parametrize("uploader_cls,valid_uri,_", UPLOADERS)
    def test_upload_rejects_uri_without_object_key(self, uploader_cls, valid_uri, _, sample_file):
        scheme = valid_uri.split("://")[0]
        for bad_uri in (f"{scheme}://", f"{scheme}://bucket", f"{scheme}://bucket/"):
            with pytest.raises(InvalidPathError):
                uploader_cls().upload(str(sample_file), bad_uri)


class TestMockDownloaders:
    @pytest.mark.parametrize("downloader_cls,valid_uri,_", DOWNLOADERS)
    def test_download_returns_true_for_valid_uri(self, downloader_cls, valid_uri, _):
        assert downloader_cls().download(valid_uri, "dest.txt") is True

    @pytest.mark.parametrize("downloader_cls,_,wrong_scheme_uri", DOWNLOADERS)
    def test_download_rejects_wrong_scheme(self, downloader_cls, _, wrong_scheme_uri):
        with pytest.raises(InvalidPathError):
            downloader_cls().download(wrong_scheme_uri, "dest.txt")

    @pytest.mark.parametrize("downloader_cls,valid_uri,_", DOWNLOADERS)
    def test_download_rejects_empty_destination(self, downloader_cls, valid_uri, _):
        with pytest.raises(InvalidPathError):
            downloader_cls().download(valid_uri, "")

    @pytest.mark.parametrize("downloader_cls,valid_uri,_", DOWNLOADERS)
    def test_download_does_not_touch_the_filesystem(self, downloader_cls, valid_uri, _):
        """A mock download must not leave directories that look like a real one."""
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "nested" / "dir" / "test.txt"

            assert downloader_cls().download(valid_uri, str(destination)) is True

            assert not destination.exists()
            assert not destination.parent.exists()
