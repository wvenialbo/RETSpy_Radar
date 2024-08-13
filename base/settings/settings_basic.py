from typing import Any

from .settings_base import SettingsBase


class SettingsBasic(SettingsBase):
    """
    Ajustes de configuración básicos para el robot.

    Methods
    -------
    load(settings_path: str) -> SettingsBasic
        Carga los ajustes de configuración desde un archivo.

    Properties
    ----------
    root : Section
        Obtiene la raíz de los ajustes de configuración.
    """

    def __init__(self, settings: dict[str, Any]) -> None:
        """
        Inicializa una nueva instancia de la clase SettingsBasic.

        Parameters
        ----------
        settings : dict[str, Any]
            Un diccionario con los ajustes de configuración.
        """
        super().__init__(settings)

    @classmethod
    def load(
        cls, settings_path: str, fail_if_not_exists: bool = True
    ) -> "SettingsBasic":
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
            settings_dict: dict[str, Any] = cls._load_settings(settings_path)

        else:
            settings_dict = cls._acquire_settings(settings_path)

        return SettingsBasic(settings_dict)

    def save(self, settings_path: str) -> None:
        """
        Guarda los ajustes de configuración en un archivo.

        Parameters
        ----------
        settings_path : str
            La ruta del archivo de ajustes de configuración.
        """
        self._save_settings(settings_path, self._root.to_dict())
