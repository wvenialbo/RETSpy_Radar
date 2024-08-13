import os
import shutil
from os import path

from ..base.exceptions import (
    UninitializedOutputDirError,
    UninitializedWorkspaceError,
)
from ..base.settings import Section
from .application_info import info
from .cli_parser import CLINamespace, Parser
from .settings_smn import SettingsSMN as Settings


class Bootstrap:

    YES = "Sí"
    NO = "No"
    YES_NO: list[str] = [YES, NO]

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
            self._initialize_workspace()

            return Settings()

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

    @staticmethod
    def _ask_user(question: str, expect: list[str]) -> str:
        expect_lower: list[str] = [option.lower() for option in expect]

        choices: str = "/".join(expect)

        query_message: str = f"{question} ({choices}): "

        answer: str = ""

        while answer not in expect_lower:
            answer = input(query_message).strip().lower()

        return answer

    def _check_settings(self) -> None:
        if not self._settings.has("model"):
            raise UninitializedWorkspaceError(
                "El archivo de configuración no existe o no es el correcto"
            )

        if self._settings.value("model").as_type(str) != info.settings_model:
            raise UninitializedWorkspaceError(
                "El archivo de configuración no es el correcto"
            )

    def _initialize_workspace(self) -> None:
        # Crear el archivo de configuración si no existe. Si existe,
        # preguntar al usuario si se desea sobrescribir. En caso
        # afirmativo se sobrescribirá con los valores predeterminados

        user_settings_path: str = path.join(
            self._settings.current_dir, info.user_settings
        )

        if path.exists(user_settings_path):
            overwrite: str = self._ask_user(
                "El archivo de configuración ya existe. "
                "¿Desea sobrescribirlo?",
                self.YES_NO,
            )

            if self._response_is(overwrite, self.NO):
                return

        # Copiar el archivo de configuración predeterminado al espacio
        # de trabajo del usuario

        default_settings_path: str = path.join(
            self._settings.install_dir, info.default_settings
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

    @staticmethod
    def _response_is(response: str, expected: str) -> bool:
        return response.strip().lower() == expected.strip().lower()

    def _setup_arguments(self, namespace: CLINamespace) -> None:
        # Configurar los argumentos de la línea de comandos

        if namespace.start_time:
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
            overwrite: str = self._ask_user(
                "El directorio de salida no existe. ¿Desea crearlo?",
                self.YES_NO,
            )

            if self._response_is(overwrite, self.NO):
                raise UninitializedOutputDirError(
                    "El directorio de salida no existe"
                )

            os.makedirs(output_dir, exist_ok=True)

        self._settings.section("path").update(
            {
                "output_dir": output_dir,
            }
        )
