from argparse import ArgumentParser, Namespace
from typing import Sequence

from ..application_info import app_info
from ..init import CLIParser as InitCLIParser
from ..package_info import pkg_info
from ..shared import CLIParserBase, CustomArgumentParser, SubParsersAction
from ..simepar import CLIParser as SimeparCLIParser
from ..sinarame import CLIParser as SinarameCLIParser


class CLINamespace:

    def __init__(
        self,
        command: str = "",
        config_path: str = "",
        output_path: str = "",
        start_time: str = "",
        end_time: str = "",
        scan_period: str = "",
        verbosity: str = "",
        station_ids: set[str] = set(),
    ) -> None:
        self.command: str = command
        self.config_path: str = config_path
        self.output_path: str = output_path
        self.start_time: str = start_time
        self.end_time: str = end_time
        self.scan_period: str = scan_period
        self.verbosity: str = verbosity
        self.station_ids: set[str] = station_ids


class CLIParser(CLIParserBase):

    COMMAND_TITLE = "Acciones de servicio y monitoreo"
    COMMAND_NAME = "command"

    @classmethod
    def get_parser(cls) -> CustomArgumentParser:
        parser = CustomArgumentParser(
            prog=pkg_info.name,
            description=f"{app_info.header}: {app_info.help}",
            epilog=app_info.copyright,
            add_help=False,
        )

        cls.create_subparsers(parser)

        cls.setup_parser(parser)

        return parser

    @classmethod
    def create_subparsers(cls, parser: CustomArgumentParser) -> None:
        commands: SubParsersAction = parser.add_subparsers(
            title=cls.COMMAND_TITLE,
            # description="Acciones de servicio y monitoreo disponibles.",
            metavar="{command}",
            dest=cls.COMMAND_NAME,
            help="Uno de los comandos siguientes:",
        )

        # "Comandos de servicio"

        InitCLIParser.create_parser(commands)

        # "Comandos de monitoreo"

        SimeparCLIParser.create_parser(commands)
        SinarameCLIParser.create_parser(commands)

    @classmethod
    def setup_parser(cls, parser: ArgumentParser) -> None:
        cls.setup_parser_common(
            parser, version=f"{pkg_info.name} {app_info.version}"
        )

    def parse_args(
        self, args: Sequence[str] | None = None, namespace: None = None
    ) -> CLINamespace:
        parser: CustomArgumentParser = self.get_parser()

        computed_namespace: Namespace = parser.parse_args(args, namespace)

        return CLINamespace(**vars(computed_namespace))
