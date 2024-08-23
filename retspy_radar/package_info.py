from typing import LiteralString

PRJ_NAME: LiteralString = "RETSpy"
NAT_NAME: LiteralString = f"{PRJ_NAME} Radar"
GIT_NAME: LiteralString = NAT_NAME.replace(" ", "_")
RAW_NAME: LiteralString = GIT_NAME.lower()
PKG_NAME: LiteralString = RAW_NAME.replace("_", "-")


class PackageInfo:
    """Información del paquete."""

    name: str = PKG_NAME

    version: str = "1.0.1"

    license: str = "MIT"

    description: str = "Indexador de imágenes de radares meteorológicos"

    long_description: str = "README.md"

    long_description_content_type: str = "text/markdown"

    package_data: dict[str, list[str]] = {RAW_NAME: ["settings.json"]}

    include_package_data: bool = True

    author: str = "Waldemar Villamayor-Venialbo"

    author_email: str = "wvenialbo@fpuna.edu.py"

    url: str = f"https://github.com/wvenialbo/{GIT_NAME}"

    keywords: list[str] = [
        "doppler radar images",
        "weather radar",
        "severe weather",
        "multi-source",
        "weather data",
        "meteorology",
        "atmospheric science",
        "weather service",
        "SMN",
        "SINARAME",
        "SIMEPAR",
        PRJ_NAME,
    ]

    classifiers: list[str] = [
        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Flake8",
        "Framework :: MkDocs",
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Extension",
        "Framework :: Sphinx :: Theme",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Natural Language :: Spanish",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Utilities",
    ]

    entry_points: dict[str, list[str]] = {
        "console_scripts": [f"{PKG_NAME}={RAW_NAME}.__main__:main"]
    }


pkg_info = PackageInfo
