
from entidades import Entidad
from excepciones import ReservaInvalidaError, OperacionNoPermitidaError
from logger_config import logger


class Reserva(Entidad):
    ESTADOS = ("Pendiente", "Confirmada", "Cancelada", "Procesada")

    def __init__(self, codigo, cliente, servicio, duracion):
        super().__init__(codigo)

        from clientes import Cliente
        from servicios import Servicio

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "La reserva requiere un objeto Cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "La reserva requiere un objeto Servicio válido."
            )

        servicio.validar_disponibilidad()
        servicio.validar_parametros(duracion)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = float(duracion)
        self.estado = "Pendiente"
        self.costo = None

    def confirmar(self):
        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.estado = "Confirmada"
        logger.info("Reserva %s confirmada.", self.identificador)

    def cancelar(self):
        if self.estado in ("Cancelada", "Procesada"):
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva cancelada o procesada."
            )

        self.estado = "Cancelada"
        logger.info("Reserva %s cancelada.", self.identificador)

    def procesar(self, impuesto=0.19, descuento=0):
        try:
            if self.estado != "Confirmada":
                raise OperacionNoPermitidaError(
                    "La reserva debe estar confirmada antes de procesarse."
                )

            costo_calculado = self.servicio.calcular_costo(
                self.duracion,
                impuesto=impuesto,
                descuento=descuento
            )

            if costo_calculado <= 0:
                raise ReservaInvalidaError(
                    "El cálculo produjo un costo inconsistente."
                )

        except Exception as exc:
            logger.exception(
                "Error procesando reserva %s.",
                self.identificador
            )
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva."
            ) from exc

        else:
            self.costo = costo_calculado
            self.estado = "Procesada"

            logger.info(
                "Reserva %s procesada. Total: $%.2f",
                self.identificador,
                self.costo
            )

            return self.costo

        finally:
            logger.info(
                "Finalizó intento de procesamiento de reserva %s.",
                self.identificador
            )

    def describir(self):
        costo = (
            f"${self.costo:.2f}"
            if self.costo is not None
            else "Pendiente de cálculo"
        )

        return (
            f"{self.identificador} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} h | "
            f"Estado: {self.estado} | Total: {costo}"
        )

    def __str__(self):
        return self.describir()
