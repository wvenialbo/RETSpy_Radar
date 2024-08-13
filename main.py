"""
Este script es el punto de entrada del Robot de descarga de imágenes y
mosaicos de radar del Sistema Nacional de Radares Meteorológicos
(SINARAME) del Servicio Meteorológico Nacional (SMN) argentino.

Si no se proveen argumentos, se utilizarán los valores por defecto. Para
más información, ejecute el script con la opción -h o --help.
"""

from .base.exceptions import (
    InvalidConfigurationFileError,
    UninitializedOutputDirError,
    UninitializedWorkspaceError,
)
from .sinarame import Application, ApplicationInfo, Bootstrap
from .sinarame import SettingsSMN as Settings
from .sinarame import Startup


def main() -> None:
    """
    Punto de entrada de la aplicación.

    Ejecuta los procesos de inicio y arranque de la aplicación, y
    posteriormente inicia la aplicación.
    """
    try:
        startup_routines = Startup(__file__)
        settings: Settings = startup_routines.run()

        bootstrap_routines = Bootstrap(settings)
        settings = bootstrap_routines.run()

        if not settings:
            return

        application_process = Application(settings)
        application_process.run(__name__)

    except InvalidConfigurationFileError as exc:
        print(f"No se pudo cargar el archivo de configuración: {exc}")

    except UninitializedOutputDirError as exc:
        print(f"El espacio de trabajo no se ha inicializado: {exc}")

    except UninitializedWorkspaceError as exc:
        print(f"El espacio de trabajo no se ha inicializado: {exc}")
        print(
            f"Ejecuta el comando '{ApplicationInfo.name} init' "
            "para inicializar el espacio de trabajo."
        )

    except Exception as exc:
        print(f"No se puede continuar: Error inesperado: {exc}")
        exit(1)


if __name__ == "__main__":
    main()
