# Proyecto turnos
Sistema de turnos v3.0

### Autores:
- Enzo Conejero
- Gastón César Mongelos

## Descripción:
Programado en python 3.8. Se trata de una aplicación que permite reservar turnos en un contexto de salud(hospital, clínica, etc). Para su posterior consulta, modificación o eliminación.

## Pre-requisitos
- Python 3.7+
- Sqlite3
- sqlAlchemy 1.4

## Instalación
- Descomprimir el archivo sistema_turnos.zip en alguna carpeta
- Se recomiendo utilizar un entorno virtual:
  1. Activar el entorno virtual
  2. Instalar las dependencias con pip instal -r requeriments.txt
- Ejecutar el archivo main.py

## Funcionamiento
Solo durante la primera ejecución, se crea la base de datos baseturnos.db y una tabla turnos vacía. Se nos presenta el menú principal, el cual nos ofrece varias opciones. La creacion, modificacion y eliminacion de turnos notifica al usuario mediante el mail provisto al momento de crear el turno.
