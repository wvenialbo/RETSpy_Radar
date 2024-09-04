from typing import Any, Type, TypeVar, cast

from .settings_section import SettingsSection

T = TypeVar("T")


class SettingsValue(SettingsSection):
    """
    Adaptador de valores de ajustes de configuración.

    Envuelve un valor o sección de ajuste de configuración y permite
    obtener valores y subsecciones de ajustes de configuración.

    Methods
    -------
    __bool__() -> bool
        Indica si el valor de ajuste de configuración no es nulo.
    __format__(format_spec: str) -> str
        Retorna una representación formateada del valor de ajuste de
        configuración.
    __getitem__(key: str) -> SettingsSection
        Obtiene un valor o una subsección de ajustes de configuración.
    __str__() -> str
        Retorna una representación en cadena del valor de ajuste de
        configuración.
    as_raw() -> Any
        Obtiene el valor de ajuste de configuración sin convertir.
    as_type(type_: Type[T]) -> T
        Convierte el valor de ajuste de configuración a un tipo
        específico.
    has(key: str) -> bool
        Si el objeto es a una sección de ajustes de configuración,
        verifica que exista un valor con la clave especificada.
    to_dict() -> dict[str, Any]
        Si el objeto es a una sección de ajustes de configuración,
        devuelve la sección de ajustes como un diccionario.
    update(data: dict[str, Any]) -> None
        Si el objeto es a una sección de ajustes de configuración,
        actualiza la sección de ajustes de configuración.
    """

    def __init__(self, data: Any) -> None:
        """
        Inicializa el adaptador de valores de ajustes de configuración.

        Parameters
        ----------
        data : Any
            El valor de ajuste de configuración.
        """
        self._data: Any = data

    def __bool__(self) -> bool:
        """
        Indica si el valor de ajuste de configuración no es nulo.

        Permite evaluar el valor en un contexto booleano. Se espera que
        el valor sea nulificable; se considera que un valor es un nulo
        si su valor es `None` o es un contenedor vacío.

        El método intenta convertir el valor asociado a un `bool`. Si la
        conversión es exitosa, retorna el resultado de la misma. Algunos
        valores numéricos se consideran nulos, a saber: `False`, `0.0`,
        y `0`; se debe tener cuidado al evaluar estos valores.

        Returns
        -------
        bool
            `True` si el valor de ajuste de configuración no es nulo,
            `False` en caso contrario.
        """
        return bool(self._data)

    def __format__(self, format_spec: str) -> str:
        """
        Retorna una representación formateada del valor de ajuste de
        configuración.

        Parameters
        ----------
        format_spec : str
            La especificación de formato a aplicar al valor de ajuste de
            configuración.

        Returns
        -------
        str
            La representación formateada del valor de ajuste de
            configuración.
        """
        return format(self._data, format_spec)

    def __getitem__(self, key: str) -> "SettingsValue":
        """
        Obtiene un valor o una subsección de ajustes de configuración.

        Parameters
        ----------
        key : str
            La clave de la subsección de ajustes de configuración.

        Returns
        -------
        Section
            La subsección de ajustes de configuración.

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
        # Devolver una nueva sección si la clave existe, de lo contrario
        # lanzar una excepción.

        section: dict[str, Any] = self.to_dict()

        if key not in section:
            raise KeyError(f"La clave '{key}' no existe en la sección")

        # Devolver una nueva adaptador con la subsección de ajustes de
        # configuración.

        return SettingsValue(section[key])

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, dict):
            subsection: SettingsValue = self[key]
            subsection.update(value)
        else:
            self._get_valid_value(self[key].as_raw())
            section: dict[str, Any] = self.to_dict()
            section[key] = self._get_valid_value(value)

    def __str__(self) -> str:
        """
        Retorna una representación en cadena del valor de ajuste de
        configuración.

        Returns
        -------
        str
            La representación en cadena del valor de ajuste de
            configuración.
        """
        return str(self._data)

    def as_raw(self) -> Any:
        """
        Obtiene el valor de ajuste de configuración sin convertir.

        Returns
        -------
        Any
            El valor de ajuste de configuración sin convertir.
        """
        return self._data

    def as_type(self, type_: Type[T]) -> T:
        """
        Convierte el valor de ajuste de configuración a un tipo específico.

        Parameters
        ----------
        type_ : Type[T]
            El tipo al que se desea convertir el valor de ajuste de
            configuración.

        Returns
        -------
        T
            El valor de ajuste de configuración convertido al tipo
            específico.

        Raises
        ------
        ValueError
            Si no se pudo convertir el valor de ajuste de configuración
            al tipo específico.
        """
        try:
            value: Any = self._get_valid_value(self._data)

            return type_(value)  # type: ignore

        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"No se pudo convertir el valor a {type_.__name__}: {exc}"
            ) from exc

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

        Raises
        ------
        TypeError
            Si el objeto no corresponde a una subsección de ajustes de
            configuración.
        ValueError
            Si la sección de ajustes de configuración no es válida o
            contiene valores de ajuste de configuración no válidos.
        """
        return key in self.to_dict()

    def to_dict(self) -> dict[str, Any]:
        """
        Obtiene la sección de ajustes como un diccionario.

        Si el objeto es a una sección de ajustes de configuración,
        devuelve una referencia al diccionario de la sección de ajustes
        de configuración.

        Returns
        -------
        dict[str, Any]
            La sección de ajustes de configuración como un diccionario.

        Raises
        ------
        TypeError
            Si el objeto no corresponde a una subsección de ajustes de
            configuración.
        """
        return self._get_valid_section(self._data)

    def update(self, data: Any) -> None:
        """
        Actualiza la sección de ajustes de configuración.

        Si el objeto es a una sección de ajustes de configuración,
        actualiza la sección de ajustes de configuración.

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
        root: dict[str, Any] = self.to_dict()

        if isinstance(data, SettingsSection):
            section: dict[str, Any] = data.to_dict()
        else:
            section = self._get_valid_section(data)

        # Asimilar la sección cuando el argumento es un diccionario.

        root.update(section)

    @staticmethod
    def _get_valid_section(section: Any) -> dict[str, Any]:
        """
        Obtiene una sección de ajustes de configuración válida.

        Parameters
        ----------
        section : Any
            La section de ajustes de configuración a validar.

        Returns
        -------
        dict[str, Any]
            La sección de ajustes de configuración validada.

        Raises
        ------
        TypeError
            Si el objeto no corresponde a una sección de ajustes de
            configuración.
        """
        # Lanzar una excepción si el objeto no corresponde a un tipo de
        # sección de ajustes de configuración compatible.

        if not isinstance(section, dict):
            raise TypeError(
                "El objeto no corresponde a una "
                "sección de ajustes de configuración"
            )

        return cast(dict[str, Any], section)

    @staticmethod
    def _get_valid_value(value: Any) -> Any:
        """
        Obtiene un valor de ajuste de configuración válido.

        Parameters
        ----------
        value : Any
            El valor de ajuste de configuración a validar.
        validate_json : bool
            Indica si se debe validar la serialización JSON.

        Returns
        -------
        Any
            El valor de ajuste de configuración validado.

        Raises
        ------
        ValueError
            Si el valor de ajuste de configuración no es válido.
        TypeError
            Si el objeto no corresponde a un valor de ajustes de
            configuración.
        """
        # No permitir valores de tipo diccionario; los diccionarios
        # representan secciones de ajustes de configuración.

        if isinstance(value, dict):
            raise TypeError(
                "El valor de ajuste de configuración "
                "no puede ser un diccionario"
            )

        # No permitir valores `None`; los valores vacíos deben ser
        # explícitos.

        if value is None:
            raise ValueError(
                "El valor de ajuste de configuración no puede ser nulo"
            )

        return value
