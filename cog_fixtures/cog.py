import abc
from dataclasses import dataclass
from typing import Dict, Optional, Sequence, Union

import affine
import rasterio
from rasterio.transform import from_origin
from pathlib import Path
from rasterio.crs import CRS
from rasterio.io import MemoryFile
from rio_cogeo.cogeo import cog_translate

from fake_geo_images.fakegeoimages import FakeGeoImage

@dataclass
class ImageBase(abc.ABC):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abc.abstractmethod
    def __post_init__(self):
        ...

    @abc.abstractmethod
    def close(self):
        ...


@dataclass
class FakeImage(ImageBase):
    driver: str
    width: int
    height: int
    count: int
    dtype: str
    crs: CRS
    nodata: float = 0.0
    transform: Optional[affine.Affine] = from_origin(1470996, 6914001, 2.0, 2.0)

    def __post_init__(self):
        fpath, _ = FakeGeoImage(
            xsize=self.width,
            ysize=self.height,
            num_bands=self.count,
            data_type=self.dtype,
            out_dir=Path(f"/vsimem"),
            crs=self.crs.to_epsg(),
            nodata=self.nodata
        ).create(transform=self.transform)
        self.handle = rasterio.open(fpath)

    def close(self):
        self.handle.close()


@dataclass
class FakeCog(ImageBase):
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
        self.handle.close()
        self.memfile.close()