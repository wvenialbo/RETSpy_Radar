import json
from json import JSONDecodeError
from typing import Any

from ..exceptions import InvalidConfigurationFileError, NotAFileError
from ..utils.filesystem import filesystem
from .settings_section import SettingsSection
from .settings_section_adapter import Section
from .settings_value_adapter import Value


class SettingsBase(SettingsSection):
    """
    Ajustes de configuración almacenados en archivos JSON.

    Attributes
    ----------
    _root : dict[str, Any]
        El objeto raíz de los ajustes de configuración como un
        diccionario de secciones y valores.

    Methods
    -------
    has(key: str) -> bool
        Indica si los ajustes de configuración contienen una subsección
        o valor con la clave especificada.
    is_empty() -> bool
        Indica si la sección de ajustes de configuración está vacía.
    section(key: str) -> Section
        Obtiene una subsección de ajustes de configuración.
    value(key: str) -> Value
        Obtiene un valor de ajuste de configuración.
    _acquire_settings(settings_path: str) -> dict[str, Any]
        Carga los ajustes de configuración desde un archivo, si existe.
    _load_settings(settings_path) -> dict[str, Any]
        Carga los ajustes de configuración desde un archivo.
    _save_settings(settings_path, root) -> None
        Guarda los ajustes de configuración en un archivo.
    """

    def __init__(self, settings: dict[str, Any]) -> None:
        """
        Inicializa los ajustes de configuración.

        Parameters
        ----------
        settings : dict[str, Any]
            Los ajustes de configuración como un diccionario de
            secciones y valores.
        """
        self._root = Section(settings)

    def has(self, key: str) -> bool:
        """
        Indica si los ajustes de configuración contienen una subsección
        o valor con la clave especificada.

        Parameters
        ----------
        key : str
            La clave de la subsección o valor.

        Returns
        -------
        bool
            True si los ajustes de configuración contienen una
            subsección o valor con la clave especificada, False
            en caso contrario.
        """
        return self._root.has(key)

    def is_empty(self) -> bool:
        """
        Indica si la sección de ajustes de configuración está vacía.

        Returns
        -------
        bool
            True si la sección de ajustes de configuración está vacía,
            False en caso contrario.
        """
        return self._root.is_empty()

    def section(self, key: str) -> "Section":
        """
        Obtiene una subsección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave de la subsección de ajustes de configuración.

        Returns
        -------
        Section
            La subsección de ajustes de configuración.
        """
        return self._root.section(key)

    def value(self, key: str) -> Value:
        """
        Obtiene un valor de ajuste de configuración.

        Parameters
        ----------
        key : str
            La clave del valor de ajuste de configuración.

        Returns
        -------
        Value
            El valor de ajuste de configuración.
        """
        return self._root.value(key)

    @staticmethod
    def _acquire_settings(settings_path: str) -> dict[str, Any]:
        """
        Carga los ajustes de configuración desde un archivo, si existe.

        Intenta obtener los ajustes de configuración desde un archivo
        JSON. Retorna un diccionario vacío si no se pudo acceder al
        archivo o si el archivo no existe.

        Parameters
        ----------
        settings_path : str
            La ruta del archivo de configuración.

        Returns
        -------
        dict[str, Any]
            Los ajustes de configuración.

        Raises
        ------
        InvalidConfigurationFileError
            Si no se pudieron cargar los ajustes de configuración.
        """
        try:
            # Verificar que la ruta del archivo de configuración sea
            # válida: que sea un archivo legible si existiere

            exists: bool = filesystem.ensure_optional_file(settings_path)

            if not exists:
                return dict()

            # Leer los ajustes de configuración del archivo JSON,
            # cargarlos en un diccionario y retornarlos

            with open(settings_path, "r", encoding="utf-8") as file:
                settings: Any = json.load(file)

            return settings

        except JSONDecodeError as exc:
            raise InvalidConfigurationFileError(
                "El archivo de configuración no tiene formato "
                f"JSON válido: {exc}"
            ) from exc

        except (FileNotFoundError, NotAFileError) as exc:
            raise InvalidConfigurationFileError(
                f"La ruta del archivo de configuración no es válida: {exc}"
            ) from exc

        except (PermissionError, IOError) as exc:  # == OSError
            raise InvalidConfigurationFileError(
                "No se pudo acceder a la ruta del archivo de "
                f"configuración: {exc}"
            ) from exc

    @staticmethod
    def _load_settings(settings_path: str) -> dict[str, Any]:
        """
        Carga los ajustes de configuración desde un archivo.

        Intenta obtener los ajustes de configuración desde un archivo
        JSON. Falla si no se puede acceder al archivo o si el archivo
        no tiene formato JSON válido.

        Parameters
        ----------
        settings_path : str
            La ruta del archivo de configuración.

        Returns
        -------
        dict[str, Any]
            Los ajustes de configuración.

        Raises
        ------
        InvalidConfigurationFileError
            Si no se pudieron cargar los ajustes de configuración.
        """
        try:
            # Verificar que la ruta del archivo de configuración sea
            # válida: que la ruta exista y sea un archivo legible

            filesystem.ensure_readable_file(settings_path)

            # Leer los ajustes de configuración del archivo JSON,
            # cargarlos en un diccionario y retornarlos

            with open(settings_path, "r", encoding="utf-8") as file:
                settings: Any = json.load(file)

            return settings

        except JSONDecodeError as exc:
            raise InvalidConfigurationFileError(
                "El archivo de configuración no tiene formato "
                f"JSON válido: {exc}"
            ) from exc

        except (FileNotFoundError, NotAFileError) as exc:
            raise InvalidConfigurationFileError(
                f"La ruta del archivo de configuración no es válida: {exc}"
            ) from exc

        except (PermissionError, IOError) as exc:  # == OSError
            raise InvalidConfigurationFileError(
                "No se pudo acceder a la ruta del archivo de "
                f"configuración: {exc}"
            ) from exc

    @staticmethod
    def _save_settings(settings_path: str, root: dict[str, Any]) -> None:
        """
        Guarda los ajustes de configuración en un archivo.

        Intenta guardar los ajustes de configuración en un archivo JSON.

        Parameters
        ----------
        settings_path : str
            La ruta del archivo de configuración.
        root : dict[str, Any]
            Los ajustes de configuración.

        Raises
        ------
        InvalidConfigurationFileError
            Si no se pudieron guardar las credenciales.
        """
        try:
            # Verificar que la ruta del archivo de configuración sea
            # válida: que la ruta no exista o que no sea un directorio

            filesystem.ensure_creatable_or_writeable_file(settings_path)

            # Escribir el diccionario en un archivo de configuración

            with open(
                settings_path, "w", encoding="utf-8", newline="\n"
            ) as file:
                json.dump(root, file, indent=4)

        except TypeError:
            raise InvalidConfigurationFileError(
                "No se pudieron guardar las credenciales"
            )

        except (IsADirectoryError, NotAFileError):
            raise InvalidConfigurationFileError(
                "La ruta del archivo de credenciales no es válida"
            )

        except (PermissionError, IOError):  # == OSError
            raise InvalidConfigurationFileError(
                "No se pudo acceder al archivo de credenciales"
            )

    @property
    def root(self) -> "Section":
        """
        La raíz de los ajustes de configuración.

        Returns
        -------
        Section
            La raíz de los ajustes de configuración.
        """
        return self._root
