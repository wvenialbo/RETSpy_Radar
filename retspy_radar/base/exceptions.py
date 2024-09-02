class AuthorizationError(RuntimeError):
    """
    Lanzado si no se pudo obtener un token de acceso.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class AuthorizationExpiredError(RuntimeError):
    """
    Lanzado si el token de acceso ha expirado.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidConfigurationFileError(TypeError):
    """
    Lanzado si el archivo de configuración no es válido.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidTimeFormatError(ValueError):
    """
    Lanzado si el formato de tiempo no es válido.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidTimeLapseError(ValueError):
    """
    Lanzado si el lapso de tiempo no es válido.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidTimeRangeError(ValueError):
    """
    Lanzado si el rango de tiempo no es válido.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotAFileError(OSError):
    """
    Lanzado si el objeto del sistema existe pero no es un archivo.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class RequestError(ConnectionError):
    """
    Lanzado si hubo un error al realizar una solicitud HTTP.
    """

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code: int = status_code


class UnexpectedResponseError(ConnectionError):
    """
    Lanzado si la respuesta de una solicitud HTTP no es la esperada.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class TimeConversionError(ValueError):
    """
    Lanzado si no se pudo convertir una información de tiempo.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class UninitializedWorkspaceError(RuntimeError):
    """
    Lanzado si no se pudo inicializar el espacio de trabajo.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class UninitializedOutputDirError(RuntimeError):
    """
    Lanzado si no se pudo inicializar el directorio de salida.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class UnspecifiedCommandError(RuntimeError):
    """
    Lanzado si no se pudo inicializar el espacio de trabajo.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
