"""Setup for rio-tiler."""

from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

# Runtime requirements.
inst_reqs = [
    "rasterio>=1.1.7",
    "rio-cogeo==2.*",
    "fake-geo-images==0.1.0",
]

extra_reqs = {
    "test": ["pytest", "pytest-cov"],
    "dev": ["pytest", "pytest-cov", "pre-commit"],
}

setup(
    name="cog-fixtures",
    version="0.1.0",  # tbd
    python_requires=">=3.6",
    description="cog fixtures",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="COG cogeo raster map tiles gdal rasterio",
    author="cogeotiff",
    author_email="cogeotiff@gmail.com",
    url="https://github.com/cogeotiff/cog-fixtures",
    license="BSD",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)
