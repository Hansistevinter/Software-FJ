import re
from entidades import Entidad
from excepciones import ClienteInvalidoError

class Cliente(Entidad):
    """Cliente con datos encapsulados y validaciones básicas."""
    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip().title()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ClienteInvalidoError("El correo electrónico no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        limpio = re.sub(r"\D", "", str(valor))
        if len(limpio) < 7 or len(limpio) > 15:
            raise ClienteInvalidoError("El teléfono debe contener entre 7 y 15 dígitos.")
        self.__telefono = limpio

    def describir(self):
        return f"{self.identificador} | {self.nombre} | {self.correo} | {self.telefono}"

    def __str__(self):
        return self.describir()
