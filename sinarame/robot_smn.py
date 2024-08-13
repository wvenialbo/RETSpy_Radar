from logging import Logger
from os import path
from typing import Any, Iterator

from ..base.exceptions import (
    AuthorizationError,
    AuthorizationExpiredError,
    InvalidConfigurationFileError,
    RequestError,
    UnexpectedResponseError,
)
from ..base.process.sleep import ProcessSleep
from ..base.robot_base import RobotBase
from ..base.settings.settings_basic import SettingsBasic
from .handler_smn import RequestsHandlerSNM
from .settings_smn import SettingsSMN


class RobotSMN(RobotBase):
    """
    Indexador de imágenes de radar del SINARAME.

    El indexador de imágenes de radar del Sistema Nacional de Radares
    Meteorológicos (SINARAME), del Servicio Meteorológico Nacional (SMN)
    argentino, permite descargar las imágenes de radar de las estaciones
    del SINARAME desde el sitio web de la SMN para guardarlas en un
    repositorio local. Las imágenes de radar se actualizan cada 10
    minutos.

    El objetivo del bot es recopilar las imágenes de radar asociadas a
    eventos meteorológicos extremos en la región de interés, para
    archivarlos en una base de datos de reportes de eventos de tiempo
    severo, para su análisis o estudio posterior.

    Methods
    -------
    run(station_ids, from_datetime=None, to_datetime=None,
        for_timedelta=None) Ejecuta el proceso de recolección de datos.
        Heredado de la clase base `RobotBase`.
    """

    def __init__(self, settings: SettingsSMN, logger: Logger) -> None:
        """
        Inicializa una nueva instancia del indexador de imágenes.

        Parameters
        ----------
        settings : SettingsSMN
            Los ajustes de configuración del indexador de imágenes.
        logger : Logger
            El registro de eventos del indexador de imágenes.
        """
        self._logger: Logger = logger
        self._settings: SettingsSMN = settings

    def _filter_downloaded_images(self, image_set: set[str]) -> set[str]:
        """
        Filtra las imágenes que ya se encuentran en el repositorio.

        Filtra las imágenes que ya se encuentran en el repositorio
        local, eliminando las imágenes que ya han sido descargadas.

        Parameters
        ----------
        image_set : set[str]
            Un conjunto de identificadores de imágenes.

        Returns
        -------
        set[str]
            Un conjunto de identificadores de imágenes pendientes.
        """
        # Actualizar el conjunto de archivos pendientes, removiendo los
        # archivos que ya se encuentran en el repositorio local
        repository_path: str = self._get_repository_path()

        for image_name in image_set.copy():
            if path.exists(f"{repository_path}{image_name}"):
                image_set.remove(image_name)

        return image_set

    def _get_access_token(self, api_key: str, renew: bool) -> str:
        """
        Obtiene o renueva un token de acceso.

        Obtiene un token de acceso del SMN. El token de acceso permite
        acceder a las imágenes de radar de las estaciones del SINARAME.

        Se intenta leer el token de acceso almacenado en un archivo de
        credenciales o se obtiene un token de acceso desde el sitio web
        del SMN. Si no se pudo obtener un token de acceso, se lanza una
        excepción.

        Parameters
        ----------
        api_key : str
            La clave de identificación para el uso de la API.
        renew : bool
            Indica si se debe renovar el token de acceso. Si es
            True, se obtiene un nuevo token de acceso desde el
            sitio web del servicio.

        Returns
        -------
        str
            El token de acceso si se obtuvo correctamente.

        Raises
        ------
        AuthorizationError
            Si no se pudo obtener un token de acceso.
        """
        # Esperar un tiempo para no saturar el servidor y evitar
        # ser bloqueado, luego obtener la lista de imágenes

        wait_for_next_authorization = ProcessSleep(
            self._settings.wait_for_next_authorization
        )

        wait_for_next_authorization.run()

        try:
            token: str = ""

            if not renew:
                token = self._load_token_from_file(
                    self._settings.CREDENTIALS_PATH
                )

                renew = not token

            if renew:
                token = self._get_token_from_server(api_key)

                self._save_token_to_file(
                    self._settings.CREDENTIALS_PATH, token
                )

            return token

        except (
            InvalidConfigurationFileError,
            RequestError,
            UnexpectedResponseError,
        ) as exc:
            raise AuthorizationError(
                f"No se pudo obtener un token de acceso: {exc}"
            ) from exc

    def _get_api_key(self) -> str:
        """
        Obtiene la clave de identificación para el uso de la API.

        El sitio web del SMN no requiere una clave de identificación,
        se retorna  una cadena vacía.

        Returns
        -------
        str
            Una cadena vacía.
        """
        return ""

    def _get_inventory(
        self, station_ids: set[str], api_key: str, auth_token: str
    ) -> set[str]:
        """
        Obtiene el conjunto de imágenes de radar meteorológico.

        Parameters
        ----------
        station_ids : set[str]
            El conjunto de identificadores de estaciones meteorológicas.
        api_key : str
            La clave de identificación para el uso de la API.
        auth_token : str
            El token de acceso para la autorización en la API.

        Returns
        -------
        set[str]
            El conjunto de imágenes de radar meteorológico.
        """
        # La clave de identificación no se utiliza en esta versión

        wait_for_next_request = ProcessSleep(
            self._settings.wait_for_next_request
        )

        requests = RequestsHandlerSNM(self._settings)

        image_set: set[str] = set()

        for station_id in station_ids:
            # Esperar un tiempo para no saturar el servidor y evitar
            # ser bloqueado, luego obtener la lista de imágenes
            wait_for_next_request.run()

            try:
                images: set[str] = requests.get_inventory(
                    station_id, auth_token
                )

                image_set.update(images)

            except RequestError as exc:
                if exc.status_code in {401}:
                    raise AuthorizationExpiredError(
                        "El token de autorización ha expirado."
                    ) from exc

                raise exc

        return self._filter_downloaded_images(image_set)

    def _get_images(
        self, image_set: set[str], api_key: str, auth_token: str
    ) -> set[str]:
        """
        Descarga las imágenes especificadas.

        Descarga las imágenes especificadas y las almacena en el
        repositorio de datos.

        Parameters
        ----------
        image_set : set[str]
            Un conjunto de identificadores de imágenes.
        api_key : str
            La clave de identificación para el uso de la API.
        auth_token : str
            El token de acceso para la autorización en la API.

        Returns
        -------
        set[str]
            Un conjunto de identificadores de imágenes descargadas.
        """
        # La clave de identificación no se utiliza en esta versión

        wait_for_next_request = ProcessSleep(
            self._settings.wait_for_next_request
        )

        requests = RequestsHandlerSNM(self._settings)

        pendent_set: set[str] = image_set.copy()

        for image_name in image_set:
            # Esperar un tiempo para no saturar el servidor y evitar ser
            # bloqueado, luego descargar y guardar cada imagen pendiente
            wait_for_next_request.run()

            try:
                image_data: Iterator[Any] = requests.download_image(image_name)

                pendent_set.remove(image_name)

                self._save_image(image_name, image_data)

            except RequestError as exc:
                if exc.status_code in {401}:
                    raise AuthorizationExpiredError(
                        "El token de autorización ha expirado."
                    ) from exc

                raise exc

        return image_set - pendent_set

    def _get_repository_path(self) -> str:
        """
        Obtiene la ruta del repositorio de datos.

        Retorna la ruta del repositorio de datos del archivo de
        configuración.

        Returns
        -------
        str
            La ruta del repositorio de datos.
        """
        return self._settings.repository_path

    def _get_token_from_server(self, api_key: str) -> str:
        """
        Obtiene un token de autorización.

        Obtiene un token de acceso desde el sitio web del SMN.

        Parameters
        ----------
        api_key : str
            La clave de identificación para el uso de la API

        Returns
        -------
        str
            El token de autorización si se obtuvo correctamente.

        Raises
        ------
        RequestError
            Si hubo un error al realizar la solicitud HTTP.
        UnexpectedResponseError
            Si no se encontró el token de autorización en la respuesta.
        """
        # La clave de identificación no se utiliza en esta versión

        requests = RequestsHandlerSNM(self._settings)

        return requests.get_access_token()

    @staticmethod
    def _load_token_from_file(credentials_path: str) -> str:
        """
        Obtiene un token de acceso de un archivo de credenciales.

        Parameters
        ----------
        credentials_path : str
            La ruta del archivo de credenciales.

        Returns
        -------
        str
            El token de acceso leído desde el archivo. Una cadena vacía
            si el archivo no existe o no se pudo leer.

        Raises
        ------
        InvalidConfigurationFileError
            Si el archivo de credenciales no contiene un token de acceso
            o no es válido.
        """
        credentials: SettingsBasic = SettingsBasic.load(
            credentials_path, fail_if_not_exists=False
        )

        if credentials.is_empty():
            return ""

        if credentials.has("token"):
            return credentials.value("token").as_type(str)

        raise InvalidConfigurationFileError(
            "El archivo de credenciales no contiene un token de acceso."
        )

    def _save_image(self, image_name: str, image_data: Iterator[Any]) -> None:
        """
        Guarda una imagen de radar en el repositorio local.

        Guarda una imagen de radar en el repositorio local especificado
        por la ruta del repositorio local. Los datos de la imagen se
        guardan en disco con el nombre de la imagen.

        Parameters
        ----------
        image_name : str
            El nombre de la imagen a guardar.
        data : Iterator[Any]
            Los datos de la imagen.

        Raises
        ------
        RequestException
            Si hubo un error al guardar la imagen en disco.
        """
        try:
            repository_path: str = self._get_repository_path()

            image_path: str = f"{repository_path}{image_name}"

            # Guardar la imagen en el disco
            with open(image_path, "wb") as file:
                for chunk in image_data:
                    file.write(chunk)

        except (IOError, OSError, TypeError) as exc:
            print(f"Error al guardar la imagen: {exc}")

    @staticmethod
    def _save_token_to_file(credentials_path: str, token: str) -> None:
        """
        Guarda un token de acceso en un archivo de credenciales.

        Parameters
        ----------
        credentials_path : str
            La ruta del archivo de credenciales.
        token : str
            El token de acceso.

        Raises
        ------
        InvalidConfigurationFileError
            Si no se pudo guardar el token de acceso en el archivo de
            credenciales.
        """
        credentials_dict: dict[str, str] = {"token": token}

        credentials = SettingsBasic(credentials_dict)

        credentials.save(credentials_path)
