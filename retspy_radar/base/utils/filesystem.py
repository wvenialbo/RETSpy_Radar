"""
Módulo con utilidades para trabajar con archivos.

Las funciones de este módulo permiten verificar si un archivo es
legible, creable o escribible. Las funciones de verificación de
legibilidad y creabilidad son `ensure_readable_file` y
`ensure_creatable_or_writeable_file`, respectivamente.

La función `ensure_readable_file` verifica si un archivo es legible. Si
el archivo no existe o no es legible, o la ruta no apunta a un archivo
se lanza una excepción. La función `ensure_creatable_or_writeable_file`
verifica si un archivo es creable o escribible. Si el archivo no es
creable o escribible, o la ruta no apunta a un archivo se lanza una
excepción.

Las clases de este módulo son:

    - `filesystem`: Clase con utilidades para trabajar con archivos.

Las funciones de este módulo son:

    - `ensure_readable_file`: Verifica si un archivo es legible.
    - `ensure_creatable_or_writeable_file`: Verifica si un archivo es
        creable o escribible.

Las constantes de este módulo son:

    - `FILE_NOT_FOUND_ERROR`: Mensaje de error para archivo no
        encontrado.
    - `IS_A_DIRECTORY_ERROR`: Mensaje de error para objeto es un
        directorio.
    - `NOT_A_FILE_ERROR`: Mensaje de error para objeto no es un archivo.
    - `READ_PERMISSION_ERROR`: Mensaje de error para archivo no es
        legible.
    - `WRITE_PERMISSION_ERROR`: Mensaje de error para archivo no es
        escribible.
"""

import os

from ..exceptions import NotAFileError

# Mensajes de error

FILE_NOT_FOUND_ERROR = "La ruta especificada no existe: '%s'"
IS_A_DIRECTORY_ERROR = "El objeto es un directorio '%s'"
NOT_A_FILE_ERROR = "El objeto no es un archivo: '%s'"
READ_PERMISSION_ERROR = "El archivo no es legible: '%s'"
WRITE_PERMISSION_ERROR = "El archivo no es escribible: '%s'"


class filesystem:  # pylint: disable=invalid-name
    """
    Clase con utilidades para trabajar con archivos.
    """

    @staticmethod
    def ensure_readable_file(
        file_path: str, *, optional: bool = False
    ) -> bool:
        """
        Asegura que un archivo sea legible.

        Si `optional` es `False`, verifica que un archivo exista y sea
        legible. Si el archivo no existe o no es legible, o la ruta no
        apunta a un archivo se lanza una excepción. Si `optional` es
        `True` y el archivo no existe, se retorna `False`; en caso
        contrario, se retorna `True` si el archivo es legible.

        Verifica

        Parameters
        ----------
        file_path : str
            La ruta del archivo a verificar.
        optional : bool, optional
            Si se debe lanzar una excepción si el archivo no existe, por
            defecto es `False`.

        Returns
        -------
        bool
            `True` si el archivo existe y es legible, `False` si el
            archivo no existe y `optional` es `True`.

        Raises
        ------
        FileNotFoundError
            Si el archivo no existe.
        IsADirectoryError
            Si la ruta apunta a un directorio.
        NotAFileError
            Si la ruta no apunta a un archivo.
        PermissionError
            Si el archivo no es legible.
        """
        if not os.path.exists(file_path):
            if optional:
                return False

            raise FileNotFoundError(FILE_NOT_FOUND_ERROR % file_path)

        if os.path.isdir(file_path):
            raise IsADirectoryError(IS_A_DIRECTORY_ERROR % file_path)

        if not os.path.isfile(file_path):
            raise NotAFileError(NOT_A_FILE_ERROR % file_path)

        if not os.access(file_path, os.R_OK):
            raise PermissionError(READ_PERMISSION_ERROR % file_path)

        return True

    @staticmethod
    def ensure_creatable_or_writeable_file(file_path: str) -> None:
        """
        Asegura que un archivo sea creable o escribible.

        Verifica que un archivo sea creable o escribible. Si el archivo
        no es creable o escribible, o la ruta no apunta a un archivo se
        lanza una excepción.

        Parameters
        ----------
        file_path : str
            La ruta del archivo a verificar.

        Raises
        ------
        IsADirectoryError
            Si la ruta apunta a un directorio.
        NotAFileError
            Si la ruta no apunta a un archivo.
        PermissionError
            Si el archivo no es escribible.
        """
        if not os.path.exists(file_path):
            return

        if os.path.isdir(file_path):
            raise IsADirectoryError(IS_A_DIRECTORY_ERROR % file_path)

        if not os.path.isfile(file_path):
            raise NotAFileError(NOT_A_FILE_ERROR % file_path)

        if not os.access(file_path, os.W_OK):
            raise PermissionError(WRITE_PERMISSION_ERROR % file_path)
