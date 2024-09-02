import json
from io import TextIOWrapper
from json import JSONDecodeError
from typing import Any

from ..exceptions import InvalidConfigurationFileError
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

    def __init__(self, data: Any | None = None) -> None:
        """
        Inicializa los ajustes de configuración.

        Parameters
        ----------
        settings : Any, optional
            Un diccionario con los ajustes de configuración. Si no se
            especifica, se crea una sección de ajustes de configuración
            vacía.
        """
        super().__init__(data)

    def dump(self, file: TextIOWrapper) -> None:
        """
        Guarda los ajustes de configuración en un archivo.

        Parameters
        ----------
        file : TextIOWrapper
            El archivo de ajustes de configuración.

        Raises
        ------
        InvalidConfigurationFileError
            Si no se pudieron guardar los ajustes de configuración.
        """
        try:
            # Escribir los ajustes de configuración en el archivo

            json.dump(self._root.to_dict(), file, indent=4)

        except TypeError:
            raise InvalidConfigurationFileError(
                "No se pudieron guardar los ajustes de configuración"
            )

    def load(self, file: TextIOWrapper) -> None:
        """
        Carga los ajustes de configuración desde un archivo.

        Parameters
        ----------
        file : TextIOWrapper
            El archivo de ajustes de configuración.

        Raises
        ------
        InvalidConfigurationFileError
            Si no se pudieron cargar los ajustes de configuración.
        """
        try:
            # Cargar los ajustes de configuración en un diccionario y
            # actualizar el objeto raíz de ajustes de configuración.
            # Se asume archivo JSON

            settings: Any = json.load(file)
            self.update(settings)

        except JSONDecodeError as exc:
            raise InvalidConfigurationFileError(
                "El archivo de configuración no tiene formato "
                f"JSON válido: {exc}"
            ) from exc
