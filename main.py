import tempfile
from pathlib import Path
from src.factories import AmazonStorageFactory, LocalDiskStorageFactory, GoogleStorageFactory
from src.client import ServiceRunner
from src.exceptions import StorageOperationError


def main():
    print("=== Multi-Cloud Storage Provider Demo ===\n")
    
    print("1. Testing Amazon S3 Storage (Mock)")
    factory = AmazonStorageFactory()
    service = ServiceRunner(factory)
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp.write("Test content for S3")
            tmp_path = tmp.name
        
        service.upload_file(tmp_path, "s3://bucket/test.txt")
        service.download_file("s3://bucket/test.txt", "local_test.txt")
        Path(tmp_path).unlink()
    except StorageOperationError as e:
        print(f"Error: {e}")
    
    print("\n2. Testing Local Disk Storage (Real Implementation)")
    factory = LocalDiskStorageFactory()
    service = ServiceRunner(factory)
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_file = Path(tmpdir) / "test.txt"
            source_file.write_text("Test content for local storage")
            
            dest_upload = Path(tmpdir) / "uploaded" / "test.txt"
            dest_download = Path(tmpdir) / "downloaded" / "test.txt"
            
            service.upload_file(str(source_file), str(dest_upload))
            service.download_file(str(dest_upload), str(dest_download))
            
            print(f"✓ Upload successful: {dest_upload.exists()}")
            print(f"✓ Download successful: {dest_download.exists()}")
    except StorageOperationError as e:
        print(f"Error: {e}")
    
    print("\n3. Testing Google Cloud Storage (Mock)")
    factory = GoogleStorageFactory()
    service = ServiceRunner(factory)
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp.write("Test content for GCS")
            tmp_path = tmp.name
        
        service.upload_file(tmp_path, "gs://bucket/test.txt")
        service.download_file("gs://bucket/test.txt", "local_gcs_test.txt")
        Path(tmp_path).unlink()
    except StorageOperationError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

