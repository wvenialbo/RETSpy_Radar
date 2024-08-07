import json
import os
import re
import time
from datetime import datetime, timedelta
from re import Match
from typing import Any, Iterator

import requests
from requests import Response
from requests.exceptions import RequestException

SITE_URL: str = "https://www.smn.gob.ar/radar"
LIST_URL: str = "https://ws1.smn.gob.ar/v1/images/radar/"
REPOSITORY_URL: str = "https://estaticos.smn.gob.ar/vmsr/radar/"
CREDENTIAL_PATH: str = "credentials.json"

WAIT_NEXT_REQUEST: float = 0.3  # seconds
WAIT_NEXT_AUTHORIZATION: float = 1.0  # seconds
MINIMUM_SCAN_PERIOD: float = 1.0  # seconds
DEFAULT_SCAN_PERIOD: int = 2  # minutes

BASE_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    ),
    "accept-language": (
        "en-GB;q=0.9,en-US;q=0.8,en;q=0.7," "es-ES;q=0.8,es-PY;q=0.7,es;q=0.6,"
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


AUTH_HEADERS: dict[str, str] = {
    "credentials": "omit",
    "priority": "u=0, i",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}


LIST_HEADERS: dict[str, str] = {
    "accept": "application/json",
    "authorization": "JWT {token}",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
}


IMAGE_HEADERS: dict[str, str] = {
    "accept": "image/png",
    "priority": "i",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
}


COMMON_HEADERS: dict[str, str] = {
    "credentials": "include",
    "sec-fetch-site": "same-site",
}


class RobotSmnRadar:
    """
    Robot scraper de imágenes de radar del SMN.

    El robot scraper de imágenes de radar del Servicio Meteorológico
    Nacional (SMN) argentino permite descargar imágenes de radar de las
    estaciones del SMN y guardarlas en un repositorio local. El robot
    realiza solicitudes HTTP a la página del radar del SMN para obtener
    un token de autorización, luego obtiene la lista de imágenes de una
    estación y descarga las imágenes de radar en el repositorio local.

    Attributes
    ----------
    local_repository_path : str
        La ruta del repositorio local donde se guardarán las imágenes.
    scan_period_minutes : int
        El período de escaneo en minutos.
    minimum_wait_time_seconds : float
        El tiempo mínimo de espera en segundos.
    authorization_token : str
        El token de autorización.

    Methods
    -------
    download_image(image_name) -> Iterator[Any]
        Descarga una imagen de radar.
    get_authorization() -> str or None
        Obtiene un token de autorización.
    get_authorization_token(first_call) -> str or None
        Obtiene un token de autorización.
    get_image_list(station_id, token) -> list[str] or None
        Obtiene la lista de imágenes de una estación.
    load_authorization_token(credentials_path) -> str or None
        Obtiene un token de autorización de un archivo de credenciales.
    renew_authorization() -> str or None
        Renueva un token de autorización.
    retrieve(station_ids, initial_date, final_date) -> None
        Recupera las imágenes de radar del SMN en un rango de fechas.
    run(station_ids) -> None
        Ejecuta el robot scraper de imágenes de radar del SMN.
    save_authorization_token(credentials_path, token) -> None
        Guarda un token de autorización en un archivo de credenciales.
    save_image(image_name, image_data) -> None
        Guarda una imagen de radar en el repositorio local.
    
    Raises
    ------
    ValueError
        Si la ruta del repositorio local no es válida o el período
        de escaneo no es válido.
    """

    def __init__(
        self,
        local_repository_path: str,
        scan_period_minutes: int = DEFAULT_SCAN_PERIOD,
        minimum_wait_time_seconds: float = MINIMUM_SCAN_PERIOD,
    ) -> None:
        """
        Inicializa el robot scraper de imágenes de radar del SMN.

        Parameters
        ----------
        local_repository_path : str
            La ruta del repositorio local donde se guardarán las
            imágenes.
        scan_period_minutes : int, optional
            El período de escaneo en minutos, por defecto 10.
        minimum_wait_time_seconds : float, optional
            El tiempo mínimo de espera en segundos, por defecto 1.

        Raises
        ------
        ValueError
            Si la ruta del repositorio local no es válida o el período
            de escaneo no es válido.
        """
        # Verificar que la ruta del repositorio local sea válida
        if not local_repository_path:
            raise ValueError("La ruta del repositorio local no es válida")

        # Verificar que el período de escaneo sea válido
        if scan_period_minutes <= 0 or scan_period_minutes > 60:
            raise ValueError(
                "El período de escaneo debe ser mayor a cero "
                "y menor o igual a 60 minutos"
            )

        self.minimum_wait_time_seconds: float = minimum_wait_time_seconds
        self.scan_period_minutes: int = scan_period_minutes
        self.local_repository_path: str = local_repository_path
        self.authorization_token: str | None = None

    def load_authorization_token(self, credentials_path: str) -> str | None:
        """
        Obtiene un token de autorización de un archivo de credenciales.

        Parameters
        ----------
        credentials_path : str
            La ruta del archivo de credenciales.

        Returns
        -------
        str or None
            El token de autorización si se obtuvo correctamente, o None
            si no se pudo obtener
        """
        try:
            # Leer el token de autorización del archivo de credenciales
            with open(credentials_path, "r") as file:
                data = json.load(file)

                return data.get("token")

        except (FileNotFoundError, IOError, OSError):
            # Notificar que no se encontró el archivo de credenciales
            print(f"El archivo {credentials_path} no fue encontrado.")

        except json.JSONDecodeError:
            # Notificar que hubo un error al parsear el archivo JSON
            print(f"Error al parsear el archivo JSON {credentials_path}.")

        # Retornar None si no se encontró el archivo de credenciales o
        # hubo un error al parsear el archivo JSON
        return None

    def save_authorization_token(
        self, credentials_path: str, token: str
    ) -> None:
        """
        Guarda un token de autorización en un archivo de credenciales.

        Parameters
        ----------
        credentials_path : str
            La ruta del archivo de credenciales.
        token : str
            El token de autorización.
        """
        try:
            # Crear un diccionario con el token
            data: dict[str, str] = {"token": token}

            # Escribir el diccionario en el archivo JSON
            with open(credentials_path, "w") as file:
                json.dump(data, file, indent=4)

            print(
                f"Credenciales guardadas exitosamente en '{credentials_path}'"
            )

        except (IOError, OSError, TypeError) as exc:
            print(f"Error al guardar el token: {exc}")

    def get_authorization_token(self, first_call: bool) -> str | None:
        """
        Obtiene un token de autorización.

        Realiza una solicitud HTTP a la página del radar del SMN y
        extrae el token de autorización de la respuesta. El token de
        autorización permite acceder a las imágenes de radar de las
        estaciones del Servicio Meteorológico Nacional (SMN) argentino.

        Parameters
        ----------
        first_call : bool
            Indica si es la primera llamada a la función.

        Returns
        -------
        str or None
            El token de autorización si se obtuvo correctamente, o None
            si no se pudo obtener.

        Raises
        ------
        RequestException
            Si hubo un error al realizar la solicitud HTTP.
        """
        try:
            HEADERS: dict[str, str] = BASE_HEADERS | AUTH_HEADERS

            # Realizar la solicitud HTTP para obtener la autorization
            response: Response = requests.get(SITE_URL, headers=HEADERS)

            # Levantar una excepción si hubo un error en la solicitud
            response.raise_for_status()

            # Extraer el token de autorización de la respuesta
            CONTENT: str = response.text
            PATTERN: str = r"localStorage\.setItem\('token',\s*'([^']+)'\);"
            match: Match[str] | None = re.search(PATTERN, CONTENT)

            # Si se encontró el token de autorización, devolverlo
            if match:
                print(
                    "Autorización obtenida correctamente"
                    if first_call
                    else "Autorización renovada correctamente"
                )

                return match.group(1)

        except RequestException as exc:
            print(f"Error al solicitar la autorization del SMN: {exc}")

            # Levantar una excepción si hubo un error en la solicitud
            raise exc

        # Si no se pudo obtener la autorización, devolver None
        print("No se pudo obtener la autorización del SMN")

        return None

    def get_authorization(self) -> str | None:
        """
        Obtiene un token de autorización.

        Obtiene un token de autorización del Servicio Meteorológico
        Nacional (SMN) argentino. El token de autorización permite
        acceder a las imágenes de radar de las estaciones del SMN.

        Se intenta leer el token de autorización de un archivo de
        credenciales. Si no se pudo leer el token de autorización del
        archivo de credenciales, se obtiene un nuevo token de
        autorización desde el sitio web del SMN.

        Returns
        -------
        str or None
            El token de autorización si se obtuvo correctamente, o None
            si no se pudo obtener.
        """
        token: str | None = self.load_authorization_token(CREDENTIAL_PATH)

        if token is None:
            token = self.get_authorization_token(True)

            if token is not None:
                self.save_authorization_token(CREDENTIAL_PATH, token)

        return token

    def renew_authorization(self) -> str | None:
        """
        Renueva un token de autorización.

        Renueva un token de autorización del Servicio Meteorológico
        Nacional (SMN) argentino. El token de autorización permite
        acceder a las imágenes de radar de las estaciones del SMN.

        Se obtiene un nuevo token de autorización desde el sitio web
        del SMN.

        Returns
        -------
        str or None
            El token de autorización si se obtuvo correctamente, o None
            si no se pudo obtener.
        """
        token: str | None = self.get_authorization_token(False)

        if token is not None:
            self.save_authorization_token(CREDENTIAL_PATH, token)

        return token

    def get_image_list(self, station_id: str, token: str) -> list[str] | None:
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
            La lista de imágenes si se obtuvo correctamente, o None si no
            se pudo obtener.

        Raises
        ------
        RequestException
            Si hubo un error al realizar la solicitud HTTP.
        """
        try:
            STATION_URL: str = f"{LIST_URL}{station_id}"

            headers: dict[str, str] = (
                BASE_HEADERS | LIST_HEADERS | COMMON_HEADERS
            )
            headers["authorization"] = f"JWT {token}"

            # print(f"Descargando datos de la estación '{station_id}'")

            # Realizar la solicitud HTTP para obtener la lista de
            # imágenes
            response: Response = requests.get(STATION_URL, headers=headers)

            # Levantar una excepción si hubo un error en la solicitud
            response.raise_for_status()

            # Parsear el contenido JSON
            CONTENT: dict[str, Any] = response.json()

            # Extraer la información de la estación y el producto
            # if "id" in CONTENT:
            #     print(f"ID de la estación : {CONTENT['id']}")

            # if "radar" in CONTENT:
            #     print(f"ID del radar      : {CONTENT['radar']}")

            # if "product" in CONTENT:
            #     print(f"Producto          : {CONTENT['product']}")

            # Extraer la lista de imágenes de la respuesta
            if "list" in CONTENT:
                return CONTENT["list"]

        except RequestException as exc:
            print(
                "Error al descargar la lista de imágenes "
                f"de la estación '{station_id}': {exc}"
            )

            # Levantar una excepción si hubo un error en la solicitud
            raise exc

        # Si no se pudo obtener la lista de imágenes, devolver None
        print(
            "No se pudo obtener la lista de imágenes "
            f"de la estación '{station_id}"
        )

        return None

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
        RequestException
            Si hubo un error al realizar la solicitud HTTP.
        """
        try:
            IMAGE_URL: str = f"{REPOSITORY_URL}{image_name}"
            HEADERS: dict[str, str] = (
                BASE_HEADERS | IMAGE_HEADERS | COMMON_HEADERS
            )

            # Realizar la solicitud HTTP para descargar la imagen
            response: Response = requests.get(IMAGE_URL, headers=HEADERS)

            # Levantar una excepción si hubo un error en la solicitud
            response.raise_for_status()

            # Devolver los datos de la imagen
            return response.iter_content(1024)

        except RequestException as exc:
            print(f"Error al descargar la imagen '{image_name}': {exc}")

            print(f"No se pudo descargar la imagen '{image_name}'")

            # Levantar una excepción si hubo un error en la solicitud
            raise exc

    def save_image(self, image_name: str, image_data: Iterator[Any]) -> None:
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
            IMAGE_PATH: str = f"{self.local_repository_path}{image_name}"

            # Guardar la imagen en el disco
            with open(IMAGE_PATH, "wb") as file:
                for chunk in image_data:
                    file.write(chunk)

            print(f"Imagen '{image_name}' guardada correctamente")

        except (IOError, OSError, TypeError) as exc:
            print(f"Error al guardar la imagen: {exc}")


    def run(self, station_ids: list[str]) -> None:
        """
        Ejecuta el robot scraper de imágenes de radar del SMN.

        Ejecuta el robot scraper de imágenes de radar del Servicio
        Meteorológico Nacional (SMN) argentino para descargar imágenes
        de radar de las estaciones del SMN y guardarlas en un repositorio
        local. El robot realiza solicitudes HTTP a la página del radar
        del SMN para obtener un token de autorización, luego obtiene la
        lista de imágenes de cada estación y descarga las imágenes de
        radar en el repositorio local.

        Parameters
        ----------
        station_ids : list[str]
            La lista de IDs de las estaciones de radar.

        Raises
        ------
        RequestException
            Si hubo un error al realizar una solicitud HTTP.
        """
        abort_operation: bool = False

        try:
            # Obtener el token de autorización
            self.authorization_token = self.get_authorization()

            # Abortar la operación si no se pudo obtener el token de
            # autorización
            if self.authorization_token is None:
                self.authorization_token = ""
                abort_operation = True

        except RequestException:
            # Abortar la operación si no se pudo obtener el token de
            # autorización debido a un error en la solicitud
            print("No se pudo iniciar el scraper de imágenes de radar del SMN")

            self.authorization_token = ""
            abort_operation = True

        # Crear el directorio del repositorio local si no existe
        if not abort_operation:
            os.makedirs(self.local_repository_path, exist_ok=True)

        count: int = 0

        pendent: set[str] = set()
        retry: set[str] = set()

        while not abort_operation:
            start_time: float = time.time()

            # Obtener lista de imágenes de radar
            print("Descargando inventario de las estaciones")

            for station_id in station_ids:
                try:
                    # Esperar un tiempo para no saturar el servidor
                    time.sleep(WAIT_NEXT_REQUEST)

                    images = self.get_image_list(
                        station_id, self.authorization_token
                    )

                    # Abortar la operación si no se pudo obtener la
                    # lista de imágenes
                    if images is None:
                        abort_operation = True
                        break

                    pendent.update(images)

                except RequestException:
                    # Esperar un tiempo y obtener un nuevo token de
                    # autorización
                    time.sleep(WAIT_NEXT_AUTHORIZATION)

                    try:
                        self.authorization_token = self.renew_authorization()

                        # Abortar la operación si no se pudo renovar el
                        # token de autorización
                        if self.authorization_token is None:
                            self.authorization_token = ""
                            abort_operation = True

                            break

                    except RequestException:
                        # Abortar la operación si no se pudo obtener un
                        # nuevo token de autorización debido a un error
                        # en la solicitud
                        abort_operation = True
                        self.authorization_token = ""

                        break

                    # Volver a (*) o a (+) según corresponda
                    continue

            # Abortar la operación si no se pudo obtener la lista de
            # imágenes o hubo algún error en la solicitud
            if abort_operation:
                break

            # Actualizar el conjunto de archivos pendientes,
            # removiendo los archivos que ya se encuentran
            # en el repositorio local
            for image_name in pendent.copy():
                if os.path.exists(f"{self.local_repository_path}{image_name}"):
                    pendent.remove(image_name)

            # Descargar y guardar cada imagen pendiente
            for image_name in pendent.copy():
                try:
                    count += 1

                    print(f"{count:5d}. Descargando imagen '{image_name}'")

                    # Esperar un tiempo para no saturar el servidor
                    time.sleep(WAIT_NEXT_REQUEST)

                    image_data: Iterator[Any] = self.download_image(image_name)

                    pendent.remove(image_name)

                    self.save_image(image_name, image_data)

                except RequestException:
                    # Try again one more time in the next scan period in
                    # case of error in the request
                    if image_name in retry:
                        retry.remove(image_name)
                        pendent.remove(image_name)
                        continue

                    retry.add(image_name)

                except Exception:
                    # Abortar la operación si no se pudo acceder al
                    # repositorio local
                    print(f"Error al guardar la imagen '{image_name}'")

                    abort_operation = True
                    break

            # Abortar la operación si no se pudo obtener la imagen,
            # hubo algún error en la solicitud o no se pudo guardar
            # la imagen
            if abort_operation:
                break

            end_time: float = time.time()

            # Ajustar el tiempo de espera para el siguiente periodo
            # de escaneo, restando el tiempo transcurrido desde el
            # inicio del periodo hasta el final de la descarga de
            # las imágenes
            elapsed_time: float = end_time - start_time
            scan_period: int = self.scan_period_minutes * 60
            wait_time: float = scan_period - elapsed_time

            if wait_time <= self.minimum_wait_time_seconds:
                wait_time = self.minimum_wait_time_seconds

            # Esperar el siguiente periodo de escaneo
            print("Esperando el siguiente periodo")

            time.sleep(wait_time)

        # Notificar si se abortó la operación
        if abort_operation:
            print("Se aborta la ejecución del programa")
            print("Intente nuevamente más tarde")

    def retrieve(
        self, station_ids: list[str], initial_date: str, final_date: str
    ) -> None:
        """
        Recupera las imágenes de radar del SMN en un rango de fechas.

        Recupera las imágenes de radar del Servicio Meteorológico
        Nacional (SMN) argentino de las estaciones del SMN requeridas en
        un rango de fechas especificado. Las imágenes se guardan en el
        repositorio local especificado por la ruta del repositorio
        local.

        Parameters
        ----------
        station_ids : list[str]
            La lista de IDs de las estaciones de radar.
        initial_date : str
            La fecha y hora de inicio del rango de fechas.
        final_date : str
            La fecha y hora de fin del rango de fechas.

        Raises
        ------
        ValueError
            Si la fecha de inicio o la fecha de fin no son válidas.
        """

        count: int = 0

        try:
            # Verificar que la fecha de inicio sea válida
            if not initial_date:
                raise ValueError("La fecha de inicio no es válida")

            # Verificar que la fecha de fin sea válida
            if not final_date:
                raise ValueError("La fecha de fin no es válida")

            DATE_PATTERN = "%Y%m%d_%H%M%S"

            # Parsear fechas a objetos datetime
            start_time: datetime = datetime.strptime(
                initial_date, DATE_PATTERN
            )
            end_time: datetime = datetime.strptime(final_date, DATE_PATTERN)

            # Crear secuencia con intervalos de step segundos
            for station_id in station_ids:
                print(
                    "Descargando imágenes de radar "
                    f"de la estación {station_id}"
                )

                current_time: datetime = start_time
                while current_time <= end_time:
                    date_stamp: str = current_time.strftime(DATE_PATTERN)

                    filename: str = f"{station_id}_ZH_CMAX_{date_stamp}Z"

                    image_name: str = f"{filename}.png"

                    current_time += timedelta(seconds=1)

                    if os.path.exists(
                        f"{self.local_repository_path}{image_name}"
                    ):
                        continue

                    try:
                        image_data: Iterator[Any] = self.download_image(
                            image_name
                        )

                        self.save_image(image_name, image_data)

                    except RequestException:
                        continue

                    count += 1

                    print(f"{count:5d}. Descargando imagen '{image_name}'")

        except ValueError as exc:
            print(f"Error al recuperar las imágenes de radar: {exc}")

            return
