class ErrorSistema(Exception):
    """Excepción base para errores controlados del sistema."""

class ErrorValidacion(ErrorSistema):
    pass

class ClienteInvalidoError(ErrorValidacion):
    pass

class ClienteDuplicadoError(ErrorSistema):
    pass

class ServicioInvalidoError(ErrorValidacion):
    pass

class ServicioNoDisponibleError(ErrorSistema):
    pass

class ReservaInvalidaError(ErrorValidacion):
    pass

class OperacionNoPermitidaError(ErrorSistema):
    pass

class ElementoNoEncontradoError(ErrorSistema):
    pass
