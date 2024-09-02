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

    COMMAND_TITLE = "Comandos"
    COMMAND_NAME = "command"

    @classmethod
    def get_parser(cls) -> CustomArgumentParser:
        parser = CustomArgumentParser(
            prog=pkg_info.name,
            description=f"{app_info.header}: {app_info.help}",
            epilog=app_info.copyright,
            add_help=False,
        )

        cls.setup_parser(parser)

        cls.create_parser_service(parser)

        cls.create_parser_monitor(parser)

        return parser

    @classmethod
    def create_parser_monitor(cls, parser: CustomArgumentParser) -> None:
        monitor_cmd: SubParsersAction = parser.add_subparsers(
            title=cls.COMMAND_TITLE,
            dest=cls.COMMAND_NAME,
            help="Comandos de monitoreo",
        )

        SimeparCLIParser.create_parser(monitor_cmd)
        SinarameCLIParser.create_parser(monitor_cmd)

    @classmethod
    def create_parser_service(cls, parser: CustomArgumentParser) -> None:
        service_cmd: SubParsersAction = parser.add_subparsers(
            title=cls.COMMAND_TITLE,
            dest=cls.COMMAND_NAME,
            help="Comandos de servicio",
        )

        InitCLIParser.create_parser(service_cmd)

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
