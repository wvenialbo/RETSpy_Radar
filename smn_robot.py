"""
Este script es el punto de entrada del Robot de descarga de imágenes de
radar del Servicio Meteorológico Nacional (SMN) argentino.

Si no se proveen argumentos, se utilizarán los valores por defecto.
Para más información, ejecute el script con la opción -h o --help.

"""

import argparse
from smn_radar import RobotSmnRadar, DEFAULT_SCAN_PERIOD

DEFAULT_REPO_PATH: str = "./"
DEFAULT_STATIONS: list[str] = ["RMA3_240", "RMA4_240", "RMA5_240", "RMA8_240", ]

def main() -> None:
    parser = argparse.ArgumentParser(description='SMN Radar Robot')

    parser.add_argument(
        "-p"
        "--path",
        dest="path",
        type=str,
        help='Ruta del directorio repositorio',
        default=DEFAULT_REPO_PATH,
    )
    parser.add_argument(
        "-t",
        "--period",
        dest="period",
        type=int,
        help='Periodo de tiempo de escaneo en segundos',
        default=DEFAULT_SCAN_PERIOD,
    )
    parser.add_argument(
        "-s",
        "--stations",
        dest="stations",
        nargs='+',
        type=str,
        help='Lista de identificadores de estaciones',
        default=DEFAULT_STATIONS,
    )

    args: argparse.Namespace = parser.parse_args()
    
    local_repository_path: str=args.path or DEFAULT_REPO_PATH
    scan_period_minutes: int=args.period or DEFAULT_SCAN_PERIOD
    station_ids: list[str]=args.stations or DEFAULT_STATIONS

    # Crear una instancia de la clase con los argumentos proporcionados
    robot = RobotSmnRadar(local_repository_path, scan_period_minutes)

    # Llamar al método run con la lista de identificadores
    robot.run(station_ids)

if __name__ == '__main__':
    main()
