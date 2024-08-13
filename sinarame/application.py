from datetime import datetime, timedelta
from logging import Logger
from typing import Any

from ..base.exceptions import (
    InvalidTimeFormatError,
    InvalidTimeRangeError,
    TimeConversionError,
)
from ..base.logging import get_logger
from ..base.utils import timing
from .application_info import info
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
        self._logger: Logger = get_logger(info.name)
        self._settings: Settings = settings

    def is_parent_process(self, module_name: str) -> bool:
        """
        Verifica el modo de ejecución.

        Comprueba si el módulo que instanció la aplicación y arrancó el
        sistema es el proceso padre.

        Parameters
        ----------
        module_name : str
            El nombre del módulo que instanció la aplicación y arrancó
            el sistema.

        Returns
        -------
        bool
            `True` si el módulo es el proceso padre, `False` en caso
            contrario.
        """
        return module_name == PARENT_PROCESS

    def is_stand_alone(self, module_name: str) -> bool:
        """
        Verifica si se está ejecutando en modo independiente.

        Comprueba si el módulo que instanció la aplicación y arrancó el
        sistema es un módulo independiente.

        Parameters
        ----------
        module_name : str
            El nombre del módulo que instanció la aplicación y arrancó
            el sistema.

        Returns
        -------
        bool
            `True` si el módulo es independiente, `False` en caso contrario.
        """
        return module_name in {PARENT_PROCESS, CHILD_PROCESS}

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

        self.print_banner()

        # Verificar que la aplicación no sea importada como módulo y
        # que se ejecute como un programa independiente. Terminar la
        # ejecución si no se cumple la condición

        if not self.is_stand_alone(module_name):
            # Registrar un mensaje de error, imprimir las directivas
            # de operación y salir

            self._logger.error(
                "Se aborta la operación: la aplicación se "
                "importó desde un proceso secundario."
            )

            print(f"Ejecuta `{info.name}` desde la línea de comando.")

            return

        # Iniciar la ejecución del bot de indexación de datos

        try:
            args: dict[str, Any] = self._setup_arguments()

            robot = RobotSMN(self._settings, self._logger)

            robot.run(**args)

        # Capturar todas excepciones no manejadas específicamente y
        # registrarlas en el registro de eventos. Finalizar la
        # ejecución del sistema graciosa y ordenadamente

        except Exception as exc:
            self._logger.critical(
                f"No se puede continuar: Error inesperado: {exc}"
            )

            print("No se puede continuar: ocurrió un error inesperado.")

    def print_banner(self) -> None:
        # Imprime el banner del programa

        print(f"{info.banner}\n")

    def print_footer(self) -> None:
        # Imprime el pie de página del programa

        print(f"{info.version_full}\n")

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

        return {
            "start_time": start_time,
            "end_time": end_time,
            "scan_interval": scan_interval,
            "station_ids": self._settings.station_ids,
        }
