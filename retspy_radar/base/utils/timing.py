import re
import time
from datetime import datetime, timedelta, timezone
from math import isfinite
from re import Match

from ..exceptions import (
    InvalidTimeFormatError,
    InvalidTimeLapseError,
    TimeConversionError,
)


class timing:
    """
    Clase de utilidades para el manejo de fechas y tiempos.

    Proporciona métodos para la conversión de cadenas de fecha y hora
    y de intervalo de tiempo en objetos datetime y timedelta, así como
    para la espera hasta el inicio de una rutina.

    Methods
    -------
    get_times(from_dt, to_dt, for_td) -> tuple[datetime, datetime]
        Obtiene los tiempos de inicio y fin de ejecución de la rutina.
    wait_for(lapse_td) -> None
        Espera un intervalo de tiempo.
    wait_for_n_seconds(n_seconds) -> None
        Espera un intervalo de tiempo en segundos.
    wait_until(start_datetime) -> None
        Espera hasta el inicio de la rutina.

    Static Methods
    --------------
    parse_datetime(dt_str) -> datetime
        Convierte una cadena de fecha y hora en un objeto datetime.
    parse_timedelta(td_str) -> timedelta
        Convierte una cadena de intervalo de tiempo en un objeto
        timedelta.
    """

    UNIT_MAPPING: dict[str, float] = {
        "millisecond": 1e-3,
        "second": 1,
        "minute": 60,
        "hour": 3600,
    }

    @staticmethod
    def current_time() -> datetime:
        """
        Obtiene la fecha y hora actuales en zona horaria UTC.

        Returns
        -------
        datetime
            La fecha y hora actuales en zona horaria UTC.
        """
        return datetime.now(timezone.utc)

    @classmethod
    def to_seconds(cls, lapse: float, units: str) -> float:
        """
        Convierte un intervalo de tiempo en segundos.

        Convierte un intervalo de tiempo en segundos a partir de un
        valor numérico y una unidad de tiempo.

        Parameters
        ----------
        lapse : float
            El valor numérico del intervalo de tiempo.
        units : str
            La unidad de tiempo del intervalo de tiempo.

        Returns
        -------
        float
            El intervalo de tiempo en segundos.

        Raises
        ------
        TimeConversionError
            Si la unidad de tiempo no es válida.
        """
        if units not in cls.UNIT_MAPPING:
            raise TimeConversionError("Unidad de tiempo inválida")

        return lapse * cls.UNIT_MAPPING[units]

    @classmethod
    def wait_for(cls, lapse_timedelta: timedelta) -> None:
        """
        Espera un intervalo de tiempo.

        Parameters
        ----------
        lapse_timedelta : timedelta
            El intervalo de tiempo de espera.
        """
        n_seconds: float = lapse_timedelta.total_seconds()

        cls.wait_for_n_seconds(n_seconds)

    @staticmethod
    def wait_for_n_seconds(n_seconds: float) -> None:
        """
        Espera un intervalo de tiempo en segundos.

        Parameters
        ----------
        n_seconds : float
            El intervalo de tiempo de espera en segundos.

        Raises
        ------
        InvalidTimeLapseError
            Si el intervalo de tiempo de espera es negativo.
        """
        if n_seconds < 0 or isfinite(n_seconds) is False:
            raise InvalidTimeLapseError(
                "El intervalo de tiempo de espera "
                "debe ser un número no negativo"
            )

        time.sleep(n_seconds)

    @classmethod
    def wait_until(cls, until_datetime: datetime) -> None:
        """
        Espera hasta un tiempo determinado.

        Parameters
        ----------
        until_datetime : datetime
            La fecha y hora de inicio de la rutina.
        """
        n_seconds: float = cls._calculate_wait_time(until_datetime)

        cls.wait_for_n_seconds(n_seconds)

    @classmethod
    def _calculate_wait_time(cls, until_datetime: datetime) -> float:
        """
        Obtiene el tiempo de espera hasta el inicio de la rutina.

        Calcula el tiempo de espera hasta el inicio de la rutina
        a partir de la fecha y hora actuales.

        Parameters
        ----------
        until_datetime : datetime
            La fecha y hora de inicio de la rutina.

        Returns
        -------
        float
            El tiempo de espera hasta el inicio de la rutina en
            segundos.
        """
        # Obtener el tiempo de espera hasta el inicio de la rutina

        current_datetime: datetime = cls.current_time()
        time_difference: timedelta = until_datetime - current_datetime
        wait_time: float = time_difference.total_seconds()

        # Verificar que el tiempo de espera sea positivo

        if wait_time < 0:
            wait_time = 0

        return wait_time

    @staticmethod
    def parse_datetime(dt_str: str) -> datetime:
        """
        Convierte una cadena de fecha y hora en un objeto datetime.

        Parameters
        ----------
        dt_str : str
            La cadena de fecha y hora en formato ISO 8601.

        Returns
        -------
        datetime
            El objeto datetime correspondiente a la cadena de fecha y
            hora en zona horaria UTC.

        Raises
        ------
        InvalidTimeFormatError
            Si la cadena de fecha y hora no tiene el formato adecuado.
        TimeConversionError
            Si hay errores en la conversión de la cadena de fecha y
            hora.
        """
        if len(dt_str) not in {19, 20, 24}:
            raise InvalidTimeFormatError(
                "Formato inválido: "
                "se esperan fecha y hora en formato ISO 8601"
            )

        DATE_PATTERN: str = (
            "%Y-%m-%dT%H:%M:%S" if len(dt_str) == 19 else "%Y-%m-%dT%H:%M:%S%z"
        )

        try:
            dt: datetime = datetime.strptime(dt_str, DATE_PATTERN)

        except ValueError as exc:
            raise TimeConversionError(
                "Error al convertir la fecha y hora: "
                f"se esperan fecha y hora en formato ISO 8601: {exc}"
            ) from exc

        if not dt.tzinfo:
            dt = dt.astimezone()

        return dt.astimezone(timezone.utc)

    @staticmethod
    def parse_timedelta(td_str: str) -> timedelta:
        """
        Convierte una cadena de intervalo de tiempo en un objeto
        timedelta.

        Parameters
        ----------
        td_str : str
            La cadena de intervalo de tiempo en formato ISO 8601.

        Returns
        -------
        timedelta
            El objeto timedelta correspondiente a la cadena de intervalo
            de tiempo.

        Raises
        ------
        InvalidTimeFormatError
            Si la cadena de intervalo de tiempo no tiene el formato
            correcto.
        TimeConversionError
            Si el valor numérico en el rango de tiempo es inválido.
        """
        # Patrón para extraer los componentes de la duración
        TD_PATTERN: str = (
            r"P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?(?:(\d+)m)?"
        )

        match: Match[str] | None = re.match(TD_PATTERN, td_str)

        if not match:
            raise InvalidTimeFormatError(
                "Formato inválido:"
                "se espera intervalo de tiempo en formato ISO 8601"
            )

        days: str
        hours: str
        minutes: str
        seconds: str
        milliseconds: str

        days, hours, minutes, seconds, milliseconds = match.groups()

        try:

            td_values: dict[str, int] = {
                "days": int(days) if days else 0,
                "hours": int(hours) if hours else 0,
                "minutes": int(minutes) if minutes else 0,
                "seconds": int(seconds) if seconds else 0,
                "milliseconds": int(milliseconds) if milliseconds else 0,
            }

            return timedelta(**td_values)

        except (TypeError, ValueError) as exc:
            raise TimeConversionError(
                f"Valor numérico de intervalo de tiempo inválido: {exc}"
            ) from exc
