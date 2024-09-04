import re
from re import Match
from typing import Any, Iterator

from requests import Response
from requests.exceptions import RequestException

from ..base.exceptions import RequestError, UnexpectedResponseError
from ..base.requests import RequestsHandlerBase
from ..shared import APPLICATION_JSON, IMAGE_PNG, TEXT_HTML, Headers, Settings


class RequestsHandlerSNM(RequestsHandlerBase):
    """
    Realiza solicitudes HTTP al Servicio Meteorológico Nacional (SMN).

    Attributes
    ----------
    _setting : SettingsSMN
        La configuración de la aplicación.
    _status_code : int
        El código de estado de la última solicitud HTTP.

    Methods
    -------
    get_access_token() -> str
        Obtiene un token de acceso.

    Properties
    ----------
    status_code : int
        Obtiene el código de estado de la última solicitud HTTP.
    """

    TOKEN_PATTERN: str = r"localStorage\.setItem\('token',\s*'([^']+)'\);"

    def __init__(self, settings: Settings) -> None:
        """
        Inicializa una nueva instancia de la clase RequestsSNM.

        Parameters
        ----------
        settings : SettingsSMN
            La configuración de la aplicación.
        """
        super().__init__()

        self._settings: Settings = settings

    def download_image(self, image_name: str) -> Iterator[Any]:
        """
        Descarga una imagen de radar.

        Realiza una solicitud HTTP al repositorio de imágenes del SMN
        para descargar una imagen de radar. Los datos de la imagen se
        devuelven como un iterador.

        Parameters
        ----------
        image_name : str
            El nombre de la imagen a descargar.

        Returns
        -------
        Iterator[Any]
            Un iterador con los datos de la imagen.

        Raises
        ------
        RequestError
            Si hubo un error al realizar la solicitud HTTP.
        """
        try:
            # Realizar la solicitud HTTP para descargar la imagen

            request_url: str = f"{self._settings.repository_url}{image_name}"

            request_headers = Headers(
                self._settings.base_url, accept=IMAGE_PNG
            )

            response: Response = self.request.get(
                request_url,
                headers=request_headers.headers,
                timeout=self._settings.request_timeout,
            )

            # Devolver los datos de la imagen como un iterador de bytes
            # por bloques con un tamaño de 1024 bytes

            return response.iter_content(self._settings.chunk_size)

        except RequestException as exc:
            raise RequestError(
                f"No se pudo descargar la imagen '{image_name}",
                self.status_code,
            ) from exc

    def get_access_token(self) -> str:
        """
        Obtiene un token de acceso.

        Realiza una solicitud HTTP a la página del radar del SMN y
        extrae el token de acceso de la respuesta. El token de acceso
        permite acceder a las imágenes de radar de las estaciones del
        Servicio Meteorológico Nacional (SMN) argentino.

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
        try:
            # Realizar la solicitud HTTP para obtener la autorización

            request_url: str = self._settings.radar_url

            request_headers = Headers(
                self._settings.base_url, accept=TEXT_HTML
            )

            response: Response = self.request.get(
                request_url,
                headers=request_headers.headers,
                timeout=self._settings.request_timeout,
            )

            # Extraer el token de autorización de la respuesta

            match: Match[str] | None = re.search(
                self.TOKEN_PATTERN, response.text
            )

            # Si se encontró el token de autorización, devolverlo

            if match:
                return match.group(1)

        except RequestException as exc:
            raise RequestError(
                "Error al solicitar el código de autorización",
                self.status_code,
            ) from exc

        raise UnexpectedResponseError(
            "No se encontró el código de autorización en la respuesta"
        )

    def get_inventory(self, station_id: str, auth_token: str) -> set[str]:
        """
        Obtiene la lista de imágenes de una estación.

        Realiza una solicitud HTTP al servicio web del SMN para obtener
        la lista de imágenes de una estación de radar. La lista de
        imágenes contiene los nombres de las imágenes de radar que se
        pueden descargar.

        Parameters
        ----------
        station_id : str
            El ID de la estación de radar.
        token : str
            El token de autorización.

        Returns
        -------
        list[str] or None
            La lista de imágenes si se obtuvo correctamente, o None si
            no se pudo obtener.

        Raises
        ------
        RequestException
            Si hubo un error al realizar la solicitud HTTP.
        """
        try:
            # Realizar la solicitud HTTP para obtener la lista de
            # imágenes

            request_url: str = f"{self._settings.inventory_url}{station_id}"

            jwt_auth: str = f"JWT {auth_token}"

            request_headers = Headers(
                self._settings.base_url,
                accept=APPLICATION_JSON,
                authorization=jwt_auth,
            )

            response: Response = self.request.get(
                request_url,
                headers=request_headers.headers,
                timeout=self._settings.request_timeout,
            )

            # Extraer el contenido inventario (JSON) de la respuesta

            content: dict[str, Any] = response.json()

            # Extraer la lista de imágenes del contenido

            if "list" in content:
                return content["list"]

            # Comentario: aunque no hayan imágenes disponibles de una
            # estación, el contenido siempre es retornado por el servido
            # con la clave "list" y un valor de lista vacío. Por lo
            # tanto, se puede asumir que la lista siempre está presente
            # en el contenido y no se esperan errores de extracción de
            # del archivo JSON.

        except RequestException as exc:
            raise RequestError(
                "Error al descargar la lista de imágenes "
                f"de la estación '{station_id}'",
                self.status_code,
            ) from exc

        raise UnexpectedResponseError(
            "No se pudo obtener el inventario de imágenes "
            f"de la estación '{station_id}"
        )
