from ..application_info import ApplicationInfo as BaseApplicationInfo


class ApplicationInfo(BaseApplicationInfo):
    """Información de la aplicación."""

    command: str = "simepar"

    header: str = "Indexador de mosaicos de radar del SIMEPAR"

    help: str = (
        "Descarga mosaicos de radar de las estaciones del Sistema de "
        "Tecnologia e Monitoramento Ambiental do Paraná (SIMEPAR) de "
        "Brasil."
    )

    version: str = "1.0.1"


app_info = ApplicationInfo
