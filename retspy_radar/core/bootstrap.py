import os
import shutil
import sys
from os import path

from ..application_info import app_info
from ..base.exceptions import (
    UninitializedOutputDirError,
    UninitializedWorkspaceError,
    UnspecifiedCommandError,
)
from ..base.settings import SettingsBasic, SettingsValue
from ..base.utils import console
from ..base.utils import settings as config
from ..package_info import pkg_info
from .cli_parser import CLINamespace, CLIParser


class Bootstrap:

    def __init__(self, settings: SettingsBasic) -> None:
        self._settings: SettingsBasic = settings

    def run(self) -> SettingsBasic:
        # Crear el analizador de argumentos de la línea de comandos, y
        # obtener los argumentos de la línea de comandos

        parser = CLIParser()

        namespace: CLINamespace = parser.parse_args()

        # Si no se especifica un comando, lanzar una excepción

        if not namespace.command:
            raise UnspecifiedCommandError("No se ha especificado un comando")

        # Si se especifica la opción de inicialización, se crea el
        # archivo de configuración en el espacio de trabajo del usuario
        # y sale; toma precedencia sobre cualquier otro argumento

        if namespace.command == "init":
            self._settings = self._initialize_workspace(namespace)

            sys.exit(0)

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

        return self._settings

    def _check_settings(self) -> None:
        if (
            not self._settings.has("product")
            or not self._settings.has("version")
            or not self._settings.has("services")
        ):
            raise UninitializedWorkspaceError(
                "El archivo de configuración no existe, "
                "no es el correcto o está corrupto"
            )

        product_name = self._settings["product"].as_type(str)
        product_version = self._settings["version"].as_type(str)

        if product_name != pkg_info.name or not pkg_info.version.startswith(
            product_version
        ):
            raise UninitializedWorkspaceError(
                "El archivo de configuración no corresponde "
                "al producto o versión actual"
            )

        services: list[str] = self._settings["services"].as_type(list[str])

        for service in services:
            if not self._settings.has(service):
                raise UninitializedWorkspaceError(
                    "El archivo de configuración está corrupto"
                )

    def _initialize_workspace(self, namespace: CLINamespace) -> SettingsBasic:
        # Crear el archivo de configuración si no existe

        current_dir: str = self._settings["path"]["current_dir"].as_type(str)
        current_path: str = path.join(current_dir, app_info.user_settings)
        user_settings_path: str = namespace.config_path or current_path
        workspace_dir: str = os.path.dirname(user_settings_path)

        # Si la ruta del archivo de configuración no existe, preguntar al
        # usuario si se desea crearla. Si no se desea crear, salir

        if not path.exists(workspace_dir):
            create: str = console.prompt(
                "La ruta del archivo de configuración no existe. "
                "¿Desea crearla?",
                console.YES_NO,
            )

            if console.response_is(create, console.NO):
                return SettingsBasic()

            os.makedirs(workspace_dir)

        # Si la ruta del archivo de configuración no es un directorio,
        # lanzar una excepción

        elif not path.isdir(workspace_dir):
            raise NotADirectoryError(
                f"La ruta del archivo de configuración no es un directorio: "
                f"'{workspace_dir}'"
            )

        # Si el archivo de configuración ya existe, preguntar al usuario
        # si se desea sobrescribir. En caso afirmativo se sobrescribirá
        # con los valores predeterminados. Si no se desea sobrescribir,
        # salir

        if path.exists(user_settings_path):
            if not path.isfile(user_settings_path):
                raise IsADirectoryError(
                    f"La ruta del archivo de configuración es un directorio: "
                    f"'{user_settings_path}'"
                )

            overwrite: str = console.prompt(
                "El archivo de configuración ya existe. "
                "¿Desea sobrescribirlo?",
                console.YES_NO,
            )

            if console.response_is(overwrite, console.NO):
                return SettingsBasic()

        # Copiar el archivo de configuración predeterminado al espacio
        # de trabajo del usuario

        install_dir: str = self._settings["path"]["install_dir"].as_type(str)
        default_settings_path: str = path.join(
            install_dir, app_info.default_settings
        )

        if not path.exists(default_settings_path):
            raise FileNotFoundError(
                f"El archivo de configuración predeterminado no existe: "
                f"'{default_settings_path}'"
            )

        shutil.copyfile(default_settings_path, user_settings_path)

        # Verificar que el archivo de configuración se haya copiado
        # correctamente cargando el archivo de configuración

        return self._load_custom_settings(user_settings_path)

    def _load_custom_settings(self, config_path: str) -> SettingsBasic:
        # Cargar el archivo de configuración y sobrescribir los valores
        # predeterminados

        settings: SettingsBasic = config.load(
            config_path, fail_if_not_exists=True
        )

        settings.root.update(self._settings["path"])

        return settings

    def _setup_arguments(self, namespace: CLINamespace) -> None:
        # Configurar los argumentos de la línea de comandos

        self._settings.root.update(
            {
                "args": {
                    "command": namespace.command,
                    "start_time": namespace.start_time or "",
                    "end_time": namespace.end_time or "",
                    "scan_period": namespace.scan_period,
                    "station_ids": namespace.station_ids or [],
                }
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

            client: SettingsValue = self._settings["client"]

            repository_path = client["repository_path"].as_type(str)

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

            os.makedirs(output_dir)

        self._settings.root.update(
            {
                "path": {
                    "output_dir": output_dir,
                }
            }
        )
