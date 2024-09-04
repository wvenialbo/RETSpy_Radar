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
from typing import Any, NoReturn, TypeAlias, cast

from .base.exceptions import ApplicationError, ExitCode, set_error_handler
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
) -> NoReturn:
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
        "%s: %s (exit_code=%s).",
        exc.which,
        exc.what_and_why,
        exc.exit_code,
        exc_info=exc_info,
    )

    sys.exit(exc.exit_code)


def handle_user_interrupt(logger: Logger) -> NoReturn:
    """
    Manejador de interrupciones del usuario.

    Muestra un mensaje de información y finaliza la aplicación.
    """
    logger.info("Ejecución terminada por el usuario.")

    sys.exit(0)


def handle_program_interrupt(value: SystemExit) -> NoReturn:
    """
    Manejador de interrupciones del programa.

    Muestra un mensaje de error y finaliza la aplicación.
    """
    logger: Logger = get_logger(pkg_info.name)

    logging_call: dict[ExitCode, LoggerType] = {
        0: logger.info,
        1: logger.error,
        2: logger.critical,
    }

    exit_code: ExitCode = 2

    production_mode: bool = not os.getenv("RETSPY_LEVEL")

    exc_info: BaseException | bool = False if production_mode else value

    exit_message: str = "Se abortó el programa: SystemExit(exit_code=%s)."

    if value.code:
        tmp_code: Any = value.code

        try:
            tmp_code = int(tmp_code)
        except (TypeError, ValueError):
            tmp_code = exit_code

        exit_code = value.code

        logging_call[tmp_code](exit_message, value, exc_info=exc_info)

    elif not production_mode:
        exit_code = 0

        logger.debug(exit_message, value.code, exc_info=exc_info)

    sys.exit(exit_code)


def main_error_handler(
    exc_type: type[BaseException],
    value: BaseException,
    traceback: TracebackType | None,
) -> NoReturn:
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

    # Errores de solicitud HTTP

    # if isinstance(value, RequestError):
    #     handle_request_error(value, exc_info, logger)

    # Errores de la aplicación controlados

    if isinstance(value, ApplicationError):
        handle_application_error(value, exc_info, logger)

    # Interrupciones del usuario

    if exc_type == KeyboardInterrupt:
        handle_user_interrupt(logger)

    # Errores de argumentos de línea de comandos

    if exc_type == ArgumentError:
        logger.critical(
            "Error del analizador de línea de comandos: %s.",
            value,
            exc_info=exc_info,
        )

    # Errores no esperados (no controlados)

    else:
        logger.exception(
            "Error inesperado: %s: %s.",
            exc_type.__name__,
            value or traceback,
            exc_info=exc_info,
        )

    sys.exit(2)


def main() -> None:
    """
    Punto de entrada de la aplicación.

    Ejecuta los procesos de inicio y arranque de la aplicación, y
    posteriormente inicia la aplicación.
    """
    # Proceso principal de inicio y arranque de la aplicación

    try:
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

    # Salida invocada por algunos procesos (deben verificarse)

    except SystemExit as exc:
        handle_program_interrupt(exc)


if __name__ == PARENT_PROCESS:
    set_error_handler(main_error_handler)
    main()
