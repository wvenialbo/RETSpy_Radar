from typing import Any

from .settings_section import SettingsSection
from .settings_value import SettingsValue


class SettingsBase(SettingsSection):
    """
    Ajustes de configuración almacenados en archivos JSON.

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

    Attributes
    ----------
    root : SettingsValue
        La raíz de los ajustes de configuración.
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
        settings: dict[str, Any] = data or dict()
        self._root = SettingsValue(settings)

    def __bool__(self) -> bool:
        """
        Indica si la sección de ajustes de configuración no está vacía.

        Returns
        -------
        bool
            `True` si la sección de ajustes de configuración no está
            vacía, `False` en caso contrario.
        """
        return bool(self._root)

    def __getitem__(self, key: str) -> "SettingsValue":
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
        return self._root[key]

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
        return self._root.to_dict()

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
        return self._root.update(data)

    @property
    def root(self) -> "SettingsValue":
        """
        La raíz de los ajustes de configuración.

        Returns
        -------
        Section
            La raíz de los ajustes de configuración.
        """
        return self._root
