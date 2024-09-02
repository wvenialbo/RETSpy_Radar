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
    exit_code: int = 1

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

    except KeyboardInterrupt:
        logger.info("El usuario ha interrumpido la ejecución del programa.")
        exit_code = 0

    except ArgumentError as exc:
        logger.critical(f"Error del analizador de línea de comandos: {exc}.")
        exit_code = 2

    except SystemExit as exc:
        exit_code = int(f"{exc.code}")

        if not exit_code:
            return

        logging_call = {
            0: logger.info,
            1: logger.error,
            2: logger.critical,
        }

        logging_call[exit_code](
            f"Se abortó el programa: SystemExit(exit_code={exc})."
        )

    # except Exception as exc:
    #     logger.critical(f"No se puede continuar: Error inesperado: {exc}.")
    # exit_code = 2

    else:
        exit_code = 0

    finally:
        if not exit_code:
            return

        logger.debug(
            f"Saliendo de {pkg_info.name} "
            f"con código de salida {exit_code}."
        )

        exit(exit_code)


if __name__ == PARENT_PROCESS:
    main()
