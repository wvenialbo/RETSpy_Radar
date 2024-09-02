from ..application_info import ApplicationInfo as BaseApplicationInfo


class ApplicationInfo(BaseApplicationInfo):
    """Información de la aplicación."""

    command: str = "sinarame"

    header: str = "Indexador de imágenes y mosaicos de radar del SINARAME"

    help: str = (
        "Descarga imágenes y mosaicos de radar de las estaciones del "
        "Sistema Nacional de Radares Meteorológicos (SINARAME) "
        "administrado por el Servicio Meteorológico Nacional argentino "
        "(SMN)."
    )

    version: str = "1.0.1"


app_info = ApplicationInfo
