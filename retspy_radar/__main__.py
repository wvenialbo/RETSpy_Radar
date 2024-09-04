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
import sys
from argparse import ArgumentError
from types import TracebackType
from typing import TypeAlias, cast

from .base.exceptions import (
    ApplicationError,
    ExitCode,
    UninitializedOutputDirError,
    UninitializedWorkspaceError,
    UnspecifiedCommandError,
    set_error_handler,
)
from .base.logging import Logger, LoggerType, get_logger
from .base.settings import SettingsBasic
from .core import Application, Bootstrap, Startup
from .package_info import pkg_info

ExceptionInfo: TypeAlias = BaseException | bool

PARENT_PROCESS = "__main__"
CHILD_PROCESS = "__mp_main__"


def handle_application_error(
    value: BaseException,
    exc_info: ExceptionInfo,
    logger: Logger,
) -> None:
    """
    Manejador de errores de la aplicación.

    Muestra un mensaje de error y finaliza la aplicación. El mensaje
    incluye el tipo de error, la descripción del error y el código de
    salida. Si `exc_info` es un objeto de excepción, se incluirá en el
    mensaje.

    Parameters
    ----------
    value : BaseException
        Excepción.
    exc_info : ExceptionInfo
        Información de la excepción.
    logger : Logger
        Objeto de registro de eventos.
    """
    loggers: dict[ExitCode, LoggerType] = {
        0: logger.warning,
        1: logger.error,
        2: logger.critical,
    }

    exc: ApplicationError = cast(ApplicationError, value)

    logger_call: LoggerType = loggers.get(exc.exit_code, logger.error)

    logger_call(
        "%s: %s (%s).",
        exc.which,
        exc.what_and_why,
        exc.exit_code,
        exc_info=exc_info,
    )

    sys.exit(exc.exit_code)


def handle_user_interrupt(logger: Logger) -> None:
    """
    Manejador de interrupciones del usuario.

    Muestra un mensaje de información y finaliza la aplicación.
    """
    logger.info("Ejecución terminada por el usuario.")

    sys.exit(0)


def main_error_handler(
    exc_type: type[BaseException],
    value: BaseException,
    traceback: TracebackType | None,
) -> None:
    """
    Manejador global de errores.

    Parameters
    ----------
    exc_type : type[BaseException]
        Tipo de excepción.
    value : BaseException
        Excepción.
    traceback : TracebackType
        Rastro de la excepción.
    """
    logger: Logger = get_logger(pkg_info.name)

    production_mode: bool = not os.getenv("RETSPY_LEVEL")

    exc_info: BaseException | bool = False if production_mode else value

    if isinstance(value, ApplicationError):
        handle_application_error(value, exc_info, logger)

    if exc_type == KeyboardInterrupt:
        handle_user_interrupt(logger)

    logger.exception(
        "No se puede continuar: Error inesperado: %s: %s.",
        exc_type.__name__,
        value or traceback,
        exc_info=exc_info,
    )


def main() -> None:
    """
    Punto de entrada de la aplicación.

    Ejecuta los procesos de inicio y arranque de la aplicación, y
    posteriormente inicia la aplicación.
    """
    # Prepara el entorno de ejecución

    exit_code: ExitCode = 1

    # Crea e inicializa el objeto de registro de eventos

    logger: Logger = get_logger(pkg_info.name)

    # Activa el color de la consola

    os.system("color")

    # Inicia y ejecuta el proceso de inicio

    startup_routines = Startup(__file__)
    settings: SettingsBasic = startup_routines.run()

    # Inicia y ejecuta el proceso de arranque

    bootstrap_routines = Bootstrap(settings)
    settings = bootstrap_routines.run()

    # Inicia y ejecuta la aplicación

    application_process = Application(settings)
    application_process.run()

    try:

        # Errores esperados
        application_process.run()

    except UninitializedOutputDirError as exc:
        logger.error(
            "El directorio del repositorio no se ha inicializado: %s.",
            exc,
            exc_info=True,
        )

    except UninitializedWorkspaceError as exc:
        logger.error(
            "El espacio de trabajo no se ha inicializado: %s.",
            exc,
            exc_info=True,
        )
        logger.info(
            "Ejecuta el comando '%s init' para inicializar "
            "el espacio de trabajo.",
            pkg_info.name,
        )

    except (NotADirectoryError, IsADirectoryError) as exc:
        logger.error("Error de archivo de usuario: %s.", exc, exc_info=True)

    except UnspecifiedCommandError as exc:
        logger.error(
            "No se especificó ninguna acción: %s.", exc, exc_info=True
        )

    # Salida invocada por algunos procesos, podría deberse a un error

    except SystemExit as exc:
        exit_code = exc.code

        if not exit_code:
            return

        logging_call: dict[int, LoggerType] = {
            0: logger.info,
            1: logger.error,
            2: logger.critical,
        }

        logging_call[int(exit_code)](
            "Se abortó el programa: SystemExit(exit_code=%s).", exc
        )

    # Errores no esperados o no controlados

    except ArgumentError as exc:
        logger.critical(
            "Error del analizador de línea de comandos: %s.",
            exc,
            exc_info=True,
        )
        exit_code = 2

    except FileNotFoundError as exc:
        logger.critical(
            "Error de empaquetado de archivos: %s.", exc, exc_info=True
        )
        exit_code = 2

    except OSError as exc:
        logger.exception("Error del sistema: %s.", exc)
        exit_code = 2

    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        logger.exception("Error de programación: %s.", exc)
        exit_code = 2

    # Excepciones no manejadas

    except Exception as exc:
        logger.exception("No se puede continuar: Error inesperado: %s.", exc)
        exit_code = 2

    # Finalización de la aplicación

    else:
        # Salida normal

        exit_code = 0

    finally:
        # Salida con error (exit_code!=0) / controlada (exit_code==0)

        if exit_code:
            logger.debug(
                "Saliendo de {%s} con código de salida %s.",
                pkg_info.name,
                exit_code,
            )

            sys.exit(exit_code)


if __name__ == PARENT_PROCESS:
    set_error_handler(main_error_handler)
    main()
    main()
