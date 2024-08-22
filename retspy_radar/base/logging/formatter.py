import logging
from logging import Formatter, LogRecord

BLUE = "\x1b[38;5;19m"
LIGHT_BLUE = "\x1b[38;5;21m"
GREEN = "\x1b[38;5;40m"
LIGHT_GREEN = "\x1b[38;5;46m"
YELLOW = "\x1b[38;5;220m"
LIGHT_YELLOW = "\x1b[38;5;226m"
ORANGE = "\x1b[38;5;202m"
LIGHT_ORANGE = "\x1b[38;5;214m"
RED = "\x1b[38;5;1m"
LIGHT_RED = "\x1b[38;5;9m"
RESET = "\x1b[0m"

COLOR: dict[int, str] = {
    logging.DEBUG: BLUE,
    logging.INFO: GREEN,
    logging.WARNING: YELLOW,
    logging.ERROR: ORANGE,
    logging.CRITICAL: LIGHT_RED,
}

HEAD = "%(asctime)s - "
LEVEL = "%(levelname)s"
MSG = " - %(message)s"

FORMAT: dict[int, str] = {
    level: HEAD + COLOR[level] + LEVEL + RESET + MSG for level in COLOR
}


class LoggerFormatter(Formatter):
    """
    Formateador de registros de log que colorea el nivel de log.
    """

    formatter: dict[int, Formatter] = {
        level: Formatter(FORMAT[level]) for level in COLOR
    }

    def format(self, record: LogRecord) -> str:
        """
        Formatea un registro de log.

        Parameters
        ----------
        record : LogRecord
            El registro de log a formatear.

        Returns
        -------
        str
            El registro de log formateado.
        """
        # Obtener el formateador correspondiente al nivel del registro,
        # formatear el registro y devolver la cadena resultante.

        formatter: Formatter = self.formatter[record.levelno]

        return formatter.format(record)
