from src.exceptions import InvalidPathError


def validate_cloud_uri(uri: str, scheme: str) -> tuple[str, str]:
    """Validate a `<scheme>://bucket/object` URI and return (bucket, object_key).

    Raises InvalidPathError if the scheme is wrong, the bucket is missing, or
    the object key is empty. A prefix check alone is not enough: `s3://` and
    `s3://bucket` are not addressable objects.
    """
    prefix = f"{scheme}://"
    if not uri.startswith(prefix):
        raise InvalidPathError(f"Invalid {scheme.upper()} path format: {uri}")

    remainder = uri[len(prefix):]
    bucket, separator, object_key = remainder.partition("/")
    if not bucket or not separator or not object_key:
        raise InvalidPathError(
            f"Invalid {scheme.upper()} path format, expected {prefix}bucket/object: {uri}"
        )

    return bucket, object_key
