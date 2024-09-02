import os
import platform

from ..package_info import UAG_NAME, pkg_info

IMAGE_JPEG: str = "image/jpeg"
IMAGE_PNG: str = "image/png"
TEXT_HTML: str = "text/html"
APPLICATION_JSON: str = "application/json"


class Headers:

    def __init__(
        self,
        referrer: str,
        *,
        accept: str = TEXT_HTML,
        authorization: str = "",
    ) -> None:
        """Inicializa una nueva instancia de la clase Headers.

        Parameters
        ----------
        referrer : str
            El valor de la cabecera "referer".
        accept : str, optional
            El valor de la cabecera "accept", por defecto es "text/html".
        authorization : str, optional
            El valor de la cabecera "authorization", por defecto es "".
        """
        USER_AGENT: str = (
            f"{UAG_NAME}-Indexer/{pkg_info.version} "
            f"({platform.system()} {os.name.upper()} "
            f"{platform.release()}/{platform.version()})"
        )
        ACCEPT_LANGUAGE: str = (
            "en-GB;q=0.9,en-US;q=0.8,en;q=0.7,"
            "es-ES;q=0.8,es-PY;q=0.7,es;q=0.6"
        )
        AUTHORIZATION: dict[str, str] = (
            {"authorization": authorization} if authorization else {}
        )

        self._headers: dict[str, str] = {
            "accept": accept,
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": ACCEPT_LANGUAGE,
            "cache-control": "no-cache",
            "connection": "keep-alive",
            "pragma": "no-cache",
            "referer": referrer,
            "user-agent": USER_AGENT,
        } | AUTHORIZATION

    @property
    def headers(self) -> dict[str, str]:
        """Devuelve los encabezados de la solicitud."""
        return self._headers
