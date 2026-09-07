import pytest
import tempfile
from pathlib import Path
from src.products.local.disk_downloader import DiskDownloader
from src.exceptions import StorageFileNotFoundError, InvalidPathError


class TestDiskDownloader:
    def test_download_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source_file = Path(tmpdir) / "test.txt"
            source_file.write_text("test content")
            
            dest_file = Path(tmpdir) / "downloaded" / "test.txt"
            downloader = DiskDownloader()
            
            result = downloader.download(str(source_file), str(dest_file))
            
            assert result is True
            assert dest_file.exists()
            assert dest_file.read_text() == "test content"

    def test_download_file_not_found(self):
        downloader = DiskDownloader()
        
        with pytest.raises(StorageFileNotFoundError):
            downloader.download("/nonexistent/file.txt", "/tmp/dest.txt")

    def test_download_invalid_source_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "directory"
            source_dir.mkdir()
            
            downloader = DiskDownloader()
            
            with pytest.raises(InvalidPathError):
                downloader.download(str(source_dir), "/tmp/dest.txt")


    def test_download_to_same_path_raises_invalid_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source_file = Path(tmpdir) / "test.txt"
            source_file.write_text("test content")

            downloader = DiskDownloader()

            with pytest.raises(InvalidPathError):
                downloader.download(str(source_file), str(source_file))

            assert source_file.read_text() == "test content"
