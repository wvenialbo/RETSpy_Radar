import json
from typing import Any, Type, TypeVar

T = TypeVar("T")


class SettingsValueAdapter:
    """
    Adaptador de valores de ajustes de configuración.

    Clase que envuelve un valor de ajuste de configuración y permite
    convertirlo a un tipo específico.

    Attributes
    ----------
    _value : Any
        El valor de ajuste de configuración.

    Methods
    -------
    as_type(type_: Type[T]) -> T
        Convierte el valor de ajuste de configuración a un tipo
        específico.
    """

    def __init__(self, value: Any) -> None:
        """
        Inicializa el adaptador de valores de ajustes de configuración.

        Parameters
        ----------
        value : Any
            El valor de ajuste de configuración.
        """
        self._value: Any = self._get_valid_value(value)

    def __bool__(self) -> bool:
        """
        Indica si el valor de ajuste de configuración no está vacío.

        Returns
        -------
        bool
            `True` si el valor de ajuste de configuración no está
            vacío, `False` en caso contrario.
        """
        return bool(self._value)

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
        return str(self._value)

    def as_raw(self) -> Any:
        """
        Obtiene el valor de ajuste de configuración sin convertir.

        Returns
        -------
        Any
            El valor de ajuste de configuración sin convertir.
        """
        return self._value

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
            return type_(self._value)  # type: ignore

        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"No se pudo convertir el valor a {type_.__name__}: {exc}"
            ) from exc

    @staticmethod
    def _get_valid_value(value: Any) -> Any:
        """
        Obtiene un valor de ajuste de configuración válido.

        Parameters
        ----------
        value : Any
            El valor de ajuste de configuración a validar.

        Returns
        -------
        Any
            El valor de ajuste de configuración validado.

        Raises
        ------
        ValueError
            Si el valor de ajuste de configuración no es válido.
        """
        # No permitir valores de tipo diccionario; los diccionarios
        # representan secciones de ajustes de configuración.

        if isinstance(value, dict):
            raise ValueError(
                "El valor de ajuste de configuración "
                "no puede ser un diccionario"
            )

        # No permitir valores `None`; los valores vacíos deben ser
        # explícitos.

        if value is None:
            raise ValueError(
                "El valor de ajuste de configuración no puede ser nulo"
            )

        # Validar el valor de ajuste de configuración antes de
        # asimilarlo.

        try:
            dummy_section: dict[str, Any] = {"dummy_value": value}

            assert json.dumps(dummy_section)

        except TypeError as exc:
            raise ValueError(
                "El valor de ajuste de configuración no es válido"
            ) from exc

        return value


Value = SettingsValueAdapter
