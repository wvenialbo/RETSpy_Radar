"""
Este script es el punto de entrada del Robot de descarga de imágenes y
mosaicos de radar del Sistema Nacional de Radares Meteorológicos
(SINARAME) del Servicio Meteorológico Nacional (SMN) argentino.

Si no se proveen argumentos, se utilizarán los valores por defecto. Para
más información, ejecute el script con la opción -h o --help.
"""

from argparse import ArgumentError

from .base.exceptions import (
    InvalidConfigurationFileError,
    UninitializedOutputDirError,
    UninitializedWorkspaceError,
    UnspecifiedCommandError,
)
from .base.logging import Logger, get_logger
from .base.settings import SettingsBasic
from .core import Application, Bootstrap, Startup
from .package_info import pkg_info

PARENT_PROCESS = "__main__"
CHILD_PROCESS = "__mp_main__"


def main() -> None:
    """
    Punto de entrada de la aplicación.

    Ejecuta los procesos de inicio y arranque de la aplicación, y
    posteriormente inicia la aplicación.
    """
    logger: Logger = get_logger(pkg_info.name)

    try:
        startup_routines = Startup(__file__)
        settings: SettingsBasic = startup_routines.run()

        bootstrap_routines = Bootstrap(settings)
        settings = bootstrap_routines.run()

        application_process = Application(settings)
        application_process.run()

    except InvalidConfigurationFileError as exc:
        logger.error(f"No se pudo cargar el archivo de configuración: {exc}.")

    except UninitializedOutputDirError as exc:
        logger.error(f"El espacio de trabajo no se ha inicializado: {exc}.")

    except UninitializedWorkspaceError as exc:
        logger.error(f"El espacio de trabajo no se ha inicializado: {exc}.")
        logger.info(
            f"Ejecuta el comando '{pkg_info.name} init' "
            "para inicializar el espacio de trabajo."
        )

    except UnspecifiedCommandError as exc:
        logger.error(f"Debe especificar una acción: {exc}.")
        exit(1)

    except KeyboardInterrupt:
        logger.info("El usuario ha interrumpido la ejecución del programa.")

    except ArgumentError as exc:
        logger.critical(f"Error del analizador de línea de comandos: {exc}.")
        exit(2)

    except SystemExit as exc:
        if not exc.code:
            return

        exit_code = int(f"{exc.code}")

        logging_call = {
            0: logger.info,
            1: logger.error,
            2: logger.critical,
        }

        logging_call[exit_code](f"Saliendo del programa: exit_code={exc}.")
        exit(exit_code)

    # except Exception as exc:
    #     logger.critical(f"No se puede continuar: Error inesperado: {exc}.")
    #     exit(2)


if __name__ == PARENT_PROCESS:
    main()
