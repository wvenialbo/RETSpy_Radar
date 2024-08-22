from ..package_info import pkg_info


class ApplicationInfo:
    """Información de la aplicación."""

    alias: str = "RETSpy-SMN"

    banner: str = f"{alias} - {pkg_info.description}"
    
    copyright: str = "Copyright (C) 2024 El equipo de desarrollo de RETSPy"

    detail: str = (
        "Indexador de imágenes y mosaicos de radar del Servicio "
        "Meteorológico Nacional argentino (SMN): Esta aplicación "
        "permite descargar imágenes de radar de las estaciones del "
        "Sistema Nacional de Radares Meteorológicos (SINARAME) "
        "administrado por el SMN."
    )

    title: str = f"{banner} ({pkg_info.version})"

    settings_model: str = "sinarame"

    default_settings: str = "settings.json"

    user_settings: str = "settings.smn.json"


app_info = ApplicationInfo
