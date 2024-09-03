"""
Este script es el punto de entrada del indexador de imágenes y mosaicos
de radares meteorológicos «RETSpy-Radar» capaz de acceder a productos de
distintos servicios, como SINARAME y SIMEPAR.

El script se encarga de cargar la configuración, inicializar el espacio
de trabajo, y ejecutar la acción especificada por el usuario.

El usuario puede especificar la acción a ejecutar mediante comandos y
argumentos de línea de comandos. Por ejemplo, para inicializar el
espacio de trabajo, el usuario puede ejecutar el comando:

                        `retspy init`.

El usuario debe especificar la acción a ejecutar. Si no se especifica
ninguna acción, el script mostrará un mensaje de error y finalizará. Si
no se proveen argumentos, se utilizarán los valores por defecto. Para
obtener más información, el usuario puede ejecutar el comando:

                `retspy --help` o `retspy -h`;

para obtener información sobre los argumentos disponibles para cada
comando, el usuario puede ejecutar el comando:

        `retspy <comando> --help` o `retspy <comando> -h`.

El script también maneja errores y excepciones, y registra mensajes de
del sistema en un archivo de registro.
"""

import os
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

    # Prepara el entorno de ejecución

    try:
        # Crea e inicializa el objeto de registro de eventos

        logger: Logger = get_logger(pkg_info.name)

        # Activa el color de la consola

        os.system("color")

    except Exception as exc:
        print(f"Error al crear el objeto de registro: {exc}.")

        exit(exit_code)

    # Inicia la ejecución de la aplicación

    try:
        # Inicia y ejecuta el proceso de inicio

        startup_routines = Startup(__file__)
        settings: SettingsBasic = startup_routines.run()

        # Inicia y ejecuta el proceso de arranque

        bootstrap_routines = Bootstrap(settings)
        settings = bootstrap_routines.run()

        # Inicia y ejecuta la aplicación

        application_process = Application(settings)
        application_process.run()

    # Interrupciones del usuario

    except KeyboardInterrupt:
        logger.info("El usuario ha interrumpido la ejecución del programa.")
        exit_code = 0

    # Errores esperados

    except InvalidConfigurationFileError as exc:
        logger.error(f"No se pudo cargar el archivo de configuración: {exc}.")

    except UninitializedOutputDirError as exc:
        logger.error(
            f"El directorio del repositorio no se ha inicializado: {exc}."
        )

    except UninitializedWorkspaceError as exc:
        logger.error(f"El espacio de trabajo no se ha inicializado: {exc}.")
        logger.info(
            f"Ejecuta el comando '{pkg_info.name} init' "
            "para inicializar el espacio de trabajo."
        )

    except (NotADirectoryError, IsADirectoryError) as exc:
        logger.error(f"Error de archivo de usuario: {exc}.")

    except UnspecifiedCommandError as exc:
        logger.error(f"No se especificó ninguna acción: {exc}.")

    # Salida invocada por algunos procesos, podría deberse a un error

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

    # Errores no esperados o no controlados

    except ArgumentError as exc:
        logger.critical(f"Error del analizador de línea de comandos: {exc}.")
        exit_code = 2

    except FileNotFoundError as exc:
        logger.critical(f"Error de empaquetado de archivos: {exc}.")
        exit_code = 2

    except OSError as exc:
        logger.critical(f"Error del sistema: {exc}.")
        exit_code = 2

    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        logger.critical(f"Error de programación: {exc}.")
        exit_code = 2

    # Excepciones no manejadas

    except Exception as exc:
        logger.critical(f"No se puede continuar: Error inesperado: {exc}.")
        exit_code = 2

    # Finalización de la aplicación

    else:
        # Salida normal

        exit_code = 0

    finally:
        # Salida controlada

        if not exit_code:
            return

        # Salida con error

        logger.debug(
            f"Saliendo de {pkg_info.name} "
            f"con código de salida {exit_code}."
        )

        exit(exit_code)


if __name__ == PARENT_PROCESS:
    main()
