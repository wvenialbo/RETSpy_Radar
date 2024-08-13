import re
from re import Match
from typing import Any, Iterator

import requests
from requests import Response
from requests.exceptions import RequestException

from ..base.exceptions import RequestError, UnexpectedResponseError
from ..base.requests.handler_base import RequestsHandlerBase
from .settings_smn import SettingsSMN


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

    def __init__(self, settings: SettingsSMN) -> None:
        """
        Inicializa una nueva instancia de la clase RequestsSNM.

        Parameters
        ----------
        settings : SettingsSMN
            La configuración de la aplicación.
        """
        self._settings: SettingsSMN = settings

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

            REQUEST_URL: str = f"{self._settings.repository_url}{image_name}"

            REQUEST_HEADERS: dict[str, str] = self._settings.REPOSITORY_HEADERS

            response: Response = requests.get(
                REQUEST_URL, headers=REQUEST_HEADERS
            )

            # Devolver los datos de la imagen como un iterador de bytes
            # por bloques con un tamaño de 1024 bytes

            return response.iter_content(self._settings.chunk_size)

        except RequestException as exc:
            raise RequestError(
                self.status_code,
                f"No se pudo descargar la imagen '{image_name}: {exc}",
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

            REQUEST_URL: str = self._settings.radar_url

            REQUEST_HEADERS: dict[str, str] = self._settings.TOKEN_HEADERS

            response: Response = self.request.get(
                REQUEST_URL, headers=REQUEST_HEADERS
            )

            # Extraer el token de autorización de la respuesta

            match: Match[str] | None = re.search(
                self._settings.TOKEN_PATTERN, response.text
            )

            # Si se encontró el token de autorización, devolverlo

            if match:
                return match.group(1)

        except RequestException as exc:
            raise RequestError(
                self.status_code,
                f"Error al solicitar el código de autorización: {exc}",
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

            REQUEST_URL: str = f"{self._settings.radar_url}{station_id}"

            REQUEST_HEADERS: dict[str, str] = (
                self._settings.IMAGE_SET_HEADERS
                | {"authorization": f"JWT {auth_token}"}
            )

            response: Response = self.request.get(
                REQUEST_URL, headers=REQUEST_HEADERS
            )

            # Extraer el contenido inventario (JSON) de la respuesta

            CONTENT: dict[str, Any] = response.json()

            # Extraer la lista de imágenes del contenido

            if "list" in CONTENT:
                return CONTENT["list"]

            # Comentario: aunque no hayan imágenes disponibles de una
            # estación, el contenido siempre es retornado por el servido
            # con la clave "list" y un valor de lista vacío. Por lo
            # tanto, se puede asumir que la lista siempre está presente
            # en el contenido y no se esperan errores de extracción de
            # del archivo JSON.

        except RequestException as exc:
            raise RequestError(
                self.status_code,
                "Error al descargar la lista de imágenes "
                f"de la estación '{station_id}': {exc}",
            ) from exc

        raise UnexpectedResponseError(
            "No se pudo obtener el inventario de imágenes "
            f"de la estación '{station_id}"
        )
