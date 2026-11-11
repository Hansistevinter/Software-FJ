import logging
from pathlib import Path

def configurar_logger():
    """Configura el registro de eventos y errores en un único archivo."""
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        ruta = Path(__file__).resolve().parent / "software_fj.log"
        manejador = logging.FileHandler(ruta, encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
    return logger

logger = configurar_logger()
