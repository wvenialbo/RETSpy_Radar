from ..shared import (
    ArgumentGroup,
    ArgumentParser,
    CLIParserBase,
    SubParsersAction,
)
from .application_info import app_info


class CLIParser(CLIParserBase):

    @classmethod
    def create_parser(cls, subparser_cmd: SubParsersAction) -> None:
        subparser: ArgumentParser = subparser_cmd.add_parser(
            app_info.command,
            help=app_info.help,
            description=f"{app_info.header}: {app_info.help}",
            epilog=app_info.copyright,
            add_help=False,
        )

        cls.setup_parser(subparser)

    @classmethod
    def setup_parser_config(cls, parser: ArgumentParser) -> None:
        config: ArgumentGroup = parser.add_argument_group(
            title="Opciones de configuración",
            # description="Opciones de archivo y configuración.",
        )

        config.add_argument(
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

    @classmethod
    def setup_parser(cls, parser: ArgumentParser) -> None:
        cls.setup_parser_shared(parser, version="")
        cls.setup_parser_config(parser)
