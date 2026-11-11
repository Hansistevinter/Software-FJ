from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import ErrorValidacion

class Entidad(ABC):
    """Abstracción general de las entidades del sistema."""
    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ErrorValidacion("El identificador es obligatorio.")
        self._identificador = identificador.strip()
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        pass
