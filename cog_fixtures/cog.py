"""cog_fixtures.cog module"""
import abc
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Sequence, Union

import affine
import rasterio
from fake_geo_images.fakegeoimages import FakeGeoImage
from rasterio.crs import CRS
from rasterio.io import MemoryFile
from rasterio.transform import from_origin
from rio_cogeo.cogeo import cog_translate


@dataclass  # type: ignore
class ImageBase(abc.ABC):
    """base image class"""

    def __enter__(self):
        """support context management"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """support context management"""
        self.close()

    @abc.abstractmethod
    def __post_init__(self):
        """post init hook"""
        ...

    @abc.abstractmethod
    def close(self):
        """close resources"""
        ...


@dataclass
class FakeImage(ImageBase):
    """fake rasterio image"""

    driver: str
    width: int
    height: int
    count: int
    dtype: str
    crs: CRS
    nodata: float = 0.0
    transform: Optional[affine.Affine] = from_origin(1470996, 6914001, 2.0, 2.0)

    def __post_init__(self):
        """post init hook"""
        fpath, _ = FakeGeoImage(
            xsize=self.width,
            ysize=self.height,
            num_bands=self.count,
            data_type=self.dtype,
            out_dir=Path("/vsimem"),
            crs=self.crs.to_epsg(),
            nodata=self.nodata,
        ).create(transform=self.transform)
        self.handle = rasterio.open(fpath)

    def close(self):
        """close resources"""
        self.handle.close()


@dataclass
class FakeCog(ImageBase):
    """fake cloud optimized geotiff"""

    src_img: FakeImage
    dst_kwargs: Dict
    indexes: Optional[Sequence[int]] = None
    nodata: Optional[Union[str, int, float]] = None
    dtype: Optional[str] = None
    add_mask: bool = False
    overview_level: Optional[int] = None
    overview_resampling: str = "nearest"
    web_optimized: bool = False
    latitude_adjustment: bool = True
    resampling: str = "nearest"
    config: Optional[Dict] = None
    allow_intermediate_compression: bool = False
    forward_band_tags: bool = False
    quiet: bool = False
    temporary_compression: str = "DEFLATE"

    def __post_init__(self):
        """post init hook"""
        self.memfile = MemoryFile()
        cog_translate(
            source=self.src_img.handle,
            dst_path=self.memfile.name,
            dst_kwargs=self.dst_kwargs,
            indexes=self.indexes,
            nodata=self.nodata,
            dtype=self.dtype,
            add_mask=self.add_mask,
            overview_level=self.overview_level,
            overview_resampling=self.overview_resampling,
            web_optimized=self.web_optimized,
            latitude_adjustment=self.latitude_adjustment,
            resampling=self.resampling,
            in_memory=True,  # TODO: This could be saved to disk
            config=self.config,
            allow_intermediate_compression=self.allow_intermediate_compression,
            forward_band_tags=self.forward_band_tags,
            quiet=self.quiet,
            temporary_compression=self.temporary_compression,
        )
        self.handle = self.memfile.open()

    def close(self):
        """close resources"""
        self.handle.close()
        self.memfile.close()
