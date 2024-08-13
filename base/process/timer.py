from datetime import datetime, timedelta

from ..utils.timing import timing


class ProcessTimer:
    """
    Temporizador de proceso.

    Controla el tiempo de ejecución de un proceso y el periodo de espera
    entre ejecuciones del bucle del proceso de recolección de datos.
    """

    def __init__(
        self, start_time: datetime, end_time: datetime, scan_period: timedelta
    ) -> None:
        """
        Inicializa un nuevo temporizador de proceso.

        Inicializa el temporizador de proceso de recolección de datos y
        establece el tiempo de inicio de ejecución de la rutina, el
        tiempo de fin de ejecución de la rutina y el periodo de espera
        entre ejecuciones del bucle del proceso de recolección de datos.

        Parameters
        ----------
        start_time : datetime
            El tiempo de inicio de ejecución de la rutina.
        end_time : datetime
            El tiempo de fin de ejecución de la rutina.
        scan_period : timedelta
            El periodo de espera entre ejecuciones del bucle del proceso
            de recolección de datos.
        """
        self._end_time: datetime = end_time
        self._next_time: datetime = start_time
        self._scan_period: timedelta = scan_period
        self._start_time: datetime = start_time

    def elapsed_time(self) -> timedelta:
        """
        Obtiene el tiempo transcurrido en el proceso.

        Obtiene el tiempo transcurrido desde el inicio de ejecución de
        la rutina.

        Returns
        -------
        timedelta
            El tiempo transcurrido desde el inicio de ejecución de la
            rutina.
        """
        current_time: datetime = timing.current_time()

        return current_time - self._start_time

    def lapse(self) -> timedelta:
        """
        Obtiene el tiempo transcurrido en el ciclo actual.

        Obtiene el tiempo transcurrido desde el inicio de ejecución del
        ciclo actual de la rutina.

        Returns
        -------
        timedelta
            El tiempo transcurrido desde el inicio de ejecución del
            ciclo actual de la rutina.
        """
        current_time: datetime = timing.current_time()

        return current_time - self._next_time + self._scan_period

    def rewind(self) -> None:
        """
        Establece el temporizador en el inicio del ciclo actual.

        Retrocede el temporizador al inicio del la ejecución del ciclo
        actual de la rutina.
        """
        self._next_time -= self._scan_period

    def start(self) -> None:
        """
        Espera el tiempo de inicio de ejecución.

        Espera hasta que sea el tiempo de inicio de ejecución de la
        rutina.
        """
        timing.wait_until(self._start_time)

    def stop(self) -> bool:
        """
        Comprueba si el tiempo de fin de ejecución ha llegado.

        Comprueba si el tiempo de fin de ejecución de la rutina ha
        llegado y espera hasta que sea el tiempo de inicio de ejecución
        del siguiente ciclo de la rutina.

        Returns
        -------
        bool
            True si el tiempo de fin de ejecución de la rutina ha
            llegado, False en caso contrario.
        """
        # Comprobar si el tiempo de fin de ejecución ha llegado, y
        # devolver True en caso positivo.

        current_time: datetime = timing.current_time()

        if current_time >= self._end_time:
            return True

        # En caso contrario, esperar hasta que sea el tiempo de inicio
        # de ejecución del siguiente ciclo de la rutina, ajustar el
        # tiempo de inicio del siguiente ciclo y devolver False

        timing.wait_until(self._next_time)

        self._next_time += self._scan_period

        return False
