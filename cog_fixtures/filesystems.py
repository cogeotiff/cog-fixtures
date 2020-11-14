"""filesystems"""
import abc
from dataclasses import dataclass
from typing import Any, ClassVar
from urllib.parse import urlsplit

import boto3

from cog_fixtures.cog import ImageBase


@dataclass  # type: ignore
class Filesystem(abc.ABC):
    """base filesystem"""

    @classmethod
    def from_path(cls, path) -> "Filesystem":
        """return a filesystem based on the path"""
        if path.startswith("s3://"):
            return S3Filesystem()
        else:
            return LocalFilesystem()

    @abc.abstractmethod
    def save(self, img: ImageBase, path: str):
        """save an image to a location"""
        ...


@dataclass
class S3Filesystem(Filesystem):
    """s3 filesystem"""

    s3_client: ClassVar[Any] = boto3.client("s3")

    def save(self, img: ImageBase, path: str):
        """save an image to S3, accepts a S3 URI"""
        splits = urlsplit(path)
        assert splits.scheme == "s3"
        self.s3_client.upload_fileobj(img.memfile, splits.netloc, splits.path[1:])  # type: ignore


@dataclass
class LocalFilesystem(Filesystem):
    """local filesystem"""

    def save(self, img: ImageBase, path: str):
        """save an image to local filesystem"""
        with open(path, "wb") as outf:
            outf.write(img.memfile.read())  # type: ignore
