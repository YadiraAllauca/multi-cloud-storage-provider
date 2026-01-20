# Multi-Cloud Storage Provider

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Code Style](https://img.shields.io/badge/code%20style-clean-blue.svg)

A clean, educational implementation demonstrating the **Abstract Factory Design Pattern** for managing multiple cloud storage providers. This is a simple project designed to showcase how the Abstract Factory pattern enables seamless switching between different storage implementations without modifying client code.

## Overview

This project demonstrates how to use the Abstract Factory pattern to create families of related objects (file uploaders and downloaders) without specifying their concrete classes. The client code (`ServiceRunner`) interacts only with abstract interfaces, allowing you to switch between storage providers (Amazon S3, Google Cloud Storage, Local Disk, or future providers) with a single line change.

## Design Pattern: Abstract Factory

The **Abstract Factory Pattern** provides an interface for creating families of related or dependent objects without specifying their concrete classes. In this project:

- **Abstract Factory**: `IStorageFactory` - Defines methods to create uploaders and downloaders
- **Concrete Factories**: `AmazonStorageFactory`, `LocalDiskStorageFactory`, `GoogleStorageFactory` - Create specific product families
- **Abstract Products**: `IFileUploader`, `IFileDownloader` - Define interfaces for product types
- **Concrete Products**: `S3Uploader`, `S3Downloader`, `DiskUploader`, `DiskDownloader`, `GCSUploader`, `GCSDownloader` - Implement specific behaviors

### Benefits

- **Flexibility**: Switch between storage providers without changing client code
- **Consistency**: Ensures related products (uploader/downloader) come from the same family
- **Maintainability**: Easy to add new storage providers by implementing the factory interface
- **Testability**: Easy to mock storage providers for testing

## Project Structure

```
multi-cloud-storage-provider/
├── src/
│   ├── interfaces/          # Abstract interfaces
│   │   ├── file_uploader.py
│   │   ├── file_downloader.py
│   │   └── storage_factory.py
│   ├── products/            # Concrete product implementations
│   │   ├── amazon/
│   │   │   ├── s3_uploader.py
│   │   │   └── s3_downloader.py
│   │   ├── amazon/
│   │   │   ├── s3_uploader.py
│   │   │   └── s3_downloader.py
│   │   ├── google/
│   │   │   ├── gcs_uploader.py
│   │   │   └── gcs_downloader.py
│   │   └── local/
│   │       ├── disk_uploader.py
│   │       └── disk_downloader.py
│   ├── factories/           # Concrete factory implementations
│   │   ├── amazon_storage_factory.py
│   │   ├── google_storage_factory.py
│   │   └── local_disk_storage_factory.py
│   ├── client/             # Client code
│   │   └── service_runner.py
│   ├── utils/              # Utility modules
│   │   └── logger.py
│   └── exceptions/          # Custom exceptions
│       └── storage_exceptions.py
├── tests/                  # Unit tests
│   ├── test_disk_uploader.py
│   ├── test_disk_downloader.py
│   ├── test_factories.py
│   ├── test_google_factory.py
│   └── test_service_runner.py
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD
├── main.py                 # Example usage
├── requirements.txt        # Python dependencies
├── pytest.ini             # Pytest configuration
└── README.md
```

## Requirements

- Python 3.7+
- pytest (for running tests)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from src.factories import AmazonStorageFactory, LocalDiskStorageFactory, GoogleStorageFactory
from src.client import ServiceRunner

# Use Amazon S3 storage
factory = AmazonStorageFactory()
service = ServiceRunner(factory)
service.upload_file("test.txt", "s3://bucket/test.txt")
service.download_file("s3://bucket/test.txt", "local_test.txt")

# Switch to Google Cloud Storage - only one line changes!
factory = GoogleStorageFactory()
service = ServiceRunner(factory)
service.upload_file("test.txt", "gs://bucket/test.txt")
service.download_file("gs://bucket/test.txt", "local_test.txt")

# Switch to local disk storage - only one line changes!
factory = LocalDiskStorageFactory()
service = ServiceRunner(factory)
service.upload_file("test.txt", "/local/path/test.txt")
service.download_file("/local/path/test.txt", "downloaded_test.txt")
```

### Running the Example

```bash
python main.py
```

### Configuration

#### Amazon S3 Storage

The `AmazonStorageFactory` supports configuration via environment variables:

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

Or pass credentials directly:

```python
factory = AmazonStorageFactory(
    aws_access_key="your-key",
    aws_secret_key="your-secret",
    region="us-west-2"
)
```

#### Google Cloud Storage

The `GoogleStorageFactory` supports configuration via environment variables:

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

Or pass credentials directly:

```python
factory = GoogleStorageFactory(
    project_id="your-project-id",
    credentials_path="/path/to/credentials.json"
)
```

### Error Handling

The project includes custom exceptions for better error handling:

- `StorageOperationError`: Base exception for storage operations
- `FileNotFoundError`: Raised when source file doesn't exist
- `InvalidPathError`: Raised when path format is invalid

All operations include proper error handling and logging.

### Logging

The project uses structured logging. All operations are logged with appropriate levels (INFO, WARNING, ERROR). Logs are output to stdout with timestamps and context.

## Testing

Run the test suite with pytest:

```bash
pytest
```

Run with verbose output and coverage report:

```bash
pytest -v --cov=src --cov-report=term-missing
```

Generate HTML coverage report:

```bash
pytest --cov=src --cov-report=html
```

The test suite includes:
- Unit tests for all uploaders and downloaders
- Factory pattern tests for all three providers
- Integration tests for ServiceRunner
- Error handling and edge case tests

### Test Coverage

- `DiskUploader` and `DiskDownloader` have full implementation with real file operations
- `S3Uploader` and `S3Downloader` are mock implementations (real S3 integration would require boto3)
- `GCSUploader` and `GCSDownloader` are mock implementations (real GCS integration would require google-cloud-storage)
- All factories are tested for correct product creation
- ServiceRunner is tested with all factory types

### Continuous Integration

This project includes GitHub Actions CI/CD workflow that:
- Runs tests on multiple Python versions (3.7, 3.8, 3.9, 3.10, 3.11)
- Generates coverage reports
- Ensures code quality across different Python versions

## Key Features

- **Interface-Based Design**: All interactions use abstract interfaces, not concrete classes
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed Principle**: Open for extension (new providers), closed for modification
- **Dependency Inversion**: High-level modules depend on abstractions, not concretions
- **Error Handling**: Comprehensive exception handling with custom exceptions
- **Logging**: Structured logging for all operations
- **Testing**: Full test coverage with pytest
- **Real Implementation**: Local disk operations use actual file system operations

## Adding a New Storage Provider

To add a new storage provider (e.g., Azure Blob Storage):

1. Create product implementations:
   - `src/products/azure/blob_uploader.py` (implements `IFileUploader`)
   - `src/products/azure/blob_downloader.py` (implements `IFileDownloader`)

2. Create factory implementation:
   - `src/factories/azure_storage_factory.py` (implements `IStorageFactory`)

3. Add tests:
   - `tests/test_azure_factory.py`

4. Use it in your code:
   ```python
   factory = AzureStorageFactory()
   service = ServiceRunner(factory)
   ```

The client code (`ServiceRunner`) requires no changes!

## Design Principles

This project follows **SOLID principles**:

- **S**ingle Responsibility: Each class has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: All implementations can be used interchangeably
- **I**nterface Segregation: Focused, specific interfaces
- **D**ependency Inversion: Depend on abstractions, not concretions

## Implementation Details

### Local Disk Storage

The `DiskUploader` and `DiskDownloader` implement real file operations:
- Validates file existence and paths
- Creates destination directories automatically
- Uses `shutil.copy2` to preserve file metadata
- Comprehensive error handling

### Amazon S3 Storage

The `S3Uploader` and `S3Downloader` are mock implementations that:
- Validate S3 path format (`s3://bucket/path`)
- Support credential configuration via environment variables or constructor
- Log operations (ready for boto3 integration)
- Follow the same interface as local implementations

### Google Cloud Storage

The `GCSUploader` and `GCSDownloader` are mock implementations that:
- Validate GCS path format (`gs://bucket/path`)
- Support credential configuration via environment variables or constructor
- Log operations (ready for google-cloud-storage integration)
- Follow the same interface as other implementations

## License

This is an educational project demonstrating design patterns.

