from abc import ABC, abstractmethod
from typing import Any


class SettingsSection(ABC):
    """
    Sección de ajustes de configuración.

    Representa una sección de ajustes de configuración y permite obtener
    valores de ajustes de la misma.

    Methods
    -------
    __bool__() -> bool
        Indica si la sección de ajustes de configuración no está vacía.
    __getitem__(key: str) -> SettingsSection
        Obtiene un valor o una subsección de ajustes de configuración.
    has(key: str) -> bool
        Verifica que exista un valor con la clave especificada.
    to_dict() -> dict[str, Any]
        Obtiene la sección de ajustes como un diccionario.
    update(data: dict[str, Any]) -> None
        Actualiza la sección de ajustes de configuración.
    """

    @abstractmethod
    def __bool__(self) -> bool:
        """
        Indica si la sección de ajustes de configuración no está vacía.

        Returns
        -------
        bool
            `True` si la sección de ajustes de configuración no está
            vacía, `False` en caso contrario.
        """

    @abstractmethod
    def __getitem__(self, key: str) -> "SettingsSection":
        """
        Obtiene un valor o una subsección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave de la subsección o valor de ajustes de
            configuración.

        Returns
        -------
        SettingsSection
            El valor o subsección de ajustes de configuración.

        Raises
        ------
        KeyError
            Si la clave no existe en la sección.
        TypeError
            Si el objeto no corresponde a una subsección de ajustes de
            configuración.
        ValueError
            Si la sección de ajustes de configuración no es válida o
            contiene valores de ajuste de configuración no válidos.
        """

    @abstractmethod
    def has(self, key: str) -> bool:
        """
        Verifica que exista un valor con la clave especificada.

        Indica si la sección de ajustes de configuración contiene un
        valor o subsección con la clave especificada.

        Parameters
        ----------
        key : str
            La clave de la subsección o valor.

        Returns
        -------
        bool
            `True` si la sección de ajustes de configuración contiene
            una subsección o valor con la clave especificada, `False`
            en caso contrario.
        """

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """
        Obtiene la sección de ajustes como un diccionario.

        Devuelve una referencia al diccionario de la sección de ajustes
        de configuración.

        Returns
        -------
        dict[str, Any]
            La sección de ajustes de configuración como un diccionario.
        """

    @abstractmethod
    def update(self, data: Any) -> None:
        """
        Actualiza la sección de ajustes de configuración.

        Parameters
        ----------
        data : Any
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
