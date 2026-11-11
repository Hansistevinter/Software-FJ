# Software FJ — Sistema de gestión integral

## Requisitos
- Python 3.9 o superior.
- No requiere instalar librerías externas.

## Ejecución
1. Extraer la carpeta `Software_FJ`.
2. Abrir una terminal en esa carpeta.
3. Ejecutar: `python main.py`

## Características
- Gestión en memoria mediante objetos y listas.
- No utiliza bases de datos.
- Clase abstracta general `Entidad` y clase abstracta `Servicio`.
- Cliente con atributos privados, propiedades y validaciones.
- Tres servicios especializados: salas, alquiler de equipos y asesorías.
- Reserva con estados, confirmación, cancelación y procesamiento.
- Cálculo polimórfico de costos con impuesto y descuento opcionales.
- Excepciones personalizadas y encadenamiento con `raise ... from exc`.
- Registro de eventos y errores en `software_fj.log`.
- Menú interactivo y pruebas automáticas.

## Nota sobre sobrecarga en Python
Python no implementa sobrecarga tradicional por firma como Java o C++. En este proyecto se demuestra flexibilidad mediante parámetros opcionales, `*args` y `**kwargs` en `calcular_costo`, permitiendo calcular el valor base, con impuesto o con impuesto y descuento.

## Almacenamiento
Clientes, servicios y reservas permanecen en listas durante la ejecución. El único archivo generado por la aplicación es `software_fj.log`, utilizado para registrar eventos y errores, no para almacenar datos operativos.
