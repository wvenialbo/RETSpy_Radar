from abc import ABC, abstractmethod
from typing import Any

from .settings_value_adapter import Value


class SettingsSection(ABC):
    """
    Sección de ajustes de configuración.

    Clase abstracta que representa una sección de ajustes de
    configuración y permite obtener subsecciones y valores de
    ajustes de configuración.

    Methods
    -------
    add_subsection(key: str, section: Section | dict[str, Any]) -> None
        Agrega una subsección a la sección de ajustes de configuración.
    add_value(key: str, value: Value | Any) -> None
        Agrega un valor a la sección de ajustes de configuración.
    create_subsection(key: str) -> None
        Agrega una subsección a la sección de ajustes de configuración.
    has(key: str) -> bool
        Indica si la sección de ajustes de configuración contiene
        una subsección o valor con la clave especificada.
    is_empty() -> bool
        Indica si la sección de ajustes de configuración está vacía.
    section(key: str) -> Section
        Obtiene una subsección de ajustes de configuración.
    to_dict() -> dict[str, Any]
        Obtiene la sección de ajustes como un diccionario.
    update(section: Section | dict[str, Any]) -> None
        Actualiza la sección de ajustes de configuración.
    value(key: str) -> Value
        Obtiene un valor de ajuste de configuración.
    """

    def __bool__(self) -> bool:
        """
        Indica si la sección de ajustes de configuración no está vacía.

        Returns
        -------
        bool
            True si la sección de ajustes de configuración no está
            vacía, False en caso contrario.
        """
        return not self.is_empty()

    @abstractmethod
    def add_subsection(
        self, key: str, section: "_Section | dict[str, Any]"
    ) -> None:
        """
        Agrega una subsección a la sección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave de la subsección.
        section : SettingsSection | dict[str, Any]
            La subsección de ajustes de configuración.

        Raises
        ------
        KeyError
            Si la clave ya existe en la sección.
        ValueError
            Si la sección de ajustes de configuración no es válida o
            contiene valores de ajuste de configuración no válidos.
        """

    @abstractmethod
    def add_value(self, key: str, value: Value | Any) -> None:
        """
        Agrega un valor a la sección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave del valor.
        value : Value | Any
            El valor de ajuste de configuración.

        Raises
        ------
        KeyError
            Si la clave ya existe en la sección.
        ValueError
            Si el valor de ajuste de configuración es inválido.
        """

    @abstractmethod
    def create_subsection(self, key: str) -> None:
        """
        Agrega una subsección a la sección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave de la subsección.

        Raises
        ------
        KeyError
            Si la clave ya existe en la sección.
        """

    @abstractmethod
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

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Indica si la sección de ajustes de configuración está vacía.

        Returns
        -------
        bool
            True si la sección de ajustes de configuración está vacía,
            False en caso contrario.
        """

    @abstractmethod
    def section(self, key: str, copy: bool = False) -> "_Section":
        """
        Obtiene una subsección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave de la subsección de ajustes de configuración.
        copy : bool, optional
            Indica si se debe devolver una copia de la subsección.
            Por defecto es `False`.

        Returns
        -------
        Section
            La subsección de ajustes de configuración.

        Raises
        ------
        KeyError
            Si la clave no existe en la sección.
        TypeError
            Si la clave no corresponde a una sección de ajustes de
            configuración.
        """

    @abstractmethod
    def to_dict(self, copy: bool = False) -> dict[str, Any]:
        """
        Obtiene la sección de ajustes como un diccionario.

        Convierte la sección de ajustes de configuración en un
        diccionario.

        Parameters
        ----------
        copy : bool, optional
            Indica si se debe devolver una copia de la subsección.
            Por defecto es `False`.

        Returns
        -------
        dict[str, Any]
            La sección de ajustes de configuración como un diccionario.
        """

    @abstractmethod
    def update(self, section: "_Section | dict[str, Any]") -> None:
        """
        Actualiza la sección de ajustes de configuración.

        Parameters
        ----------
        section : SettingsSection | dict[str, Any]
            Un diccionario con los ajustes de configuración.

        Raises
        ------
        ValueError
            Si la sección de ajustes de configuración no es válida o
            contiene valores de ajuste de configuración no válidos.
        TypeError
            Si el objeto no corresponde a una sección de ajustes de
            configuración.
        """

    @abstractmethod
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

        Raises
        ------
        KeyError
            Si la clave no existe en la sección.
        TypeError
            Si la clave no corresponde a un valor de ajuste de
            configuración.
        """


_Section = SettingsSection
