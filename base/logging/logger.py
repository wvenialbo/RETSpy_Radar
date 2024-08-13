from logging import DEBUG, Logger, StreamHandler, getLogger

from .formatter import LoggerFormatter

_logger: Logger | None = None


def instance_logger(name: str, logger_level: int, stream_level: int) -> Logger:
    """
    Instancia un objeto de registro de eventos.

    Crea un objeto de registro de eventos para que registre todos los
    eventos de nivel 'logger_level' o superior y muestre en la consola
    de usuario todos los eventos de nivel 'stream_level' o superior.

    Parameters
    ----------
    name : str
        Nombre del objeto de registro de eventos.
    logger_level : int, optional
        Nivel de los eventos a registrar.
    stream_level : int, optional
        Nivel de los eventos a mostrar en la consola de usuario.

    Returns
    -------
    Logger
        El objeto de registro de eventos.
    """
    # Crear un objeto de registro de eventos y configurarlo para que
    # registre todos los eventos de nivel 'logger_level' o superior,
    # por defecto 'DEBUG'

    logger: Logger = getLogger(name)
    logger.setLevel(logger_level)

    # Crear un manejador de flujo de salida y configurarlo para que
    # registre todos los eventos de nivel 'stream_level' o superior,
    # por defecto 'DEBUG', en la consola de usuario

    handler = StreamHandler()
    handler.setLevel(stream_level)

    # Crear un formateador de registro de eventos y configurarlo para
    # que muestre la fecha y hora de los eventos, el nivel del evento
    # y el mensaje del evento. Asignar el formateador al manejador de
    # flujo de salida y el manejador al objeto de registro de eventos

    formatter = LoggerFormatter()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_logger(
    name: str, logger_level: int = DEBUG, stream_level: int = DEBUG
) -> Logger:
    """
    Obtiene un único objeto de registro de eventos.

    Retorna un objeto de registro de eventos para que registre todos los
    eventos de nivel 'logger_level' o superior y muestre en la consola
    de usuario todos los eventos de nivel 'stream_level' o superior.

    Parameters
    ----------
    name : str
        Nombre del objeto de registro de eventos.
    logger_level : int, optional
        Nivel de los eventos a registrar, por defecto 'DEBUG'.
    stream_level : int, optional
        Nivel de los eventos a mostrar en la consola de usuario,
        por defecto 'DEBUG'.

    Returns
    -------
    Logger
        El objeto de registro de eventos.
    """
    # Si no se ha creado un objeto de registro de eventos, crear uno con
    # el nombre 'name' y los niveles 'logger_level' y 'stream_level'.
    # Luego, almacenar el objeto de registro de eventos y devolverlo.

    global _logger

    if _logger is None:
        _logger = instance_logger(name, logger_level, stream_level)

    return _logger
