"""
Módulo que contiene las excepciones personalizadas de la aplicación.
"""

import sys
from types import TracebackType
from typing import Callable, TypeAlias

ExitCode: TypeAlias = str | int | None
ErrorHandler: TypeAlias = Callable[..., None]


class BaseError(Exception):
    """
    Clase base para las excepciones personalizadas.
    """

    def __init__(self, what: str, some_code: ExitCode) -> None:
        super().__init__(what)
        self._some_code: ExitCode = some_code

    @staticmethod
    def _why_chain(exc: BaseException | None) -> str:
        """
        Construye una cadena de mensajes de error.

        Parameters
        ----------
        exc : BaseException | None
            Excepción o `None`.

        Returns
        -------
        str
            Cadena de mensajes de error.
        """
        messages: list[str] = []

        while exc:
            messages.append(str(exc))
            exc = exc.__cause__

        return ": ".join(messages)

    @property
    def which(self) -> str:
        return self.__class__.__name__

    @property
    def what(self) -> str:
        return str(self)

    @property
    def what_and_why(self) -> str:
        return self._why_chain(self)

    @property
    def why(self) -> str:
        return self._why_chain(self.__cause__)


class ApplicationError(BaseError):
    """
    Lanzado si hubo un error en la aplicación.
    """

    def __init__(self, what: str, exit_code: int = 1) -> None:
        super().__init__(what, exit_code)

    @property
    def exit_code(self) -> ExitCode:
        return self._some_code


class AuthorizationError(ApplicationError):
    """
    Lanzado si no se pudo obtener un token de acceso.
    """


class ConfigurationFileError(ApplicationError):
    """
    Lanzado si el acceso al archivo de configuración produjo errores.
    """


class UninitializedOutputDirError(ApplicationError):
    """
    Lanzado si no se pudo inicializar el directorio de salida.
    """


class UninitializedWorkspaceError(ApplicationError):
    """
    Lanzado si no se pudo inicializar el espacio de trabajo.
    """


class UnspecifiedCommandError(ApplicationError):
    """
    Lanzado si no se pudo inicializar el espacio de trabajo.
    """


class RequestError(BaseError):
    """
    Lanzado si hubo un error al realizar una solicitud HTTP.
    """

    def __init__(self, what: str, status_code: int = 200) -> None:
        super().__init__(what, status_code)

    @property
    def status_code(self) -> ExitCode:
        return self._some_code


class AuthorizationExpiredError(RuntimeError):
    """
    Lanzado si el token de acceso ha expirado.
    """


class InvalidTimeFormatError(ValueError):
    """
    Lanzado si el formato de tiempo no es válido.
    """


class InvalidTimeLapseError(ValueError):
    """
    Lanzado si el lapso de tiempo no es válido.
    """


class InvalidTimeRangeError(ValueError):
    """
    Lanzado si el rango de tiempo no es válido.
    """


class NotAFileError(OSError):
    """
    Lanzado si el objeto del sistema existe pero no es un archivo.
    """


class TimeConversionError(ValueError):
    """
    Lanzado si no se pudo convertir una información de tiempo.
    """


class UnexpectedResponseError(ConnectionError):
    """
    Lanzado si la respuesta de una solicitud HTTP no es la esperada.
    """


_exc_handler: ErrorHandler | None = None


def _except_hook(
    exc_type: type[BaseException],
    value: BaseException,
    traceback: TracebackType | None,
) -> None:
    """
    Manejador de errores no controlados.

    Parameters
    ----------
    exc_type : type[BaseException]
        Tipo de excepción.
    value : BaseException
        Excepción.
    traceback : TracebackType, optional
        Rastro de la excepción, por defecto es None.
    """
    if _exc_handler is not None:
        _exc_handler(exc_type, value, traceback)
    else:
        sys.__excepthook__(exc_type, value, traceback)


def set_error_handler(handler: ErrorHandler | None = None) -> None:
    """
    Establece un manejador de errores.

    Parameters
    ----------
    handler : Callable[..., None], optional
        Función que maneja los errores, por defecto es None.
    """
    global _exc_handler  # pylint: disable=global-statement

    _exc_handler = handler


def get_default_error_handler() -> ErrorHandler:
    """
    Retorna el manejador de errores por defecto.

    Returns
    -------
    Callable[..., None]
        Manejador de errores por defecto.
    """
    return sys.__excepthook__


sys.excepthook = _except_hook
