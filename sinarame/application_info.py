class ApplicationInfo:
    """Información de la aplicación."""

    name: str = "robot_smn"
    alias: str = "RETSPy"
    version_short: str = "1.0.1"
    detail: str = "Indexador SINARAME"
    lemma: str = "Indexador de imágenes de radar del SINARAME"
    description: str = (
        "El indexador de imágenes de radar del Sistema Nacional de "
        "Radares Meteorológicos (SINARAME), del Servicio Meteorológico "
        "Nacional (SMN) argentino, permite descargar las imágenes de "
        "radar de las estaciones del SINARAME desde el sitio web de la "
        "SMN para guardarlas en un repositorio local. Las imágenes de "
        "radar del SINARAME se actualizan cada 10 minutos.\n\n"
        "El objetivo del bot es recopilar las información de radar "
        "asociada a eventos meteorológicos extremos en una región de "
        "interés, para archivarlos en la base de datos «RETSPy» de "
        "reportes de eventos de tiempo severo, para su análisis o "
        "estudio posterior."
    )

    default_settings: str = "settings.json"

    user_settings: str = "settings.snm.json"

    settings_model: str = "sinarame"

    banner: str = f"{alias} - {lemma}"

    title: str = f"{alias} ({detail})"

    version_full: str = f"{title} {version_short}"


info = ApplicationInfo
