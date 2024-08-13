import time


class ProcessSleep:
    """
    Clase para simular un proceso de espera.
    """

    def __init__(self, sleep_time: float) -> None:
        """
        Inicializa una nueva instancia de la clase ProcessSleep.

        Parameters
        ----------
        sleep_time : float
            El tiempo de espera en segundos.
        """
        self.sleep_time: float = sleep_time

    def run(self) -> None:
        """
        Ejecuta el proceso de espera.
        """
        time.sleep(self.sleep_time)
