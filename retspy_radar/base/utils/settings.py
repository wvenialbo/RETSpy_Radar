"""
Módulo con funciones para cargar y guardar ajustes de configuración
en un archivo.

Las funciones de este módulo permiten cargar y guardar ajustes de
configuración en un archivo JSON. Las funciones de carga y guardado
de ajustes de configuración son `load` y `save`, respectivamente.

La función `load` carga los ajustes de configuración desde un archivo
JSON. Si el archivo no existe, se lanza una excepción. La función
`save` guarda los ajustes de configuración en un archivo JSON.

Las clases de este módulo son:

    - `settings_manager`: Clase con utilidades para cargar y guardar
        ajustes de configuración en un archivo.

Las funciones de este módulo son:

    - `load`: Carga los ajustes de configuración desde un archivo.
    - `save`: Guarda los ajustes de configuración en un archivo.
    - `_load_settings`: Carga los ajustes de configuración desde un
        archivo.
    - `_save_settings`: Guarda los ajustes de configuración en un
        archivo.
"""

from ..exceptions import ConfigurationFileError, NotAFileError
from ..settings import SettingsBasic
from . import filesystem

# Mensajes de error

CONFIG_FILE_NOT_FOUND_ERROR = "No se encontró el archivo de configuración"
CONFIG_FILE_OPEN_ERROR = "No se pudo abrir el archivo de configuración"
CONFIG_FILE_PATH_ERROR = "La ruta del archivo de configuración no es válida"
CONFIG_FILE_READ_ERROR = "No se pudo leer el archivo de configuración"
CONFIG_FILE_WRITE_ERROR = "No se pudo escribir en el archivo de configuración"


class settings_manager:  # pylint: disable=invalid-name

    @classmethod
    def load(
        cls, settings_path: str, fail_if_not_exists: bool
    ) -> SettingsBasic:
        """
        Carga los ajustes de configuración desde un archivo.

        Parameters
        ----------
        settings_path : str
            La ruta del archivo de ajustes de configuración.
        fail_if_not_exists : bool, optional
            Indica si se debe fallar si el archivo no existe.

        Returns
        -------
        SettingsBasic
            Una instancia de la clase SettingsBasic con los ajustes
            cargados desde el archivo.
        """
        return cls._load_settings(
            settings_path, optional=not fail_if_not_exists
        )

    @classmethod
    def save(cls, settings_path: str, settings: SettingsBasic) -> None:
        """
        Guarda los ajustes de configuración en un archivo.

        Parameters
        ----------
        settings_path : str
            La ruta del archivo de ajustes de configuración.
        settings : SettingsBasic
            Los ajustes de configuración a guardar en el
            archivo.
        """
        cls._save_settings(settings_path, settings)

    @staticmethod
    def _load_settings(
        settings_path: str, *, optional: bool = False
    ) -> SettingsBasic:
        """
        Carga los ajustes de configuración desde un archivo.

        Obtiene los ajustes de configuración desde un archivo JSON.
        Falla si no pudo acceder al archivo o si el archivo no tiene
        formato JSON válido si `optional` es `False`. Si `optional` es
        `True` y el archivo no existe, retorna un objeto vacío.

        Parameters
        ----------
        settings_path : str
            La ruta del archivo de configuración.
        optional : bool, optional
            Si se debe lanzar una excepción si el archivo no existe, por
            defecto es `False`.

        Returns
        -------
        SettingsBasic
            Una instancia de la clase `SettingsBasic` con los ajustes
            cargados desde un archivo, o un objeto vacío si el archivo
            no existe y `optional` es `True`.

        Raises
        ------
        ConfigurationFileError
            Si no se pudieron cargar los ajustes de configuración.
        """
        settings = SettingsBasic()

        try:
            # Verificar que la ruta del archivo de configuración sea
            # válida: que la ruta exista y sea un archivo legible
            # (optional=False) o que sea un archivo legible si existe
            # (optional=True)

            exists: bool = filesystem.ensure_readable_file(
                settings_path, optional=optional
            )

            if not exists:
                return settings

            # Leer los ajustes de configuración del archivo JSON,
            # cargarlos en un diccionario y retornarlos

            with open(
                settings_path, "rt", encoding="utf-8", errors="strict"
            ) as file:
                settings.load(file)

            return settings

        except FileNotFoundError as exc:
            raise ConfigurationFileError(CONFIG_FILE_NOT_FOUND_ERROR) from exc

        except (IsADirectoryError, NotAFileError) as exc:
            raise ConfigurationFileError(CONFIG_FILE_OPEN_ERROR) from exc

        except (PermissionError, IOError) as exc:  # IOError == OSError
            raise ConfigurationFileError(CONFIG_FILE_READ_ERROR) from exc

    @staticmethod
    def _save_settings(settings_path: str, settings: SettingsBasic) -> None:
        """
        Guarda los ajustes de configuración en un archivo.

        Intenta guardar los ajustes de configuración en un archivo JSON.

        Parameters
        ----------
        settings_path : str
            La ruta del archivo de configuración.
        settings : SettingsBasic
            Los ajustes de configuración a guardar en el
            archivo.

        Raises
        ------
        ConfigurationFileError
            Si no se pudieron guardar las credenciales.
        """
        try:
            # Verificar que la ruta del archivo de configuración sea
            # válida: que la ruta no exista o que no sea un directorio

            filesystem.ensure_creatable_or_writeable_file(settings_path)

            # Escribir el diccionario en un archivo de configuración

            with open(
                settings_path, "wt", encoding="utf-8", newline="\n"
            ) as file:
                settings.dump(file)

        except (IsADirectoryError, NotAFileError) as exc:
            raise ConfigurationFileError(CONFIG_FILE_PATH_ERROR) from exc

        except (PermissionError, IOError) as exc:  # IOError == OSError
            raise ConfigurationFileError(CONFIG_FILE_WRITE_ERROR) from exc
