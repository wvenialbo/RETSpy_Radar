from datetime import datetime, timedelta
from logging import Logger
from typing import Any

from ..base.exceptions import (
    InvalidTimeFormatError,
    InvalidTimeRangeError,
    TimeConversionError,
)
from ..base.logging import get_logger
from ..base.utils import console, timing
from .application_info import pkg_info
from .robot_smn import RobotSMN
from .settings_smn import SettingsSMN as Settings

PARENT_PROCESS = "__main__"
CHILD_PROCESS = "__mp_main__"


class Application:
    def __init__(self, settings: Settings) -> None:
        """
        Inicializa la aplicación.

        Parameters
        ----------
        settings : Settings
            Los ajustes de configuración de la aplicación.
        logger : Logger
            El registro de eventos de la aplicación.
        """
        self._logger: Logger = get_logger(pkg_info.name)
        self._settings: Settings = settings

    def run(self, module_name: str) -> None:
        """
        Inicia la ejecución de la aplicación.

        Parameters
        ----------
        module_name : str
            El nombre del módulo que instanció la aplicación y
            arrancó el sistema.
        """
        # Mostrar el banner del programa

        self._print_banner()

        # Iniciar la ejecución del bot de indexación de datos

        # Capturar las excepciones específicas y registrarlas en el
        # registro de eventos. Finalizar la ejecución del sistema
        # graciosa y ordenadamente
        # --------------------------------------------------------------

        args: dict[str, Any] = self._setup_arguments()

        robot = RobotSMN(self._settings, self._logger)

        self._print_summary(args)

        while True:
            try:

                robot.run(**args)

                break

            except KeyboardInterrupt as exc:
                terminate: str = console.prompt(
                    "¿Desea salir del programa?", console.YES_NO
                )

                if console.response_is(terminate, console.YES):
                    raise exc

        # --------------------------------------------------------------

        self._print_footer()

    def _print_banner(self) -> None:
        # Imprime el banner del programa

        print(f"{pkg_info.banner}\n")

    def _print_footer(self) -> None:
        # Imprime el pie de página del programa

        print(f"{pkg_info.version_full}\n")

    def _print_summary(self, args: dict[str, Any]) -> None:
        # Imprime el resumen de la ejecución del programa

        start_time: datetime = args["start_time"]
        end_time: datetime = args["end_time"]
        scan_interval: timedelta = args["scan_interval"]
        station_ids: list[str] = args["station_ids"]

        begin: str = start_time.strftime("%Y-%m-%dT%H:%M:%S%z")
        end: str = end_time.strftime("%Y-%m-%dT%H:%M:%S%z")

        print("Resumen de la ejecución")
        print("----------------------")
        print(f"  - Fecha de inicio         : {begin}")
        print(f"  - Fecha de finalización   : {end}")
        print(f"  - Intervalo de escaneo    : {scan_interval}")
        print(f"  - Estaciones a monitorear : {', '.join(station_ids)}\n")

        stations: dict[str, dict[str, Any]] = self._settings.section(
            "stations"
        ).to_dict()

        for station_id in station_ids:
            if station_id in stations:
                station: dict[str, Any] = stations[station_id]
                print(f"Estación {station_id}: {station['name']}")
                print(f"  - Latitud  : {station['lat']:+02.14f}")
                print(f"  - Longitud : {station['lon']:+02.14f}\n")

    def _setup_arguments(self) -> dict[str, Any]:
        """
        Configura los argumentos de la aplicación.

        Configura los argumentos de la aplicación para la ejecución del
        proceso de recolección de datos.

        Returns
        -------
        dict[str, Any]
            Los argumentos de la aplicación.
        """
        # Fijar valores predeterminados para los parámetros de fecha y
        # hora si no se especificaron
        start_time: datetime
        end_time: datetime
        scan_period: timedelta

        # Obtener el tiempo de ejecución de la rutina; si no se
        # especifica se ejecutará la rutina por 24 horas

        if self._settings.scan_period:
            try:
                scan_period = timing.parse_timedelta(
                    self._settings.scan_period
                )

            except (InvalidTimeFormatError, TimeConversionError) as exc:
                raise TimeConversionError(
                    f"Error al leer el rango de tiempo: {exc}"
                ) from exc
        else:
            scan_period = timedelta(hours=24)

        # Obtener la fecha de inicio de ejecución de la rutina; si no
        # se especifica, se ejecutará la rutina desde el momento de la
        # llamada

        if self._settings.start_time:
            try:
                start_time = timing.parse_datetime(self._settings.start_time)

            except (InvalidTimeFormatError, TimeConversionError) as exc:
                raise TimeConversionError(
                    f"Error al leer la fecha inicial: {exc}"
                ) from exc
        else:
            start_time = timing.current_time()

        # Obtener la fecha de finalización de ejecución de la rutina; si
        # no se especifica se calcula sumando el tiempo de ejecución a
        # la fecha de inicio

        if self._settings.end_time:
            try:
                end_time = timing.parse_datetime(self._settings.end_time)

            except (InvalidTimeFormatError, TimeConversionError) as exc:
                raise TimeConversionError(
                    f"Error al leer la fecha final: {exc}"
                ) from exc
        else:
            end_time = start_time + scan_period

        # Validación de rango de fechas

        if start_time >= end_time:
            raise InvalidTimeRangeError(
                "La fecha de finalización debe ser posterior "
                "a la fecha de inicio"
            )

        scan_interval = timedelta(seconds=self._settings.scan_interval)

        station_ids: list[str] = list()

        stations: dict[str, Any] = self._settings.section("stations").to_dict()
        groups: dict[str, list[str]] = self._settings.value(
            "station_groups"
        ).as_type(dict[str, list[str]])

        for station_id in self._settings.station_ids:
            if station_id in stations:
                station_ids.append(station_id)
            elif station_id in groups:
                station_ids.extend(groups[station_id])
            else:
                station_ids.append(station_id)
                self._logger.warning(
                    f"La estación '{station_id}' no está definida en la "
                    "configuración de la aplicación."
                )

        return {
            "start_time": start_time,
            "end_time": end_time,
            "scan_interval": scan_interval,
            "station_ids": station_ids,
        }
