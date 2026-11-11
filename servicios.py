from abc import ABC, abstractmethod
from entidades import Entidad
from excepciones import ServicioInvalidoError, ServicioNoDisponibleError

class Servicio(Entidad, ABC):
    """Clase abstracta para todos los servicios ofrecidos."""
    def __init__(self, codigo, nombre, tarifa_base, disponible=True):
        super().__init__(codigo)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio es obligatorio.")
        try:
            tarifa = float(tarifa_base)
        except (TypeError, ValueError) as exc:
            raise ServicioInvalidoError("La tarifa debe ser numérica.") from exc
        if tarifa <= 0:
            raise ServicioInvalidoError("La tarifa debe ser mayor que cero.")
        self.nombre = nombre.strip()
        self.tarifa_base = tarifa
        self.disponible = bool(disponible)

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    @abstractmethod
    def calcular_costo(self, duracion, *args, **kwargs):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def describir(self):
        pass

class ReservaSala(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0 or duracion > 24:
            raise ServicioInvalidoError("La duración de la sala debe estar entre 0 y 24 horas.")

    def calcular_costo(self, duracion, *args, **kwargs):
        self.validar_parametros(duracion)
        impuesto = kwargs.get("impuesto", args[0] if args else 0)
        descuento = kwargs.get("descuento", args[1] if len(args) > 1 else 0)
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise ServicioInvalidoError("Impuesto y descuento deben estar entre 0 y 1.")
        subtotal = self.tarifa_base * duracion
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)

    def describir(self):
        return f"Sala: {self.nombre} | ${self.tarifa_base:.2f}/hora | Capacidad: {self.capacidad}"

class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, unidades, disponible=True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if not isinstance(unidades, int) or unidades <= 0:
            raise ServicioInvalidoError("Las unidades deben ser un entero positivo.")
        self.unidades = unidades

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0 or duracion > 720:
            raise ServicioInvalidoError("La duración del alquiler debe estar entre 0 y 720 horas.")

    def calcular_costo(self, duracion, *args, **kwargs):
        self.validar_parametros(duracion)
        impuesto = kwargs.get("impuesto", args[0] if args else 0)
        descuento = kwargs.get("descuento", args[1] if len(args) > 1 else 0)
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise ServicioInvalidoError("Impuesto y descuento deben estar entre 0 y 1.")
        subtotal = self.tarifa_base * duracion * self.unidades
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)

    def describir(self):
        return f"Equipo: {self.nombre} | ${self.tarifa_base:.2f}/hora | Unidades: {self.unidades}"

class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La especialidad es obligatoria.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0 or duracion > 12:
            raise ServicioInvalidoError("La asesoría debe durar entre 0 y 12 horas.")

    def calcular_costo(self, duracion, *args, **kwargs):
        self.validar_parametros(duracion)
        impuesto = kwargs.get("impuesto", args[0] if args else 0)
        descuento = kwargs.get("descuento", args[1] if len(args) > 1 else 0)
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise ServicioInvalidoError("Impuesto y descuento deben estar entre 0 y 1.")
        subtotal = self.tarifa_base * duracion
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)

    def describir(self):
        return f"Asesoría: {self.nombre} | ${self.tarifa_base:.2f}/hora | Especialidad: {self.especialidad}"
