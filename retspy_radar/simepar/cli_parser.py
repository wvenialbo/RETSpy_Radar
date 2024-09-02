from argparse import SUPPRESS, ArgumentParser

from ..package_info import pkg_info
from ..shared import CLIParserBase, SubParsersAction
from .application_info import app_info


class CLIParser(CLIParserBase):

    # Constantes de la aplicación

    DEFAULT_STATIONS: list[str] = ["mosaico"]

    @classmethod
    def create_parser(cls, subparser_cmd: SubParsersAction) -> None:
        subparser: ArgumentParser = subparser_cmd.add_parser(
            app_info.command,
            help=app_info.help,
            prog=f"{pkg_info.name} {app_info.command}",
            description=f"{app_info.header}: {app_info.help}",
            epilog=app_info.copyright,
            add_help=False,
        )

        cls.setup_parser(subparser)

    @classmethod
    def setup_parser(cls, parser: ArgumentParser) -> None:
        cls.setup_parser_shared(
            parser, version=f"{pkg_info.name} {app_info.version}"
        )

        cls.setup_parser_config(parser)

        cls.setup_parser_monitor(parser)

        parser.add_argument(
            "-i",
            "--station-ids",
            dest="station_ids",
            metavar=cls.ID_STRING,
            nargs="+",
            type=set[str],
            # help="Lista de identificadores de estaciones o grupos de "
            # "estaciones de radar del SIMEPAR, por defecto es el grupo "
            # f"de estaciones de prueba: '{cls.DEFAULT_STATIONS[0]}'.",
            help=SUPPRESS,
            default=cls.DEFAULT_STATIONS,
        )
