from ..exceptions import InvalidConfigurationFileError, NotAFileError
from ..settings import SettingsBasic
from . import filesystem


class settings:

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
        if fail_if_not_exists:
            return cls._load_settings(settings_path)

        return cls._acquire_settings(settings_path)

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
    def _acquire_settings(settings_path: str) -> SettingsBasic:
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
        SettingsBasic
            Una instancia de la clase SettingsBasic con los ajustes
            cargados desde el archivo.

        Raises
        ------
        InvalidConfigurationFileError
            Si no se pudieron cargar los ajustes de configuración.
        """
        settings = SettingsBasic()

        try:
            # Verificar que la ruta del archivo de configuración sea
            # válida: que sea un archivo legible si existiere

            exists: bool = filesystem.ensure_optional_file(settings_path)

            if not exists:
                return settings

            # Leer los ajustes de configuración del archivo JSON,
            # cargarlos en un diccionario y retornarlos

            with open(settings_path, "r", encoding="utf-8") as file:
                settings.load(file)

            return settings

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
    def _load_settings(settings_path: str) -> SettingsBasic:
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
        SettingsBasic
            Una instancia de la clase SettingsBasic con los ajustes
            cargados desde el archivo.

        Raises
        ------
        InvalidConfigurationFileError
            Si no se pudieron cargar los ajustes de configuración.
        """
        settings = SettingsBasic()

        try:
            # Verificar que la ruta del archivo de configuración sea
            # válida: que la ruta exista y sea un archivo legible

            filesystem.ensure_readable_file(settings_path)

            # Leer los ajustes de configuración del archivo JSON,
            # cargarlos en un diccionario y retornarlos

            with open(settings_path, "r", encoding="utf-8") as file:
                settings.load(file)

            return settings

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
                settings.dump(file)

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
