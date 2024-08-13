from typing import Any, Callable

from requests import Response, Session


class RequestsBase:
    """
    Realiza solicitudes HTTP.

    Attributes
    ----------
    _base_url : str
        La URL base de las solicitudes.
    _headers : dict[str, Any]
        Los encabezados de las solicitudes.
    _session : Session
        La sesión de solicitudes.
    _status_code : int
        El código de estado de la última solicitud HTTP.

    Methods
    -------
    close() -> None
        Cierra la sesión de solicitudes.
    delete(url, headers = None, **kwargs) -> Response
        Realiza una solicitud HTTP DELETE.
    get(url, headers = None, **kwargs) -> Response
        Realiza una solicitud HTTP GET.
    head(url, headers = None, **kwargs) -> Response
        Realiza una solicitud HTTP HEAD.
    options(url, headers = None, **kwargs) -> Response
        Realiza una solicitud HTTP OPTIONS.
    patch(url, headers = None, **kwargs) -> Response
        Realiza una solicitud HTTP PATCH.
    post(url, headers = None, **kwargs) -> Response
        Realiza una solicitud HTTP POST.
    put(url, headers = None, **kwargs) -> Response
        Realiza una solicitud HTTP PUT.

    Properties
    ----------
    status_code : int
        Obtiene el código de estado de la última solicitud HTTP.
    """

    def __init__(
        self, base_url: str = "", headers: dict[str, Any] | None = None
    ) -> None:
        """
        Inicializa una nueva instancia de la clase RequestsBase.

        Parameters
        ----------
        base_url : str, optional
            La URL base de las solicitudes, por defecto es una cadena vacía.
        headers : dict[str, Any], optional
            Los encabezados de las solicitudes, por defecto es None.
        """
        self._base_url: str = base_url
        self._headers: dict[str, Any] = headers or dict()
        self._session = Session()
        self._status_code: int = 0

    def close(self) -> None:
        """
        Cierra la sesión de solicitudes.
        """
        self._session.close()

    def delete(
        self, url: str, headers: dict[str, Any] | None = None, **kwargs: Any
    ) -> Response:
        """
        Realiza una solicitud HTTP DELETE.

        Parameters
        ----------
        url : str
            La URL de la solicitud.
        headers : dict[str, Any], optional
            Los encabezados de la solicitud, por defecto es None.
        **kwargs : Any
            Argumentos adicionales de la solicitud.

        Returns
        -------
        Response
            La respuesta de la solicitud.
        """
        return self._dispatch(self._session.delete, url, headers, **kwargs)

    def get(
        self, url: str, headers: dict[str, Any] | None = None, **kwargs: Any
    ) -> Response:
        """
        Realiza una solicitud HTTP GET.

        Parameters
        ----------
        url : str
            La URL de la solicitud.
        headers : dict[str, Any], optional
            Los encabezados de la solicitud, por defecto es None.
        **kwargs : Any
            Argumentos adicionales de la solicitud.

        Returns
        -------
        Response
            La respuesta de la solicitud.
        """
        return self._dispatch(self._session.get, url, headers, **kwargs)

    def head(
        self, url: str, headers: dict[str, Any] | None = None, **kwargs: Any
    ) -> Response:
        """
        Realiza una solicitud HTTP HEAD.

        Parameters
        ----------
        url : str
            La URL de la solicitud.
        headers : dict[str, Any], optional
            Los encabezados de la solicitud, por defecto es None.
        **kwargs : Any
            Argumentos adicionales de la solicitud.

        Returns
        -------
        Response
            La respuesta de la solicitud.
        """
        return self._dispatch(self._session.head, url, headers, **kwargs)

    def options(
        self, url: str, headers: dict[str, Any] | None = None, **kwargs: Any
    ) -> Response:
        """
        Realiza una solicitud HTTP OPTIONS.

        Parameters
        ----------
        url : str
            La URL de la solicitud.
        headers : dict[str, Any], optional
            Los encabezados de la solicitud, por defecto es None.
        **kwargs : Any
            Argumentos adicionales de la solicitud.

        Returns
        -------
        Response
            La respuesta de la solicitud.
        """
        return self._dispatch(self._session.options, url, headers, **kwargs)

    def patch(
        self, url: str, headers: dict[str, Any] | None = None, **kwargs: Any
    ) -> Response:
        """
        Realiza una solicitud HTTP PATCH.

        Parameters
        ----------
        url : str
            La URL de la solicitud.
        headers : dict[str, Any], optional
            Los encabezados de la solicitud, por defecto es None.
        **kwargs : Any
            Argumentos adicionales de la solicitud.

        Returns
        -------
        Response
            La respuesta de la solicitud.
        """
        return self._dispatch(self._session.patch, url, headers, **kwargs)

    def post(
        self, url: str, headers: dict[str, Any] | None = None, **kwargs: Any
    ) -> Response:
        """
        Realiza una solicitud HTTP POST.

        Parameters
        ----------
        url : str
            La URL de la solicitud.
        headers : dict[str, Any], optional
            Los encabezados de la solicitud, por defecto es None.
        **kwargs : Any
            Argumentos adicionales de la solicitud.

        Returns
        -------
        Response
            La respuesta de la solicitud.
        """
        return self._dispatch(self._session.post, url, headers, **kwargs)

    def put(
        self, url: str, headers: dict[str, Any] | None = None, **kwargs: Any
    ) -> Response:
        """
        Realiza una solicitud HTTP PUT.

        Parameters
        ----------
        url : str
            La URL de la solicitud.
        headers : dict[str, Any], optional
            Los encabezados de la solicitud, por defecto es None.
        **kwargs : Any
            Argumentos adicionales de la solicitud.

        Returns
        -------
        Response
            La respuesta de la solicitud.
        """
        return self._dispatch(self._session.put, url, headers, **kwargs)

    def _dispatch(
        self,
        request: Callable[..., Response],
        url: str,
        headers: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> Response:
        """
        Realiza una solicitud HTTP.

        Parameters
        ----------
        request : Callable[..., Response]
            La función de solicitud HTTP.
        url : str
            La URL de la solicitud.
        headers : dict[str, Any], optional
            Los encabezados de la solicitud, por defecto es None.
        **kwargs : Any
            Argumentos adicionales de la solicitud.

        Returns
        -------
        Response
            La respuesta de la solicitud.
        """
        target_url: str = self._base_url + url
        headers = headers or self._headers

        response: Response = request(target_url, headers, **kwargs)

        self._status_code = response.status_code

        response.raise_for_status()

        return response

    @property
    def status_code(self) -> int:
        """
        Obtiene el código de estado de la última solicitud HTTP.

        Returns
        -------
        int
            El código de estado de la última solicitud HTTP.
        """
        return self._status_code
