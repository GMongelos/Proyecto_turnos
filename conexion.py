"""
Conexion a la base de datos
"""
import sqlite3
from sqlite3 import Error

def conectar():
    """Conecta con la base de datos"""

    try:
        con = sqlite3.connect('turnos.db')
        return con
    except Error:
        return print(Error)

def crear_tabla(con):
    """Crea la tabla de turnos"""

    try:
        cursor_obj = con.cursor()
        cursor_obj.execute("""CREATE TABLE IF NOT EXISTS turnos(
                            id integer PRIMARY KEY, 
                            nombre TEXT NOT NULL,
                            apellido TEXT NOT NULL,
                            dni TEXT NOT NULL,
                            fecha TEXT NOT NULL,
                            profesional TEXT NOT NULL,
                            observaciones TEXT)""")
        con.commit()
    except Error:
        print("Hubo un error al crear tabla")


if __name__ == '__main__':
    pass