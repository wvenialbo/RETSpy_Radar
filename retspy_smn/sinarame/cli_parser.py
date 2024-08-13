from argparse import SUPPRESS, ArgumentParser, Namespace
from typing import Any, Sequence

from .application_info import info


class CustomArgumentParser(ArgumentParser):

    # Constantes de la aplicación

    DEFAULT_REPO_PATH: str = "./"
    DEFAULT_PERIOD_TIME: str = "PT24H"
    DEFAULT_STATIONS: list[str] = ["retspy"]

    # Meta variables del intérprete de linea de comandos

    DIRECTORY_PATH: str = "DIRECTORY_PATH"
    FILE_PATH: str = "FILE_PATH"
    INTEGER_NUMBER: str = "INTEGER_NUMBER"
    ISO_DATE_TIME: str = "ISO_DATE_TIME"
    ISO_TIME_PERIOD: str = "ISO_TIME_PERIOD"
    ID_STRING: str = "ID_STRING"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._positionals.title = "Argumentos posicionales"
        self._optionals.title = "Argumentos opcionales"

    @classmethod
    def get_parser(cls) -> "CustomArgumentParser":
        parser = CustomArgumentParser(
            prog=info.name,
            description=f"{info.lemma}:\n\n{info.description}",
            epilog="Hecho por el equipo de desarrollo de RETSPy.\n"
            "Copyright (C) 2024.",
            add_help=False,
        )

        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s {info.version_short}",
            help="Muestra la versión del programa y termina.",
        )

        parser.add_argument(
            "-h",
            "--help",
            action="help",
            default=SUPPRESS,
            help="Muestra este mensaje de ayuda y termina.",
        )

        parser.add_argument(
            "-c" "--config-path",
            dest="config_path",
            metavar=cls.FILE_PATH,
            type=str,
            help="Ruta del archivo de configuración del indexador. "
            "Si se especifica este argumento, se ignora el archivo "
            "de configuración del usuario en la carpeta de trabajo.",
            default=None,
        )

        parser.add_argument(
            "-o" "--output-path",
            dest="output_path",
            metavar=cls.DIRECTORY_PATH,
            type=str,
            help="Ruta del directorio del repositorio local, por "
            "defecto es la carpeta de trabajo actual desde donde "
            "se ejecuta el script.",
            default=cls.DEFAULT_REPO_PATH,
        )

        parser.add_argument(
            "-s" "--start-time",
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

        parser.add_argument(
            "-e" "--end-time",
            dest="end_time",
            metavar=cls.ISO_DATE_TIME,
            type=str,
            help="Fecha y hora de fin de la descarga de imágenes de "
            "radar, en formato ISO 8601, por ejemplo: "
            "'2024-01-01T00:00:00', '2024-01-01T00:00:00-0300' "
            "o '2024-01-01T00:00:00Z'. Por defecto la descarga "
            "termina 24 horas después de la fecha de inicio. "
            "Tiene precedencia sobre el argumento -s/--scan-time.",
            default=None,
        )

        parser.add_argument(
            "-s" "--scan-time",
            dest="scan_period",
            metavar=cls.ISO_TIME_PERIOD,
            type=str,
            help="Duración de la ventana de tiempo de monitorización "
            "de imágenes de radar, en formato ISO 8601, por ejemplo: "
            "'PT10M' para 10 minutos, 'PT1H' para 1 hora, 'PT1H30M' "
            "para 1 hora y 30 minutos, etc. Por defecto es de 24 horas "
            "('PT24H'). Si se especifica el argumento -e/--end-time, "
            "este parámetro se ignora.",
            default=cls.DEFAULT_PERIOD_TIME,
        )

        parser.add_argument(
            "-S",
            "--stations",
            dest="station_ids",
            metavar=cls.ID_STRING,
            nargs="+",
            type=set[str],
            help="Lista de identificadores de estaciones o grupos de "
            "estaciones de radar del SINARAME, por defecto es el grupo "
            "de estaciones de prueba: 'retspy'.",
            default=cls.DEFAULT_STATIONS,
        )

        subparser = parser.add_subparsers(
            dest="init",
            help="Inicializa el directorio de trabajo "
            "crea una copia del archivo de configuración con los "
            "valores por defecto en la carpeta de trabajo. El usuario "
            "puede modificar los valores de configuración según sus "
            "necesidades.",
        )

        init_parser = subparser.add_parser(
            "init",
            prog=info.name,
            description=f"{info.lemma}:\n\n{info.description}",
            epilog="Hecho por el equipo de desarrollo de RETSPy.\n"
            "Copyright (C) 2024.",
            add_help=False,
            usage="%(prog)s init [opciones]",
        )

        init_parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s {info.version_short}",
            help="Muestra la versión del programa y termina.",
        )

        init_parser.add_argument(
            "-h",
            "--help",
            action="help",
            default=SUPPRESS,
            help="Muestra este mensaje de ayuda y termina.",
        )

        init_parser.add_argument(
            "-c" "--config-path",
            dest="config_path",
            metavar=cls.FILE_PATH,
            type=str,
            help="Crea una copia del archivo de configuración con los "
            "valores por defecto en la ruta indicada. Si se especifica "
            "esta opción, se ignora la creación del archivo de "
            "configuración del usuario en la carpeta de trabajo.",
            default=None,
        )

        return parser


class CLINamespace:

    def __init__(
        self,
        init: bool = False,
        config_path: str = "",
        output_path: str = "",
        start_time: str = "",
        end_time: str = "",
        scan_period: str = "",
        station_ids: set[str] = set(),
    ) -> None:
        self.init: bool = init
        self.config_path: str = config_path
        self.output_path: str = output_path
        self.start_time: str = start_time
        self.end_time: str = end_time
        self.scan_period: str = scan_period
        self.station_ids: set[str] = station_ids


class CLIParser:

    def parse_args(
        self, args: Sequence[str] | None = None, namespace: None = None
    ) -> CLINamespace:
        parser: CustomArgumentParser = CustomArgumentParser.get_parser()

        computed_namespace: Namespace = parser.parse_args(args, namespace)

        return CLINamespace(**vars(computed_namespace))


Parser = CLIParser
