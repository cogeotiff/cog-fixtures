import os

import boto3
from moto import mock_s3
from rasterio.crs import CRS
from rasterio.transform import from_origin
from rio_cogeo.cogeo import cog_info
from rio_cogeo.profiles import JPEGProfile

from cog_fixtures import FakeCog, FakeImage
from cog_fixtures.filesystems import LocalFilesystem, S3Filesystem


def _create_cog() -> FakeCog:
    img = FakeImage(
        driver="GTiff",
        width=512,
        height=512,
        count=3,
        dtype="uint8",
        crs=CRS.from_epsg(3857),
        transform=from_origin(1470996, 6914001, 2.0, 2.0),
    )
    return FakeCog(src_img=img, dst_kwargs=JPEGProfile(),)


def test_local_filesystem():
    fs = LocalFilesystem()
    cog = _create_cog()
    fs.save(cog, path="/tmp/test-cog.tif")

    info = cog_info("/tmp/test-cog.tif")
    assert info["COG"]

    os.remove("/tmp/test-cog.tif")


@mock_s3
def test_s3_filesystem():
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="bucket")

    fs = S3Filesystem()
    fs.s3_client = boto3.client("s3")
    cog = _create_cog()
    fs.save(cog, path="s3://bucket/test-cog.tif")

    resp = fs.s3_client.head_object(Bucket="bucket", Key="test-cog.tif")
    assert resp["ResponseMetadata"]["HTTPStatusCode"] == 200
