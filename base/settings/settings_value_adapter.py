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
        self._value: Any = value

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


Value = SettingsValueAdapter
