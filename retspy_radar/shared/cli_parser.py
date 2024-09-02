from argparse import SUPPRESS, ArgumentParser
from argparse import _ArgumentGroup as ArgumentGroup_  # type: ignore
from argparse import _MutuallyExclusiveGroup as MutexGroup_  # type: ignore
from argparse import _SubParsersAction as SubParsersAction_  # type: ignore
from typing import Any

ArgumentGroup = ArgumentGroup_
MutuallyExclusiveGroup = MutexGroup_


class CustomArgumentParser(ArgumentParser):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._positionals.title = "Argumentos posicionales"
        self._optionals.title = "Argumentos opcionales"


type SubParsersAction = SubParsersAction_[CustomArgumentParser]


class CLIParserBase:

    # Meta variables del intérprete de linea de comandos

    DIRECTORY_PATH: str = "DIRECTORY_PATH"
    FILE_PATH: str = "FILE_PATH"
    INTEGER_NUMBER: str = "INTEGER_NUMBER"
    ISO_DATE_TIME: str = "ISO_DATE_TIME"
    ISO_TIME_PERIOD: str = "ISO_TIME_PERIOD"
    ID_STRING: str = "ID_STRING"

    # Constantes de la aplicación

    DEFAULT_REPO_PATH: str = "./"
    DEFAULT_PERIOD_TIME: str = "PT24H"
    DEFAULT_PERIOD_STR: str = "24 horas"

    @classmethod
    def setup_parser_common(
        cls, parser: ArgumentParser, version: str
    ) -> ArgumentGroup:
        common: ArgumentGroup = parser.add_argument_group(
            title="Opciones de programa",
            # description="Opciones generales del programa.",
        )

        common.add_argument(
            "-h",
            "--help",
            action="help",
            default=SUPPRESS,
            help="Muestra este mensaje de ayuda y termina.",
        )

        if version:
            common.add_argument(
                "-v",
                "--version",
                action="version",
                version=version,
                help="Muestra la versión del programa y termina.",
            )

        return common

    @classmethod
    def setup_parser_shared(cls, parser: ArgumentParser, version: str) -> None:
        common: ArgumentGroup = cls.setup_parser_common(parser, version)

        verbosity: MutuallyExclusiveGroup = (
            common.add_mutually_exclusive_group()
        )

        verbosity.add_argument(
            "-D",
            "--debug",
            action="store_const",
            dest="verbosity",
            const="debug",
            help="Muestra todos los mensajes de depuración.",
        )

        verbosity.add_argument(
            "-Q",
            "--quiet",
            action="store_const",
            dest="verbosity",
            const="quiet",
            help="Muestra solamente los mensajes de error. (Por defecto)",
            default="quiet",
        )

        verbosity.add_argument(
            "-S",
            "--silent",
            action="store_const",
            dest="verbosity",
            const="silent",
            help="No muestra ningún mensaje.",
        )

        verbosity.add_argument(
            "-V",
            "--verbose",
            action="store_const",
            dest="verbosity",
            const="verbose",
            help="Muestra los mensajes de información y de advertencia.",
        )

    @classmethod
    def setup_parser_config(cls, parser: ArgumentParser) -> None:
        config: ArgumentGroup = parser.add_argument_group(
            title="Opciones de configuración",
            # description="Opciones de archivo y configuración.",
        )

        config.add_argument(
            "-c",
            "--config-path",
            dest="config_path",
            metavar=cls.FILE_PATH,
            type=str,
            help="Ruta del archivo de configuración del indexador. "
            "Si se especifica este argumento, se ignora el archivo "
            "de configuración del usuario en la carpeta de trabajo.",
            default=None,
        )

        config.add_argument(
            "-o",
            "--output-path",
            dest="output_path",
            metavar=cls.DIRECTORY_PATH,
            type=str,
            help="Ruta del directorio del repositorio local, por "
            "defecto es la carpeta de trabajo actual desde donde "
            "se ejecuta el script.",
            default=cls.DEFAULT_REPO_PATH,
        )

    @classmethod
    def setup_parser_monitor(
        cls, parser: ArgumentParser, stations: list[str], hide_stations: bool
    ) -> None:
        monitor: ArgumentGroup = parser.add_argument_group(
            title="Opciones de monitoreo",
            # description="Opciones de monitoreo de imágenes de radar.",
        )

        monitor.add_argument(
            "-s",
            "--start-time",
            dest="start_time",
            metavar=cls.ISO_DATE_TIME,
            type=str,
            help="Fecha y hora de inicio de la descarga de imágenes "
            "de radar en formato ISO 8601, por ejemplo: "
            "'2024-01-01T00:00:00', '2024-01-01T00:00:00-0300' "
            "o '2024-01-01T00:00:00Z'. Por defecto son la fecha "
            "y hora actuales.",
            default=None,
        )

        monitor.add_argument(
            "-e",
            "--end-time",
            dest="end_time",
            metavar=cls.ISO_DATE_TIME,
            type=str,
            help="Fecha y hora de fin de la descarga de imágenes de "
            "radar, en formato ISO 8601, por ejemplo: "
            "'2024-01-01T00:00:00', '2024-01-01T00:00:00-0300' "
            "o '2024-01-01T00:00:00Z'. Por defecto la descarga "
            f"termina {cls.DEFAULT_PERIOD_STR} después de la fecha "
            "de inicio. Tiene precedencia sobre el argumento "
            "-p/--scan-period.",
            default=None,
        )

        monitor.add_argument(
            "-p",
            "--scan-period",
            dest="scan_period",
            metavar=cls.ISO_TIME_PERIOD,
            type=str,
            help="Duración de la ventana de tiempo de monitorización "
            "de imágenes de radar, en formato ISO 8601, por ejemplo: "
            "'P1M' para 1 mes, 'PT10M' para 10 minutos, 'PT1H30M' "
            "para 1 hora y 30 minutos, etc. Por defecto es de "
            f"{cls.DEFAULT_PERIOD_STR} ('{cls.DEFAULT_PERIOD_TIME}'). "
            "Si se especifica el argumento -e/--end-time, este "
            "parámetro se ignora.",
            default=cls.DEFAULT_PERIOD_TIME,
        )

        if stations:
            help = (
                SUPPRESS
                if hide_stations
                else (
                    "Lista de identificadores de estaciones o grupos "
                    "de estaciones de radar a monitorear. Por defecto "
                    f"tiene el valor: '{stations[0]}'."
                )
            )
            monitor.add_argument(
                "-i",
                "--station-ids",
                dest="station_ids",
                metavar=cls.ID_STRING,
                nargs="+",
                type=set[str],
                help=help,
                default=stations,
            )
