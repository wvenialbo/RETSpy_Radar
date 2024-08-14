from pathlib import Path
from typing import Any

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

args: dict[str, Any] = {
    k: v
    for k, v in pkg_info.__dict__.items()
    if not (k.startswith("__") and k.endswith("__"))
}

setup(packages=find_namespace_packages(exclude=EXCLUDE), **args)

pkg_info.long_description = long_description
