from clientes import Cliente
from servicios import Servicio
from reservas import Reserva
from excepciones import (ClienteDuplicadoError, ElementoNoEncontradoError,
                         ServicioInvalidoError, ReservaInvalidaError)
from logger_config import logger

class GestorSistema:
    """Administra objetos en memoria mediante listas; no utiliza bases de datos."""
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise TypeError("Se esperaba un objeto Cliente.")
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ClienteDuplicadoError("Ya existe un cliente con esa identificación.")
        self.clientes.append(cliente)
        logger.info("Cliente registrado: %s.", cliente.identificador)
        return cliente

    def agregar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ServicioInvalidoError("El objeto no corresponde a un servicio válido.")
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise ServicioInvalidoError("Ya existe un servicio con ese código.")
        self.servicios.append(servicio)
        logger.info("Servicio creado: %s.", servicio.identificador)
        return servicio

    def crear_reserva(self, codigo, id_cliente, codigo_servicio, duracion):
        cliente = next((c for c in self.clientes if c.identificador == id_cliente), None)
        servicio = next((s for s in self.servicios if s.identificador == codigo_servicio), None)
        if cliente is None:
            raise ElementoNoEncontradoError("No existe el cliente indicado.")
        if servicio is None:
            raise ElementoNoEncontradoError("No existe el servicio indicado.")
        if any(r.identificador == codigo for r in self.reservas):
            raise ReservaInvalidaError("El código de reserva ya existe.")
        reserva = Reserva(codigo, cliente, servicio, duracion)
        self.reservas.append(reserva)
        logger.info("Reserva creada: %s.", codigo)
        return reserva

    def buscar_reserva(self, codigo):
        reserva = next((r for r in self.reservas if r.identificador == codigo), None)
        if reserva is None:
            raise ElementoNoEncontradoError(f"No existe la reserva {codigo}.")
        return reserva
