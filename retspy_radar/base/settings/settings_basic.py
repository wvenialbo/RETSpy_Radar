"""
Define un manipulador básico de ajustes de configuración.

La clase `SettingsBasic` proporciona funciones básicas para manipular,
cargar y guardar ajustes de configuración en un archivo.

Las clases de este módulo son:

    - `SettingsBasic`: Ajustes de configuración básico.

Las funciones de `SettingsBasic` son:

    - `load`: Carga los ajustes de configuración desde un archivo.
    - `save`: Guarda los ajustes de configuración en un archivo.
"""

import json
from io import TextIOWrapper
from json import JSONDecodeError
from typing import Any

from ..exceptions import ConfigurationFileError
from .settings_base import SettingsBase


class SettingsBasic(SettingsBase):
    """
    Manipulador básico de ajustes de configuración.

    Methods
    -------
    dump(file: TextIOWrapper) -> None
        Guarda los ajustes de configuración en un archivo.
    load(settings_path: str) -> SettingsBasic
        Carga los ajustes de configuración desde un archivo.

    Properties
    ----------
    root : Section
        Obtiene la raíz de los ajustes de configuración.
    """

    def dump(self, file: TextIOWrapper) -> None:
        """
        Guarda los ajustes de configuración en un archivo.

        Parameters
        ----------
        file : TextIOWrapper
            El archivo de ajustes de configuración.

        Raises
        ------
        ConfigurationFileError
            Si no se pudieron guardar los ajustes de configuración.
        """
        try:
            # Escribir los ajustes de configuración en el archivo

            json.dump(self._root.to_dict(), file, indent=4, allow_nan=False)

        except (RecursionError, TypeError, ValueError) as exc:
            raise ConfigurationFileError(
                "No se pudieron guardar los ajustes de configuración"
            ) from exc

    def load(self, file: TextIOWrapper) -> None:
        """
        Carga los ajustes de configuración desde un archivo.

        Parameters
        ----------
        file : TextIOWrapper
            El archivo de ajustes de configuración.

        Raises
        ------
        ConfigurationFileError
            Si no se pudieron cargar los ajustes de configuración.
        """
        try:
            # Cargar los ajustes de configuración en un diccionario y
            # actualizar el objeto raíz de ajustes de configuración.
            # Se asume archivo JSON

            settings: Any = json.load(file)
            self.update(settings)

        except JSONDecodeError as exc:
            raise ConfigurationFileError(
                "No se pudieron cargar los ajustes de configuración"
            ) from exc
