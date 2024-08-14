from pathlib import Path

from setuptools import find_namespace_packages, setup

from retspy_smn.package_info import pkg_info

this_directory: Path = Path(__file__).parent

long_description: str = pkg_info.long_description

pkg_info.long_description = (this_directory / long_description).read_text()

EXCLUDE: tuple[str, ...] = (
    "build",
    "dist",
    "docs",
    "examples",
    "scripts",
    "tests",
    "tutorial",
)

setup(packages=find_namespace_packages(exclude=EXCLUDE), **vars(pkg_info()))

pkg_info.long_description = long_description
