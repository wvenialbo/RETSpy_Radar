import json
from typing import Any

from .settings_section import SettingsSection
from .settings_value_adapter import Value


class SettingsSectionAdapter(SettingsSection):
    """
    Adaptador de secciones de ajustes de configuración.

    Clase que envuelve una sección de ajustes de configuración y permite
    obtener subsecciones y valores de ajustes de configuración.

    Attributes
    ----------
    _section : dict[str, Any]
        La sección de ajustes de configuración.

    Methods
    -------
    get_section(key) -> Section
        Obtiene una subsección de ajustes de configuración.
    get_value(key) -> Value
        Obtiene un valor de ajuste de configuración.
    """

    def __init__(self, section: Any) -> None:
        """
        Inicializa el adaptador de secciones de ajustes de
        configuración.

        Parameters
        ----------
        section : Any
            La sección de ajustes de configuración.
        """
        self._section: dict[str, Any] = section

    def add_subsection(
        self, key: str, section: "Section | dict[str, Any]"
    ) -> None:
        """
        Agrega una subsección a la sección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave de la subsección.
        section : Section | dict[str, Any]
            La subsección de ajustes de configuración.

        Raises
        ------
        ValueError
            Si la clave ya existe en la sección.
        """
        # Crear una nueva sección si la clave no existe, de lo contrario
        # lanzar una excepción.

        if key in self._section:
            raise ValueError(f"La clave '{key}' ya existe en la sección.")

        try:
            if isinstance(section, dict):
                json.dumps(section)
                self._section[key] = section
            else:
                json.dumps(section.to_dict())
                self._section[key] = section.to_dict()

        except TypeError as exc:
            raise ValueError(
                "Los valores de ajuste de configuración no son válidos."
            ) from exc

    def add_value(self, key: str, value: Any) -> None:
        """
        Agrega un valor a la sección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave del valor.
        value : Value
            El valor de ajuste de configuración.

        Raises
        ------
        ValueError
            Si la clave ya existe en la sección o si el valor es un
            diccionario.
        """
        # Crear un nuevo valor si la clave no existe, de lo contrario
        # lanzar una excepción.

        if key in self._section:
            raise ValueError(f"La clave '{key}' ya existe en la sección.")

        # No permitir valores de tipo diccionario; Los diccionarios con
        # clave de tipo cadena se utilizan para representar secciones de
        # ajustes de configuración, de este modo reforzamos el uso
        # correcto de la semántica del código y la correcta sintaxis de
        # los archivos de configuración, pues los archivos JSON no
        # permiten claves que no sean de tipo cadena.

        if isinstance(value, dict):
            raise ValueError("El valor no puede ser un diccionario.")

        self._section[key] = value

    def create_subsection(self, key: str) -> None:
        """
        Agrega una subsección a la sección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave de la subsección.

        Raises
        ------
        ValueError
            Si la clave ya existe en la sección.
        """
        # Crear una nueva sección si la clave no existe, de lo contrario
        # lanzar una excepción.

        if key in self._section:
            raise ValueError(f"La clave '{key}' ya existe en la sección.")

        self._section[key] = dict()

    def has(self, key: str) -> bool:
        """
        Indica si la sección de ajustes de configuración contiene una
        subsección o valor con la clave especificada.

        Parameters
        ----------
        key : str
            La clave de la subsección o valor.

        Returns
        -------
        bool
            True si la sección de ajustes de configuración contiene una
            subsección o valor con la clave especificada, False en caso
            contrario.
        """
        return key in self._section

    def is_empty(self) -> bool:
        """
        Indica si la sección de ajustes de configuración está vacía.

        Returns
        -------
        bool
            True si la sección de ajustes de configuración está vacía,
            False en caso contrario.
        """
        return not bool(self._section)

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
        return Section(self._section[key])

    def to_dict(self) -> dict[str, Any]:
        """
        Obtiene la sección de ajustes como un diccionario.

        Convierte la sección de ajustes de configuración en un
        diccionario.

        Returns
        -------
        dict[str, Any]
            La sección de ajustes de configuración como un diccionario.
        """
        return self._section

    def update(self, section: dict[str, Any]) -> None:
        """
        Actualiza la sección de ajustes de configuración.

        Parameters
        ----------
        section : dict[str, Any]
            Un diccionario con los ajustes de configuración.

        Raises
        ------
        ValueError
            Si los valores de ajuste de configuración no son válidos
        """
        # Validar los valores de ajuste de configuración antes de
        # actualizar la sección.

        try:
            json.dumps(section)

            self._section.update(section)

        except TypeError as exc:
            raise ValueError(
                "Los valores de ajuste de configuración no son válidos."
            ) from exc

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
        return Value(self._section[key])


Section = SettingsSectionAdapter
