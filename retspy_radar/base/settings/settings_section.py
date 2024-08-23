from abc import ABC, abstractmethod

from .settings_value_adapter import Value


class SettingsSection(ABC):
    """
    Sección de ajustes de configuración.

    Clase abstracta que representa una sección de ajustes de
    configuración y permite obtener subsecciones y valores de
    ajustes de configuración.

    Methods
    -------
    has(key: str) -> bool
        Indica si la sección de ajustes de configuración contiene
        una subsección o valor con la clave especificada.
    section(key: str) -> Section
        Obtiene una subsección de ajustes de configuración.
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
    def section(self, key: str) -> "SettingsSection":
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
        """
