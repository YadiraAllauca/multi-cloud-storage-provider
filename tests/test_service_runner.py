import pytest
import tempfile
from pathlib import Path
from src.factories import LocalDiskStorageFactory, AmazonStorageFactory
from src.client import ServiceRunner
from src.exceptions import FileNotFoundError


class TestServiceRunner:
    def test_upload_file_with_local_factory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source_file = Path(tmpdir) / "test.txt"
            source_file.write_text("test content")
            
            dest_file = Path(tmpdir) / "uploaded" / "test.txt"
            factory = LocalDiskStorageFactory()
            service = ServiceRunner(factory)
            
            result = service.upload_file(str(source_file), str(dest_file))
            
            assert result is True
            assert dest_file.exists()

    def test_download_file_with_local_factory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source_file = Path(tmpdir) / "test.txt"
            source_file.write_text("test content")
            
            dest_file = Path(tmpdir) / "downloaded" / "test.txt"
            factory = LocalDiskStorageFactory()
            service = ServiceRunner(factory)
            
            result = service.download_file(str(source_file), str(dest_file))
            
            assert result is True
            assert dest_file.exists()

    def test_upload_file_with_amazon_factory(self):
        factory = AmazonStorageFactory()
        service = ServiceRunner(factory)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            source_file = Path(tmpdir) / "test.txt"
            source_file.write_text("test content")
            
            result = service.upload_file(str(source_file), "s3://bucket/test.txt")
            assert result is True

    def test_service_runner_raises_exception_on_invalid_file(self):
        factory = LocalDiskStorageFactory()
        service = ServiceRunner(factory)
        
        with pytest.raises(FileNotFoundError):
            service.upload_file("/nonexistent/file.txt", "/tmp/dest.txt")

