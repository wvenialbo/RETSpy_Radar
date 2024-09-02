from .package_info import NAT_NAME, RAW_NAME, pkg_info


class ApplicationInfo:
    """Información de la aplicación."""

    alias: str = NAT_NAME

    banner: str = f"{alias} - {pkg_info.description}"

    copyright: str = "Copyright (C) 2024 El equipo de desarrollo de RETSpy"

    header: str = "Indexador de imágenes y mosaicos de radar"

    help: str = (
        "Esta aplicación permite descargar imágenes de radar de las "
        "estaciones del Sistema Nacional de Radares Meteorológicos "
        "(SINARAME) del Servicio Meteorológico Nacional (SMN) de "
        "Argentina y del Sistema de Tecnologia e Monitoramento "
        "Ambiental do Paraná (SIMEPAR) de Brasil."
    )

    title: str = f"{banner} ({pkg_info.version})"

    default_settings: str = pkg_info.package_data[RAW_NAME][0]

    user_settings: str = "settings.user.json"

    version: str = pkg_info.version


app_info = ApplicationInfo
