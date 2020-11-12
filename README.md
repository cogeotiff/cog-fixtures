# cog-fixtures
Suite of valid and invalid Cloud Optimized GeoTIFF for testing purposes

## Usage
The library can be used to create "fake" COGs for testing purposes.  Images are created in memory using GDAL's [`vsimem` filesystem](https://gdal.org/user/virtual_file_systems.html).

```python
from rio_cogeo.profiles import JPEGProfile
from rasterio.crs import CRS

from cog_fixtures.cog import FakeImage, FakeCog

# Create the source image
img = FakeImage(
    driver="GTiff",
    width=512,
    height=512,
    count=3,
    dtype="uint8",
    crs=CRS.from_epsg(3857)
)

# Convert to COG
cog = FakeCog(src_img=img, dst_kwargs=JPEGProfile(), quiet=True)
print(cog)


>>> FakeCog(src_img=FakeImage(driver='GTiff', width=512, height=512, count=3, dtype='uint8', crs=CRS.from_epsg(3857), nodata=0.0, transform=Affine(2.0, 0.0, 1470996.0,
       0.0, -2.0, 6914001.0)), dst_kwargs={'driver': 'GTiff', 'interleave': 'pixel', 'tiled': True, 'blockxsize': 512, 'blockysize': 512, 'compress': 'JPEG', 'photometric': 'YCbCr'}, indexes=None, nodata=None, dtype=None, add_mask=False, overview_level=None, overview_resampling='nearest', web_optimized=False, latitude_adjustment=True, resampling='nearest', config=None, allow_intermediate_compression=False, forward_band_tags=False, quiet=True, temporary_compression='DEFLATE')
```
