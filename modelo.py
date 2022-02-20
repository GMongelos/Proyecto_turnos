"""
Conexion a la base de datos
"""
import sqlite3
from sqlite3 import Error
from src.Utils import Logger


class Database:

    def __init__(self, nombre):
        self.nombre_db = nombre

    def conectar(self):
        """Conecta con la base de datos"""
        try:
            con = sqlite3.connect(self.nombre_db + ".db")
            return con
        except Error:
            print("Ocurrio un error al intentar conectar con la base de datos")
            obj_logger = Logger()
            obj_logger.loguear_error(Error)

    def crear_tabla(self, conexion):
        """Crea la tabla de turnos"""

        try:
            cursor_obj = conexion.cursor()
            cursor_obj.execute("""CREATE TABLE IF NOT EXISTS turnos(
                                id integer PRIMARY KEY, 
                                nombre TEXT NOT NULL,
                                apellido TEXT NOT NULL,
                                dni TEXT NOT NULL,
                                fecha TEXT NOT NULL,
                                profesional TEXT NOT NULL,
                                observaciones TEXT)""")
            conexion.commit()
        except Error:
            print("Hubo un error al crear tabla")
            obj_logger = Logger()
            obj_logger.loguear_error(Error)


if __name__ == '__main__':
    pass
