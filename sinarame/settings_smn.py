from typing import Any

from ..base.exceptions import InvalidConfigurationFileError
from ..base.settings.settings_basic import SettingsBasic
from ..base.utils.timing import timing


class SettingsSMN(SettingsBasic):

    CREDENTIALS_PATH: str = "credentials.snm.json"

    AUTH_HEADERS: dict[str, str] = {
        "credentials": "omit",
        "priority": "u=0, i",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    }

    BASE_HEADERS: dict[str, str] = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        ),
        "accept-language": (
            "en-GB;q=0.9,en-US;q=0.8,en;q=0.7,"
            "es-ES;q=0.8,es-PY;q=0.7,es;q=0.6,"
        ),
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": (
            '"Chromium";v="128", '
            '"Not;A=Brand";v="24", '
            '"Google Chrome";v="128"'
        ),
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "referrer": "https://www.smn.gob.ar/",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "mode": "cors",
    }

    COMMON_HEADERS: dict[str, str] = {
        "credentials": "include",
        "sec-fetch-site": "same-site",
    }

    IMAGE_HEADERS: dict[str, str] = {
        "accept": "image/png",
        "priority": "i",
        "sec-fetch-dest": "image",
        "sec-fetch-mode": "no-cors",
    }

    LIST_HEADERS: dict[str, str] = {
        "accept": "application/json",
        "authorization": "JWT {token}",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
    }

    TOKEN_HEADERS: dict[str, str] = BASE_HEADERS | AUTH_HEADERS
    TOKEN_PATTERN: str = r"localStorage\.setItem\('token',\s*'([^']+)'\);"

    IMAGE_SET_HEADERS: dict[str, str] = (
        BASE_HEADERS | LIST_HEADERS | COMMON_HEADERS
    )

    REPOSITORY_HEADERS: dict[str, str] = (
        BASE_HEADERS | IMAGE_HEADERS | COMMON_HEADERS
    )

    def __init__(self, settings: dict[str, Any] | None = None) -> None:
        super().__init__(settings or dict())

        self._validate()

        self._version: str = self.value("version").as_type(str)

    @classmethod
    def load(
        cls, settings_path: str, fail_if_not_exists: bool = True
    ) -> "SettingsSMN":
        """
        Carga los ajustes de configuración desde un archivo.

        Parameters
        ----------
        settings_path : str
            La ruta del archivo de ajustes de configuración.
        """
        basic: SettingsBasic = super().load(settings_path, fail_if_not_exists)

        return SettingsSMN(basic.root.to_dict())

    def _validate(self) -> None:
        """
        Valida los valores de las configuraciones.

        Raises
        ------
        InvalidConfigurationFileError
            Si alguna configuración no es válida.
        """
        try:
            assert self.value("model").as_type(str) == "sinarame"
            assert self.value("version").as_type(str) == "1.0"

            assert self.has("metadata")
            assert self.has("server")
            assert self.has("client")
            assert self.has("timing")
            assert self.has("station_groups")
            assert self.has("stations")

        except AssertionError:
            raise InvalidConfigurationFileError(
                "El archivo de configuración no es válido."
            )

    @property
    def chunk_size(self) -> int:
        """
        Obtiene el tamaño de los fragmentos de descarga.

        Returns
        -------
        int
            El tamaño de los fragmentos de descarga en bytes.
        """
        return self.section("client").value("chunk_size").as_type(int)

    @property
    def current_dir(self) -> str:
        """
        Obtiene la ruta del directorio actual.

        Returns
        -------
        str
            La ruta del directorio actual.
        """
        return self.section("path").value("current_dir").as_type(str)

    @property
    def end_time(self) -> str:
        """
        Obtiene la hora de fin de la recolección de datos.

        Returns
        -------
        str
            La hora de fin de la recolección de datos.
        """
        return self.section("args").value("end_time").as_type(str)

    @property
    def install_dir(self) -> str:
        """
        Obtiene la ruta del directorio actual.

        Returns
        -------
        str
            La ruta del directorio actual.
        """
        return self.section("path").value("install_dir").as_type(str)

    @property
    def inventory_url(self) -> str:
        """
        Obtiene la URL del conjunto de imágenes disponibles.

        Returns
        -------
        str
            La URL del conjunto de imágenes disponibles.
        """
        return self.section("server").value("inventory_url").as_type(str)

    @property
    def radar_url(self) -> str:
        """
        Obtiene la URL de la página de imágenes de los radares del SINARAME.

        Returns
        -------
        str
            La URL de la página de imágenes de radar.
        """
        return self.section("server").value("radar_url").as_type(str)

    @property
    def repository_path(self) -> str:
        """
        Obtiene la ruta del directorio de almacenamiento local.

        Returns
        -------
        str
            La ruta del directorio de almacenamiento local de las
            imágenes.
        """
        return self.section("client").value("repository_path").as_type(str)

    @property
    def repository_url(self) -> str:
        """
        Obtiene la URL del repositorio de imágenes.

        Returns
        -------
        str
            La URL del repositorio de imágenes remoto.
        """
        return self.section("server").value("repository_url").as_type(str)

    @property
    def scan_interval(self) -> float:
        """
        Obtiene el intervalo de tiempo de escaneo de las imágenes.

        Returns
        -------
        int
            El intervalo de tiempo de escaneo en segundos.
        """
        units: str = self.section("timing").value("units").as_type(str)

        value: float = (
            self.section("timing").value("scan_interval").as_type(float)
        )

        return timing.to_seconds(value, units)

    @property
    def scan_period(self) -> str:
        """
        Obtiene el período de escaneo de las imágenes.

        Returns
        -------
        str
            El período de escaneo de las imágenes.
        """
        return self.section("args").value("scan_period").as_type(str)

    @property
    def start_time(self) -> str:
        """
        Obtiene la hora de inicio de la recolección de datos.

        Returns
        -------
        str
            La hora de inicio de la recolección de datos.
        """
        return self.section("args").value("start_time").as_type(str)

    @property
    def station_ids(self) -> list[str]:
        """
        Obtiene los identificadores de las estaciones a escanear.

        Returns
        -------
        list[str]
            Los identificadores de las estaciones a escanear.
        """
        return self.section("args").value("station_ids").as_type(list[str])

    @property
    def wait_for_next_authorization(self) -> float:
        """
        Obtiene el tiempo de espera entre solicitudes de autorización.

        Returns
        -------
        int
            El tiempo de espera en segundos.
        """
        units: str = self.section("timing").value("units").as_type(str)

        value: float = (
            self.section("timing")
            .value("wait_for_next_authorization")
            .as_type(float)
        )

        return timing.to_seconds(value, units)

    @property
    def wait_for_next_request(self) -> float:
        """
        Obtiene el tiempo de espera entre solicitudes HTTP.

        Returns
        -------
        int
            El tiempo de espera en segundos.
        """
        units: str = self.section("timing").value("units").as_type(str)

        value: float = (
            self.section("timing")
            .value("wait_for_next_request")
            .as_type(float)
        )

        return timing.to_seconds(value, units)
