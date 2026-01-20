import pytest
import tempfile
from pathlib import Path
from src.products.local.disk_uploader import DiskUploader
from src.exceptions import FileNotFoundError, InvalidPathError


class TestDiskUploader:
    def test_upload_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source_file = Path(tmpdir) / "test.txt"
            source_file.write_text("test content")
            
            dest_file = Path(tmpdir) / "uploaded" / "test.txt"
            uploader = DiskUploader()
            
            result = uploader.upload(str(source_file), str(dest_file))
            
            assert result is True
            assert dest_file.exists()
            assert dest_file.read_text() == "test content"

    def test_upload_file_not_found(self):
        uploader = DiskUploader()
        
        with pytest.raises(FileNotFoundError):
            uploader.upload("/nonexistent/file.txt", "/tmp/dest.txt")

    def test_upload_invalid_source_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "directory"
            source_dir.mkdir()
            
            uploader = DiskUploader()
            
            with pytest.raises(InvalidPathError):
                uploader.upload(str(source_dir), "/tmp/dest.txt")

