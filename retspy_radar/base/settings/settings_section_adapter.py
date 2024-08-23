import json
from typing import Any, cast

from .settings_section import SettingsSection
from .settings_section import SettingsSection as _Section
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

    def __init__(self, section: "Section | dict[str, Any]") -> None:
        """
        Inicializa el adaptador de secciones de ajustes de
        configuración.

        Parameters
        ----------
        section : SettingsSectionAdapter | dict[str, Any]
            La sección de ajustes de configuración.

        Raises
        ------
        ValueError
            Si la sección de ajustes de configuración no es válida o
            contiene valores de ajuste de configuración no válidos.
        TypeError
            Si el objeto no corresponde a una sección de ajustes de
            configuración.
        """
        # Asimilar la sección cuando el argumento corresponde a un tipo
        # de sección de ajustes de configuración compatible.

        self._section: dict[str, Any] = self._get_valid_section(section, True)

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
        # Crear una nueva sección si la clave no existe, de lo contrario
        # lanzar una excepción.

        self._raise_for_key(key)

        # Asimilar la sección cuando el argumento corresponde a un tipo
        # de sección de ajustes de configuración compatible.

        self._section[key] = self._get_valid_section(section, True)

    def add_value(self, key: str, value: Any) -> None:
        """
        Agrega un valor a la sección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave del valor.
        value : Any
            El valor de ajuste de configuración.

        Raises
        ------
        KeyError
            Si la clave ya existe en la sección.
        ValueError
            Si el valor de ajuste de configuración es inválido.
        """
        # Crear un nuevo valor si la clave no existe, de lo contrario
        # lanzar una excepción.

        self._raise_for_key(key)

        # Si el valor no es una instancia de `Value`, se convierte a una
        # instancia de `Value` para asimilarla.

        if not isinstance(value, Value):
            value = Value(value)

        # Si el valor es una instancia de Value, se asimila su valor
        # crudo directamente.

        self._section[key] = value.as_raw()

    def create_subsection(self, key: str) -> None:
        """
        Crea una subsección de ajustes de configuración vacía.

        Parameters
        ----------
        key : str
            La clave de la subsección.

        Raises
        ------
        KeyError
            Si la clave ya existe en la sección.
        """
        # Crear una nueva sección vacía si la clave no existe, de lo
        # contrario lanzar una excepción.

        self._raise_for_key(key)

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

    def section(self, key: str, copy: bool = False) -> "Section":
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
        # Devolver una nueva sección si la clave existe, de lo contrario
        # lanzar una excepción.

        self._raise_for_no_key(key)

        # Lanzar una excepción si la clave no corresponde a una sección.

        if not isinstance(self._section[key], dict):
            raise TypeError(f"La clave '{key}' no corresponde a una sección")

        # Devolver una nueva sección con la subsección de ajustes de
        # configuración.

        section: dict[str, Any] = self._section[key]

        return Section(section.copy() if copy else section)

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
        return self._section.copy() if copy else self._section

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
        # Actualizar la sección cuando el argumento corresponde a un
        # tipo de sección de ajustes de configuración compatible.

        section = self._get_valid_section(section, False)

        self._section.update(section)

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
        # Devolver un nuevo valor si la clave existe, de lo contrario
        # lanzar una excepción.

        self._raise_for_no_key(key)

        # Lanzar una excepción si la clave no corresponde a un valor.

        if isinstance(self._section[key], dict):
            raise TypeError(f"La clave '{key}' no corresponde a un valor")

        # Devolver un nuevo `Value` con el valor de ajuste de
        # configuración.

        return Value(self._section[key])

    @staticmethod
    def _get_valid_section(section: Any, copy: bool) -> dict[str, Any]:
        """
        Obtiene una sección de ajustes de configuración válida.

        Parameters
        ----------
        section : Any
            La sección de ajustes de configuración a validar.
        copy : bool
            Indica si se debe devolver una copia de la sección.

        Returns
        -------
        dict[str, Any]
            La sección de ajustes de configuración validada.

        Raises
        ------
        ValueError
            Si la sección de ajustes de configuración no es válida o
            contiene valores de ajuste de configuración no válidos.
        TypeError
            Si el objeto no corresponde a una sección de ajustes de
            configuración.
        """
        # Si el argumento es una sección, su contenido se asume como
        # válido, se convierte a un diccionario y se asimila una copia
        # de este.

        if isinstance(section, _Section):
            return section.to_dict().copy() if copy else section.to_dict()

        # Lanzar una excepción si el objeto no corresponde a un tipo de
        # sección de ajustes de configuración compatible.

        if not isinstance(section, dict):
            raise TypeError(
                "El objeto no corresponde a una "
                "sección de ajustes de configuración"
            )

        # Validar los valores de ajuste de configuración antes de
        # asimilar la sección cuando el argumento es un diccionario:

        try:
            assert json.dumps(section)

        except TypeError as exc:
            raise ValueError(
                "Los valores de ajuste de configuración no son válidos"
            ) from exc

        # Una sección de valores de ajuste de configuración válida debe
        # ser un diccionario serializable a JSON.

        return cast(dict[str, Any], section)

    def _raise_for_key(self, key: str) -> None:
        """
        Lanza una excepción si la clave ya existe en la sección.

        Parameters
        ----------
        key : str
            La clave de la subsección o valor.

        Raises
        ------
        KeyError
            Si la clave ya existe en la sección.
        """
        if self.has(key):
            raise KeyError(f"La clave '{key}' ya existe en la sección")

    def _raise_for_no_key(self, key: str) -> None:
        """
        Lanza una excepción si la clave no existe en la sección.

        Parameters
        ----------
        key : str
            La clave de la subsección o valor.

        Raises
        ------
        KeyError
            Si la clave no existe en la sección.
        """
        if not self.has(key):
            raise KeyError(f"La clave '{key}' no existe en la sección")


Section = SettingsSectionAdapter
