from ..application_info import ApplicationInfo as BaseApplicationInfo


class ApplicationInfo(BaseApplicationInfo):
    """Información de la aplicación."""

    command: str = "init"

    help: str = (
        "Inicializa el directorio de trabajo. Crea una copia del "
        "archivo de configuración con los valores por defecto en "
        "la carpeta de trabajo. El usuario puede modificar los "
        "valores de configuración según sus necesidades."
    )

    version: str = "1.0.1"


app_info = ApplicationInfo
