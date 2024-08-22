from .request_base import RequestBase


class RequestsHandlerBase:
    """
    Maneja y realiza solicitudes HTTP.

    Attributes
    ----------
    _request : RequestsBase
        Objeto para realizar solicitudes HTTP.

    Properties
    ----------
    request : RequestsBase
        Obtiene el objeto que realiza solicitudes HTTP.
    status_code : int
        Obtiene el código de estado de la última solicitud HTTP.
    """

    def __init__(self, request: RequestBase | None = None) -> None:
        """
        Inicializa una nueva instancia del manejador de solicitudes.

        Parameters
        ----------
        request : RequestsBase, optional
            Objeto para realizar solicitudes HTTP.
        """
        self._request: RequestBase = request or RequestBase()

    @property
    def request(self) -> RequestBase:
        """
        Obtiene el objeto que realiza solicitudes HTTP.

        Returns
        -------
        RequestsBase
            El objeto que realiza solicitudes HTTP.
        """
        return self._request

    @property
    def status_code(self) -> int:
        """
        Obtiene el código de estado de la última solicitud HTTP.

        Returns
        -------
        int
            El código de estado de la última solicitud HTTP.
        """
        return self._request.status_code
