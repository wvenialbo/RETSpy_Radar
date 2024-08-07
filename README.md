## README

# SMN Radar Robot

Este repositorio contiene una aplicación para descargar imágenes de radar y mosaicos del Servicio Meteorológico Nacional (SMN) argentino. La aplicación consta de una clase principal y dos módulos ejecutables desde la consola.

## Descripción

El SMN Radar Robot es un scraper diseñado para descargar imágenes de radar y mosaicos de las estaciones del SMN. La aplicación realiza solicitudes HTTP para obtener un token de autorización, obtener la lista de imágenes o mosaicos de una estación, y luego descargarlas y guardarlas en un repositorio local.

## Características

- **Descarga de Imágenes de Radar:** El robot permite descargar imágenes de radar de las estaciones del SMN y guardarlas en un repositorio local.
- **Descarga de Mosaicos:** Además de imágenes individuales, el robot puede descargar mosaicos de radar.

## Instalación

Para instalar las dependencias necesarias, puedes utilizar `pip`:

```sh
pip install -r requirements.txt
```

## Uso

### Descarga de Imágenes de Radar

Para ejecutar el robot de descarga de imágenes de radar, utiliza el módulo correspondiente. Si no se proveen argumentos, se utilizarán los valores por defecto.

```sh
python download_images.py -p <ruta_del_directorio_repositorio> -t <periodo_de_tiempo_de_escaneo> -s <lista_de_identificadores_de_estaciones>
```

### Descarga de Mosaicos

Para ejecutar el robot de descarga de mosaicos de radar, utiliza el módulo correspondiente. Si no se proveen argumentos, se utilizarán los valores por defecto.

```sh
python download_mosaics.py -p <ruta_del_directorio_repositorio> -t <periodo_de_tiempo_de_escaneo> -m <lista_de_identificadores_de_mosaicos>
```

## Ejemplos

### Ejemplo de Descarga de Imágenes de Radar

```sh
python download_images.py -p ./radar_images -t 10 -s station1 station2
```

### Ejemplo de Descarga de Mosaicos

```sh
python download_mosaics.py -p ./mosaic_images -t 10 -m mosaic1 mosaic2
```

## Documentación de la Clase Principal

### `RobotSmnRadar`

Clase principal para el scraper de imágenes de radar del SMN.

#### Atributos

- `local_repository_path` (str): La ruta del repositorio local donde se guardarán las imágenes.
- `scan_period_minutes` (int): El período de escaneo en minutos.
- `minimum_wait_time_seconds` (float): El tiempo mínimo de espera en segundos.
- `authorization_token` (str): El token de autorización.

#### Métodos

- `download_image(image_name)`: Descarga una imagen de radar.
- `get_authorization()`: Obtiene un token de autorización.
- `get_authorization_token(first_call)`: Obtiene un token de autorización.
- `get_image_list(station_id, token)`: Obtiene la lista de imágenes de una estación.
- `load_authorization_token(credentials_path)`: Obtiene un token de autorización de un archivo de credenciales.
- `renew_authorization()`: Renueva un token de autorización.
- `retrieve(station_ids, initial_date, final_date)`: Recupera las imágenes de radar del SMN en un rango de fechas.
- `run(station_ids)`: Ejecuta el robot scraper de imágenes de radar del SMN.
- `save_authorization_token(credentials_path, token)`: Guarda un token de autorización en un archivo de credenciales.
- `save_image(image_name, image_data)`: Guarda una imagen de radar en el repositorio local.

### Inicialización

```python
robot = RobotSmnRadar(
    local_repository_path='./radar_images',
    scan_period_minutes=10,
    minimum_wait_time_seconds=1.0
)
```

### Ejecución

```python
robot.run(['station1', 'station2'])
```

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulte el archivo LICENSE para más detalles.