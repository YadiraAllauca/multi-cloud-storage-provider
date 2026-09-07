# Multi-Cloud Storage Provider

[![CI](https://github.com/YadiraAllauca/multi-cloud-storage-provider/actions/workflows/ci.yml/badge.svg)](https://github.com/YadiraAllauca/multi-cloud-storage-provider/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An educational implementation of the **Abstract Factory** pattern, using file storage as the
example domain.

**This is not a usable storage library.** Only the local-disk provider performs real I/O
(`shutil.copy2`). The S3 and GCS providers are **mocks**: they validate the path format, log what
they *would* do, and return `True`. No bytes ever reach AWS or Google Cloud, and no SDK
(`boto3`, `google-cloud-storage`) is installed or imported. The name describes the *shape* of the
design, not its capability.

Read it for the pattern and the trade-off discussion below, not to move files to the cloud.

## Limitations

- **S3 and GCS are mocks.** `S3Uploader`, `S3Downloader`, `GCSUploader` and `GCSDownloader`
  validate their inputs and log. They do not transfer data.
- **Credentials are accepted and stored, but never used.** `AmazonStorageFactory` reads
  `AWS_ACCESS_KEY_ID` and friends, and passes them to the products, where they sit in an unused
  attribute. They exist to show where configuration would enter the design.
- **Mock downloads write nothing.** They do not create the destination directory either, so you
  are never left with an empty tree that looks like a successful download.
- **No retries, no timeouts, no streaming, no multipart, no concurrency, no progress reporting.**
  Real cloud clients need all of these.
- **Local disk only copies files.** No directories, no symlink policy, no permission handling
  beyond whatever `shutil.copy2` does.
- **Coverage is high but the tested surface is small.** The tests cover the local implementation
  end to end, and the mocks' validation rules. There is no integration test against real storage,
  because there is nothing real to integrate with.

## Why Abstract Factory here — and when it would be overengineering

This is the part worth arguing about, so I'll argue against my own code first.

Abstract Factory earns its keep when **a family of products must be created together and mixing
families is a bug**. That condition is genuinely met here: uploading to S3 and downloading from
local disk in the same `ServiceRunner` would be nonsense, and the factory makes that combination
impossible to express.

But look at the cost. To guarantee "uploader and downloader come from the same provider", this
repo defines **3 interfaces + 3 factories + 6 products = 12 types**. And an interface with a
single method, implemented by a class with no state of its own, is a strong hint that the
abstraction isn't paying rent.

A single interface gets the same guarantee for a third of the classes:

```python
class IStorage(ABC):
    @abstractmethod
    def upload(self, file_path: str, destination: str) -> bool: ...

    @abstractmethod
    def download(self, source: str, destination: str) -> bool: ...


class DiskStorage(IStorage): ...
class S3Storage(IStorage): ...
class GCSStorage(IStorage): ...

# The client takes the dependency directly. No factory, no create_* indirection.
service = ServiceRunner(S3Storage(region="us-west-2"))
```

Mixing providers is now impossible **by construction** rather than by convention, because there is
only one object. That is a stronger guarantee than the factory gives, with 3 classes instead of 12.

**So when would the factory actually be the right call?**

- **The family grows.** Two products is not a family, it's a pair. Add `IObjectLister`,
  `ISignedUrlGenerator`, `IMultipartUploader`, `ILifecyclePolicyManager` and a single `IStorage`
  becomes a ten-method interface that violates Interface Segregation. Then a factory that hands
  out focused, provider-consistent products is clearly better.
- **Products have different lifecycles or construction costs.** Here both products are stateless
  and take identical constructor arguments, so there is nothing for the factory to *decide*. If a
  downloader needed a connection pool and an uploader needed a multipart session, the factory
  would be encapsulating real construction logic instead of forwarding arguments.
- **The provider is chosen at runtime from configuration and registered by third parties.** A
  plugin registry mapping `"s3" -> S3Factory()` is the classic case; the client must not know the
  concrete types at all.
- **Consumers need only one half of the pair.** A read-only service wanting a downloader without
  dragging in upload capability is a real Interface Segregation argument for splitting the products.

**Verdict:** at this scope, `IStorage` injected directly is what I would ship. The factory is here
because the exercise is about the pattern, and because the structure is worth being able to
recognise — but "the pattern applies" and "the pattern pays for itself" are different questions,
and this repo is on the wrong side of the second one. Keeping the note is more honest than quietly
presenting 12 classes as the obvious design.

## Pattern mapping

| Role | Type |
| --- | --- |
| Abstract Factory | `IStorageFactory` |
| Concrete Factories | `AmazonStorageFactory`, `GoogleStorageFactory`, `LocalDiskStorageFactory` |
| Abstract Products | `IFileUploader`, `IFileDownloader` |
| Concrete Products | `S3Uploader`/`S3Downloader`, `GCSUploader`/`GCSDownloader`, `DiskUploader`/`DiskDownloader` |
| Client | `ServiceRunner` |

`ServiceRunner` depends only on the interfaces, so swapping providers is a one-line change at the
composition point.

## Project structure

```
multi-cloud-storage-provider/
├── src/
│   ├── interfaces/                 # Abstract factory + abstract products
│   │   ├── storage_factory.py
│   │   ├── file_uploader.py
│   │   └── file_downloader.py
│   ├── products/                   # Concrete products
│   │   ├── amazon/                 # mock
│   │   │   ├── s3_uploader.py
│   │   │   └── s3_downloader.py
│   │   ├── google/                 # mock
│   │   │   ├── gcs_uploader.py
│   │   │   └── gcs_downloader.py
│   │   └── local/                  # real file I/O
│   │       ├── disk_uploader.py
│   │       └── disk_downloader.py
│   ├── factories/                  # Concrete factories
│   │   ├── amazon_storage_factory.py
│   │   ├── google_storage_factory.py
│   │   └── local_disk_storage_factory.py
│   ├── client/
│   │   └── service_runner.py
│   ├── utils/
│   │   ├── logger.py
│   │   └── cloud_uri.py            # s3://bucket/key and gs://bucket/key validation
│   └── exceptions/
│       └── storage_exceptions.py
├── tests/
│   ├── test_disk_uploader.py
│   ├── test_disk_downloader.py
│   ├── test_cloud_mocks.py
│   ├── test_exceptions.py
│   ├── test_factories.py
│   ├── test_google_factory.py
│   └── test_service_runner.py
├── .github/workflows/ci.yml
├── LICENSE
├── main.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Requirements

- Python 3.9+
- pytest and pytest-cov (tests only; the library itself has no runtime dependencies)

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.factories import AmazonStorageFactory, GoogleStorageFactory, LocalDiskStorageFactory
from src.client import ServiceRunner

# Local disk — the only provider that actually moves bytes.
service = ServiceRunner(LocalDiskStorageFactory())
service.upload_file("test.txt", "/local/path/test.txt")
service.download_file("/local/path/test.txt", "downloaded_test.txt")

# Swapping the factory is the only change the client needs...
service = ServiceRunner(AmazonStorageFactory())
service.upload_file("test.txt", "s3://bucket/test.txt")   # validates and logs; uploads nothing

service = ServiceRunner(GoogleStorageFactory())
service.upload_file("test.txt", "gs://bucket/test.txt")   # validates and logs; uploads nothing
```

Run the demo:

```bash
python main.py
```

### Configuration (accepted, not used)

The cloud factories read credentials from environment variables or constructor arguments and hand
them to their products. **Nothing authenticates with them** — they are wiring for an integration
that does not exist yet. Set them only if you want to see where they would flow.

```python
factory = AmazonStorageFactory(aws_access_key="...", aws_secret_key="...", region="us-west-2")
# env: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

factory = GoogleStorageFactory(project_id="...", credentials_path="/path/to/credentials.json")
# env: GOOGLE_CLOUD_PROJECT, GOOGLE_APPLICATION_CREDENTIALS
```

### Errors

```
StorageOperationError            # base for everything below
├── StorageFileNotFoundError     # source file does not exist
└── InvalidPathError             # bad path format, or source is not a file
```

`StorageFileNotFoundError` is deliberately **not** named `FileNotFoundError`. An earlier version
was, which shadowed the Python builtin: any module importing from `src.exceptions` silently
rebound the name, and `except FileNotFoundError` then caught our exception or the operating
system's depending on import order. `tests/test_exceptions.py` guards against the regression.

## Testing

```bash
pytest                                        # runs with coverage, per pytest.ini
pytest --cov=src --cov-report=html            # HTML report in htmlcov/
```

What the tests actually cover:

- `DiskUploader` / `DiskDownloader`: real copies, missing sources, directories passed as files,
  and the same-file case.
- The S3 and GCS mocks: scheme validation, malformed URIs, missing sources, and the guarantee that
  a mock download leaves the filesystem untouched.
- All three factories produce the expected product types and forward configuration.
- `ServiceRunner` against local and mock factories, including error propagation.
- The exception hierarchy, including the builtin-shadowing regression test.

Coverage sits around 90% of `src/`, but read that number in context: two thirds of the products
are mocks, so high coverage here means "the validation and wiring are exercised", not "cloud
uploads work".

CI runs the suite on Python 3.9 through 3.13 on every push and pull request to `master`.

## Adding a provider

1. Implement `IFileUploader` and `IFileDownloader` under `src/products/<provider>/`.
2. Implement `IStorageFactory` under `src/factories/`.
3. Add tests.
4. `ServiceRunner(YourStorageFactory())` — the client does not change.

## License

MIT — see [LICENSE](LICENSE). Educational project; not intended for production use.
