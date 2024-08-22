import os
import shutil
from os import path

from ..base.exceptions import (
    UninitializedOutputDirError,
    UninitializedWorkspaceError,
)
from ..base.settings import Section
from ..base.utils import console
from .application_info import app_info
from .cli_parser import CLINamespace, Parser
from .settings_smn import SettingsSMN as Settings


class Bootstrap:

    def __init__(self, settings: Settings) -> None:
        self._settings: Settings = settings

    def run(self) -> Settings:
        # Crear el analizador de argumentos de la línea de comandos, y
        # obtener los argumentos de la línea de comandos
        parser: Parser = Parser()

        namespace: CLINamespace = parser.parse_args()

        # Si se especifica la opción de inicialización, se crea el
        # archivo de configuración en el espacio de trabajo del usuario
        # y sale; toma precedencia sobre cualquier otro argumento

        if namespace.init:
            self._initialize_workspace(namespace)

            return Settings(validate=False)

        # Si se especifica un archivo de configuración alternativo, se
        # carga y se sobrescriben los valores predeterminados

        if namespace.config_path:
            self._settings = self._load_custom_settings(namespace.config_path)

        # Verificar la existencia y el contenido correcto del archivo de
        # configuración

        self._check_settings()

        # Configurar el directorio de salida para las imágenes
        # descargadas

        self._setup_output_directory(namespace)

        # Configurar los argumentos de la línea de comandos

        self._setup_arguments(namespace)

        # Configurar el color de la consola

        os.system("color")

        return self._settings

    def _check_settings(self) -> None:
        if not self._settings.has("model"):
            raise UninitializedWorkspaceError(
                "El archivo de configuración no existe o no es el correcto"
            )

        if (
            self._settings.value("model").as_type(str)
            != app_info.settings_model
        ):
            raise UninitializedWorkspaceError(
                "El archivo de configuración no es el correcto"
            )

    def _initialize_workspace(self, namespace: CLINamespace) -> None:
        # Crear el archivo de configuración si no existe. Si existe,
        # preguntar al usuario si se desea sobrescribir. En caso
        # afirmativo se sobrescribirá con los valores predeterminados

        user_settings_path: str = namespace.config_path or path.join(
            self._settings.current_dir, app_info.user_settings
        )

        if path.exists(user_settings_path):
            overwrite: str = console.prompt(
                "El archivo de configuración ya existe. "
                "¿Desea sobrescribirlo?",
                console.YES_NO,
            )

            if console.response_is(overwrite, console.NO):
                return

        # Copiar el archivo de configuración predeterminado al espacio
        # de trabajo del usuario

        default_settings_path: str = path.join(
            self._settings.install_dir, app_info.default_settings
        )

        if not path.exists(default_settings_path):
            raise FileNotFoundError(
                f"El archivo de configuración predeterminado no existe: "
                f"'{default_settings_path}'"
            )

        shutil.copyfile(default_settings_path, user_settings_path)

        self._load_custom_settings(user_settings_path)

    def _load_custom_settings(self, config_path: str) -> Settings:
        # Cargar el archivo de configuración y sobrescribir los valores
        # predeterminados

        settings: Settings = Settings.load(
            config_path, fail_if_not_exists=True
        )

        settings.root.update(self._settings.section("path").to_dict())

        return settings

    def _setup_arguments(self, namespace: CLINamespace) -> None:
        # Configurar los argumentos de la línea de comandos

        self._settings.create_subsection("args")

        self._settings.section("args").update(
            {
                "start_time": namespace.start_time,
                "end_time": namespace.end_time,
                "scan_period": namespace.scan_period,
                "station_ids": namespace.station_ids,
            }
        )

    def _setup_output_directory(self, namespace: CLINamespace) -> None:
        # Obtener el directorio de salida para las imágenes descargadas

        if namespace.output_path:
            # El usuario especificó un directorio de salida

            repository_path: str = namespace.output_path

        else:
            # El usuario no especificó un directorio de salida, por lo
            # que se utilizará el directorio de salida predeterminado

            client: Section = self._settings.section("client")

            repository_path = client.value("repository_path").as_type(str)

        output_dir: str = path.abspath(repository_path)

        # Si no existe el directorio de salida, preguntar al usuario si
        # se desea crearlo.

        if not path.exists(output_dir):
            overwrite: str = console.prompt(
                "El directorio de salida no existe. ¿Desea crearlo?",
                console.YES_NO,
            )

            if console.response_is(overwrite, console.NO):
                raise UninitializedOutputDirError(
                    "El directorio de salida no existe"
                )

            os.makedirs(output_dir, exist_ok=True)

        self._settings.section("path").update(
            {
                "output_dir": output_dir,
            }
        )
