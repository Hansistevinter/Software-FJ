from gestor import GestorSistema
from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSistema
from logger_config import logger

def leer(texto):
    return input(texto).strip()

def ejecutar_pruebas(gestor):
    """Ejecuta más de diez operaciones, incluyendo escenarios fallidos."""
    print("\n--- PRUEBAS AUTOMÁTICAS DE SOFTWARE FJ ---")
    operaciones = 0

    def prueba(nombre, accion, esperada=True):
        nonlocal operaciones
        operaciones += 1
        try:
            resultado = accion()
            if esperada:
                print(f"[OK] {nombre}" + (f": {resultado}" if resultado is not None else ""))
            else:
                print(f"[FALLO DE PRUEBA] {nombre}: se esperaba una excepción.")
        except Exception as exc:
            logger.exception("Prueba '%s' produjo error controlado.", nombre)
            if not esperada:
                print(f"[OK] {nombre}: excepción controlada ({exc})")
            else:
                print(f"[ERROR] {nombre}: {exc}")

    prueba("Registrar cliente válido", lambda: gestor.registrar_cliente(
        Cliente("CC1001", "Ana Pérez", "ana@example.com", "3001234567")))
    prueba("Rechazar correo inválido", lambda: Cliente("CC1002", "Luis Díaz", "correo-invalido", "3001234567"), False)
    prueba("Rechazar identificación duplicada", lambda: gestor.registrar_cliente(
        Cliente("CC1001", "Ana Pérez", "ana2@example.com", "3001234567")), False)
    prueba("Crear sala correctamente", lambda: gestor.agregar_servicio(
        ReservaSala("S01", "Sala ejecutiva", 50000, 12)))
    prueba("Registrar servicio no disponible", lambda: gestor.agregar_servicio(
    ReservaSala("S03", "Sala temporal", 40000, 8, disponible=False)))
    prueba("Rechazar reserva de servicio no disponible",
       lambda: gestor.crear_reserva("R05", "CC1001", "S03", 1), False)
    prueba("Rechazar tarifa negativa", lambda: ReservaSala("S02", "Sala inválida", -10, 5), False)
    prueba("Crear alquiler de equipos", lambda: gestor.agregar_servicio(
        AlquilerEquipo("E01", "Proyector", 15000, 2)))
    prueba("Crear asesoría especializada", lambda: gestor.agregar_servicio(
        AsesoriaEspecializada("A01", "Consultoría TI", 80000, "Tecnología")))
    prueba("Crear reserva válida", lambda: gestor.crear_reserva("R01", "CC1001", "S01", 2))
    prueba("Rechazar cliente inexistente", lambda: gestor.crear_reserva("R02", "NO_EXISTE", "S01", 1), False)
    prueba("Rechazar duración inválida", lambda: gestor.crear_reserva("R03", "CC1001", "S01", -2), False)
    prueba("Confirmar reserva", lambda: gestor.buscar_reserva("R01").confirmar())
    prueba("Procesar reserva con impuesto y descuento", lambda: gestor.buscar_reserva("R01").procesar(0.19, 0.10))
    prueba("Rechazar descuento fuera de rango", lambda: gestor.buscar_reserva("R01").servicio.calcular_costo(
           2, impuesto=0.19, descuento=1.5), False)
    prueba("Rechazar segunda confirmación", lambda: gestor.buscar_reserva("R01").confirmar(), False)
    prueba("Cancelar reserva pendiente", lambda: gestor.crear_reserva("R04", "CC1001", "E01", 3).cancelar())
    print(f"\nPruebas ejecutadas: {operaciones}")
    print("La aplicación continúa activa después de los errores.")

def mostrar_menu():
    print("""
========================================
              SOFTWARE FJ
       SISTEMA DE GESTIÓN INTEGRAL
========================================
1. Registrar cliente
2. Consultar clientes
3. Crear servicio
4. Consultar servicios
5. Crear reserva
6. Confirmar reserva
7. Cancelar reserva
8. Procesar reserva
9. Consultar reservas
10. Ejecutar pruebas automáticas
0. Salir
""")

def main():
    gestor = GestorSistema()
    logger.info("Aplicación Software FJ iniciada.")
    while True:
        try:
            mostrar_menu()
            opcion = leer("Seleccione una opción: ")
            if opcion == "1":
                cliente = Cliente(leer("Identificación: "), leer("Nombre: "),
                                  leer("Correo: "), leer("Teléfono: "))
                gestor.registrar_cliente(cliente)
                print("Cliente registrado correctamente.")
            elif opcion == "2":
                print("\n".join(map(str, gestor.clientes)) or "No hay clientes registrados.")
            elif opcion == "3":
                print("Tipo: 1. Sala  2. Equipo  3. Asesoría")
                tipo = leer("Seleccione: ")
                codigo, nombre = leer("Código: "), leer("Nombre: ")
                tarifa = float(leer("Tarifa por hora: "))
                if tipo == "1":
                    servicio = ReservaSala(codigo, nombre, tarifa, int(leer("Capacidad: ")))
                elif tipo == "2":
                    servicio = AlquilerEquipo(codigo, nombre, tarifa, int(leer("Unidades: ")))
                elif tipo == "3":
                    servicio = AsesoriaEspecializada(codigo, nombre, tarifa, leer("Especialidad: "))
                else:
                    raise ValueError("Tipo de servicio no reconocido.")
                gestor.agregar_servicio(servicio)
                print("Servicio creado correctamente.")
            elif opcion == "4":
                print("\n".join(s.describir() for s in gestor.servicios) or "No hay servicios.")
            elif opcion == "5":
                reserva = gestor.crear_reserva(leer("Código de reserva: "),
                    leer("Identificación del cliente: "), leer("Código del servicio: "),
                    float(leer("Duración en horas: ")))
                print(f"Reserva creada: {reserva}")
            elif opcion == "6":
                gestor.buscar_reserva(leer("Código de reserva: ")).confirmar()
                print("Reserva confirmada.")
            elif opcion == "7":
                gestor.buscar_reserva(leer("Código de reserva: ")).cancelar()
                print("Reserva cancelada.")
            elif opcion == "8":
                reserva = gestor.buscar_reserva(leer("Código de reserva: "))
                impuesto = float(leer("Impuesto (ej. 0.19): ") or "0.19")
                descuento = float(leer("Descuento (ej. 0.10): ") or "0")
                print(f"Total procesado: ${reserva.procesar(impuesto, descuento):,.2f}")
            elif opcion == "9":
                print("\\n".join(map(str, gestor.reservas)) or "No hay reservas.")
            elif opcion == "10":
                ejecutar_pruebas(gestor)
            elif opcion == "0":
                logger.info("Aplicación Software FJ finalizada por el usuario.")
                print("Gracias por utilizar Software FJ.")
                break
            else:
                raise ValueError("Opción no válida. Seleccione una opción del menú.")
        except (ErrorSistema, ValueError, TypeError) as exc:
            logger.exception("Operación rechazada: %s", exc)
            print(f" No se pudo completar la operación: {exc}")
        except Exception as exc:
            logger.exception("Error inesperado en el menú principal.")
            print(f"Error inesperado controlado: {exc}")
        finally:
            # El ciclo del menú se mantiene disponible después de cada operación.
            pass

if __name__ == "__main__":
    main()
