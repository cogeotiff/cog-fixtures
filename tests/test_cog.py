from rasterio.crs import CRS
from rio_cogeo.cogeo import cog_info
from rio_cogeo.profiles import JPEGProfile

from cog_fixtures import FakeCog, FakeImage


def test_fake_image():
    img = FakeImage(
        driver="GTiff",
        width=512,
        height=512,
        count=3,
        dtype="uint8",
        crs=CRS.from_epsg(3857),
    )
    profile = img.handle.profile
    assert profile["width"] == 512
    assert profile["height"] == 512
    assert profile["count"] == 3
    assert profile["dtype"] == "uint8"
    assert profile["crs"] == CRS.from_epsg(3857)

    img.close()
    assert img.handle.closed


def test_fake_cog():
    img = FakeImage(
        driver="GTiff",
        width=512,
        height=512,
        count=3,
        dtype="uint8",
        crs=CRS.from_epsg(3857),
    )
    cog = FakeCog(src_img=img, dst_kwargs=JPEGProfile(),)

    info = cog_info(cog.handle.name)
    assert info["COG"]
    assert info["Compression"] == "JPEG"

    img.close()
    cog.close()


def test_with_context():
    with FakeImage(
        driver="GTiff",
        width=100,
        height=100,
        count=3,
        dtype="int16",
        crs=CRS.from_epsg(4326),
    ) as img:
        ...

    assert img.handle.closed
