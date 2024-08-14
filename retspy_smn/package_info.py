class PackageInfo:
    """Información del paquete."""

    name: str = "retspy-smn"

    version: str = "1.0.1"

    license: str = "MIT"

    description: str = "Indexador de imágenes de radar del SMN"

    long_description: str = "README.md"

    long_description_content_type: str = "text/markdown"

    package_data: dict[str, list[str]] = {
        "retspy_smn": ["retspy_smn/settings.json"]
    }

    include_package_data: bool = True

    author: str = "Waldemar Villamayor-Venialbo"

    author_email: str = "wvenialbo@fpuna.edu.py"

    url: str = "https://github.com/wvenialbo/RETSpy_smn"

    keywords: list[str] = [
        "meteorology",
        "severe weather",
        "doppler radar",
        "SMN",
        "SINARAME",
        "RETSpy",
    ]

    classifiers: list[str] = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ]

    entry_points: dict[str, list[str]] = {
        "console_scripts": ["retspy-smn=retspy_smn.__main__:main"]
    }


pkg_info = PackageInfo
