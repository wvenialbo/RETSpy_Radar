"""
Módulo que contiene las excepciones personalizadas de la aplicación.
"""

import sys
from types import TracebackType
from typing import Callable, TypeAlias

ExitCode: TypeAlias = str | int | None
ErrorHandler: TypeAlias = Callable[..., None]


class ApplicationError(Exception):
    """
    Lanzado si hubo un error en la aplicación.
    """

    def __init__(self, what: str, exit_code: ExitCode = 1) -> None:
        super().__init__(what)
        self._exit_code = exit_code

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
    def exit_code(self) -> ExitCode:
        return self._exit_code

    @exit_code.setter
    def exit_code(self, value: ExitCode) -> None:
        self._exit_code = value

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


class AuthorizationError(ApplicationError):
    """
    Lanzado si no se pudo obtener un token de acceso.
    """


class AuthorizationExpiredError(RuntimeError):
    """
    Lanzado si el token de acceso ha expirado.
    """


class ConfigurationFileError(ApplicationError):
    """
    Lanzado si el acceso al archivo de configuración produjo errores.
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


class RequestError(ConnectionError):
    """
    Lanzado si hubo un error al realizar una solicitud HTTP.
    """

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code: int = status_code


class TimeConversionError(ValueError):
    """
    Lanzado si no se pudo convertir una información de tiempo.
    """


class UnexpectedResponseError(ConnectionError):
    """
    Lanzado si la respuesta de una solicitud HTTP no es la esperada.
    """


class UninitializedOutputDirError(RuntimeError):
    """
    Lanzado si no se pudo inicializar el directorio de salida.
    """


class UninitializedWorkspaceError(RuntimeError):
    """
    Lanzado si no se pudo inicializar el espacio de trabajo.
    """


class UnspecifiedCommandError(RuntimeError):
    """
    Lanzado si no se pudo inicializar el espacio de trabajo.
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
sys.excepthook = _except_hook
