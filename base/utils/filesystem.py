import os

from ..exceptions import NotAFileError

FILE_NOT_FOUND_ERROR = "No se encontró la ruta especificada"
NOT_A_FILE_ERROR = "El objeto no es un archivo"
READ_PERMISSION_ERROR = "El archivo no es legible"
WRITE_PERMISSION_ERROR = "El archivo no es escribible"
IS_A_DIRECTORY_ERROR = "El objeto es un directorio"


class filesystem:
    @staticmethod
    def ensure_readable_file(file_path: str) -> None:
        """
        Asegura que un archivo sea legible.

        Verifica que un archivo exista y sea legible. Si el archivo no
        existe o no es legible, o la ruta no apunta a un archivo se
        lanza una excepción.

        Parameters
        ----------
        file_path : str
            La ruta del archivo a verificar.

        Raises
        ------
        FileNotFoundError
            Si el archivo no existe.
        NotAFileError
            Si la ruta no apunta a un archivo.
        PermissionError
            Si el archivo no es legible.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(FILE_NOT_FOUND_ERROR)

        if not os.path.isfile(file_path):
            raise NotAFileError(NOT_A_FILE_ERROR)

        if not os.access(file_path, os.R_OK):
            raise PermissionError(READ_PERMISSION_ERROR)

    @staticmethod
    def ensure_optional_file(file_path: str) -> bool:
        """
        Asegura que un archivo sea legible si existe.

        Verifica que un archivo sea legible si existe. Si el archivo
        existe y no es legible, o la ruta no apunta a un archivo, se
        lanza una excepción.

        Parameters
        ----------
        file_path : str
            La ruta del archivo a verificar.

        Raises
        ------
        NotAFileError
            Si la ruta no apunta a un archivo.
        PermissionError
            Si el archivo no es legible.
        """
        if not os.path.exists(file_path):
            return False

        if not os.path.isfile(file_path):
            raise NotAFileError(NOT_A_FILE_ERROR)

        if not os.access(file_path, os.R_OK):
            raise PermissionError(READ_PERMISSION_ERROR)

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
            raise IsADirectoryError(IS_A_DIRECTORY_ERROR)

        if not os.path.isfile(file_path):
            raise NotAFileError(NOT_A_FILE_ERROR)

        if not os.access(file_path, os.W_OK):
            raise PermissionError(WRITE_PERMISSION_ERROR)
